from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.core.db import models, schemas, crud
from app.core.db.base import SessionLocal, engine
from app.core.db.crud import get_user_by_email, update_user, update_user_points, get_user
from app.core.db.schemas import UserCreate, UserBase, Login, UserUpdate, PointsUpdate
from passlib.context import CryptContext

from app.core.prompt_image.createPrompt import create_prompt

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


# Dependency(DB 접근 함수)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 유저 생성
# 프론트앤드에서 오류가 낫을때, 필드의 값을 대채워달라는 메시지 표시(422 Unprocessable Entity 응답일때)
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, e_mail=user.e_mail) or crud.get_user_by_nickname(db, nickname=user.nickname):
        raise HTTPException(status_code=400, detail="Email or nickname already registered")
    return crud.create_user(db=db, user_create=user)

@app.get("/users/{user_id}/readuser", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user

@app.get("/users/check_email/")
def check_email(email: str, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, e_mail=email):
        return {"is_available": False}
    return {"is_available": True}


@app.get("/users/check_nickname/")
def check_nickname(nickname: str, db: Session = Depends(get_db)):
    if crud.get_user_by_nickname(db, nickname=nickname):
        return {"is_available": False}
    return {"is_available": True}


# 사용자 정보를 검색하는 엔드포인트
@app.get("/users/{e_mail}", response_model=schemas.UserBase)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, e_mail=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login/", response_model=UserBase)
def login(credentials: Login, db: Session = Depends(get_db)):
    user = get_user_by_email(db, e_mail=credentials.e_mail)
    # 비밀번호 확인
    if not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user


@app.put("/user/{user_id}/update")
def update_user_info(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data_dict = update_data.dict()
    update_user(db, user_id, update_data_dict)

    db.refresh(existing_user)

    return {
        "user_id": existing_user.user_id,
        "nickname": existing_user.nickname,
        "profile_image": existing_user.profile_image

    }

@app.put("/user/{user_id}/points")
def update_points(user_id: int, points_update: PointsUpdate, db: Session = Depends(get_db)):
    try:
        update_user_points(db, user_id, points_update.user_point)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "user_point": points_update.user_point,
        "message": "User points updated successfully"
    }

@app.get("/user/{user_id}/ranking")
def get_user_ranking(user_id: int, db: Session = Depends(get_db)):
    ranking = db.query(models.Ranking).filter(models.Ranking.user_id == user_id).first()
    if ranking is None:
        raise HTTPException(status_code=404, detail="Ranking not found for user")

    return {
        "user_id": ranking.user_id,
        "ranking_position": ranking.ranking_position,
        "user_point": ranking.user_point
    }

@app.get("/scripts_read/{scripts_id}")
def read_script(scripts_id: int, db: Session = Depends(get_db)):
    db_script = crud.get_script(db, scripts_id=scripts_id)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script

@app.post("/create_prompt_and_save/")
async def create_prompt_and_save(db: Session = Depends(get_db)):
    parts, level, category = await create_prompt()
    script_data = {
        "level": 1,
        "category_name": 1,
        "content_1": parts[0],
        "content_2": parts[1],
        "content_3": parts[2],
        "inspection_status": False
    }
    new_script = crud.create_script(db=db, script_data=script_data)
    return new_script

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
