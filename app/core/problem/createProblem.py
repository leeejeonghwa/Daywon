import httpx
from app.core.api import util_api, get_api_key  # 앞서 정의한 함수를 임포트


async def create_problem(script, example_script, level):
    api_key = get_api_key()
    # model = 'ft:gpt-3.5-turbo-0125:personal:daywon123:9HulgDod'
    model = 'gpt-4'

    system_prompt = f"""
    다음 조건을 모두 만족하는 문제를 만들어주세요.
    1 - 10대가 이해할 수 있도록 작성해주세요.
    2 - 생성된 문제의 보기는 4개만 만들어 주세요.
    3 - 문제의 정답에 대한 설명과 오답에 대한 설명을 해설로 작성해주세요.
    4 - 문제를 생성할 때에는 한글만 사용해주세요.
    5 - 앞 뒤 문맥을 고려해서 문장들을 작성해주세요.
    6 - 명확한 정답 보기 하나와 확실한 오답이유가 있는 오답 보기 3개로 만들어주세요.
    7 - 만약 영어가 포함되어 있으면 한국어로 번역해주세요.

    다음 형식을 사용하십시오.
    문제 :
    보기 :
    1.
    2.
    3.
    4.
    정답 :
    해설 :
    """

    if level is None:
        return "레벨을 읽어 오는 중 오류가 발생했습니다."
    if level == 1:
        system_prompt = system_prompt + "초등학교 1학년 학생들을 위한 난이도로 문제를 만들어 주세요."
    elif level == 2:
        system_prompt = system_prompt + "초등학교 3학년 학생들을 위한 난이도로 문제를 만들어 주세요."
    elif level == 3:
        system_prompt = system_prompt + "초등학교 6학년 학생들을 위한 난이도로 문제를 만들어 주세요."
    elif level == 4:
        system_prompt = system_prompt + "중학교 2학년 학생들을 위한 난이도로 문제를 만들어 주세요."
    elif level == 5:
        system_prompt = system_prompt + "고등학교 3학년 학생들을 위한 난이도로 문제를 만들어 주세요."
    else:
        return "유효하지 않은 레벨입니다."

    user_prompt = f"""
    문제: {script}와 {example_script}에서 언급한 내용을 이용하여 객관식 문제 하나를 만들어주세요.
    """
    # 문제 형식은 객관식이며, 선택지는 4 개입니다.
    #     문제의 정답은 확실하게 한 개만 존재해야 합니다.
    #     정답이 아닌 나머지 3개의 선택지는 명백히 오답이어야 합니다.
    #     해설: 문제의 정답과 왜 그 답이 맞는지에 대해 간단하고 이해하기 쉬운 설명을 포함해주세요.
    #     영어가 아닌 한글 또는 한국어로만 작성해주세요.

    api_url, headers, data = util_api(api_key, model, system_prompt, user_prompt)

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return f"에러: {response.status_code}, {response.text}"
