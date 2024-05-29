import httpx
import random
from app.core.api import util_api, get_api_key


async def call_api(api_url, headers, data):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return f"Error: {response.status_code}, {response.text}"


async def create_prompt():
    api_key = get_api_key()
    model = 'gpt-4'

    level = get_finance_level()
    category = get_finance_category()
    print(level)
    print(category)
    if level == 1:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 저학년 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 초등학교 저학년 학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 2:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 고학년 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 초등학교 고학년 학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 간단한 개념을 이해할 수 있으며, 더 구체적인 예시와 약간의 수학적 설명도 가능합니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 3:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 중학교 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 중학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 추상적인 개념을 이해할 수 있으며, 실제 생활과 관련된 예시를 통해 더 깊이 있는 내용을 다룰 수 있습니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 4:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 고등학교 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 고등학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 복잡한 개념을 이해하고, 장기적인 재무 계획에 대해 생각할 수 있습니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 5:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 대학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 대학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 독립적인 재무 결정을 내릴 준비가 되어 있으며, 고급 금융 개념을 이해할 수 있습니다. 
        5 - 대상을 언급하지 마세요.
        """
    else:
        return "Invalid level"

    additional_prompts = ['기본 개념과 용어 설명', '다양한 금융 상품의 상세 정보', '특징']
    selected_additional_prompt = random.choice(additional_prompts)
    user_prompt = f"""
    다음 동작을 수행하세요.
    1 - {category}에 관련된 {selected_additional_prompt}에 대해서 설명해주세요. 
    """
    print(f"additional prompts : {selected_additional_prompt}\n")
    api_url, headers, data = util_api(api_key, model, system_prompt, user_prompt)

    # return await call_api(api_url, headers, data)

    conceptual_script = await call_api(api_url, headers, data)
    return conceptual_script, level, category


async def create_example_prompt(finance_category, level):
    api_key = get_api_key()
    model = 'gpt-4'

    if level == 1:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 저학년 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 2:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 고학년 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 3:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 중학교 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """
    elif level == 4:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 고등학교 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 5:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 대학생 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """
    else:
        return "Invalid level"

    user_prompt = f"""
    다음 동작을 수행하세요. 
    1 - {finance_category}에 대한 구체적인 실생활 예시를 들어주세요.
    """
    api_url, headers, data = util_api(api_key, model, system_prompt, user_prompt)
    return await call_api(api_url, headers, data)


def get_finance_category():
    finance_categories = [
        # 금융상품
        "예금", "정기예금", "적금", "자유예금", "정기적금", "자유적립식 적금", "연금저축", "목표달성 저축", "주택청약종합저축통장",
        "아이사랑통장", "주식저축", "채권저축", "펀드저축", "외화저축", "생활저축", "월급저축",
        "예비 부모 저축", "교육 저축", "외식 저축", "상품 저축", "부동산 저축", "대출 담보 저축", "보험 연계 저축",
        "세금 저축", "청년 적금", "외국인 적금", "연금 보험 저축", "청약 자금 적금", "증권연계 적금", "종합저축",
        "자동이체 적금", "비과세 적금", "연금 저축", "단리이자", "복리이자", "정액이자", "비정액이자",
        "고정금리", "변동금리", "연간이자", "월간이자", "주간이자", "일간이자", "대출", "카드", "세금 및 공과금",
        "주식펀드", "채권펀드", "혼합펀드", "해외펀드", "특수목적펀드", "채권형펀드",
        "주식형펀드", "인덱스펀드", "화폐시장펀드", "부동산펀드", "적립식펀드", "국내주식펀드",
        "해외주식펀드", "파생상품펀드", "공모펀드", "ETF", "종합펀드", "인플레이션펀드",
        "기술펀드", "중국펀드", "일본펀드", "신흥시장펀드", "미국펀드", "유럽펀드",
        "환율펀드", "환헤지펀드", "부채펀드", "자금운용펀드",

        # 세금 및 공과금
        "소득세", "부가가치세 (VAT)", "법인세", "지방소득세", "지방법인세",
        "주민세", "취득세", "증여세", "상속세", "주택세",
        "특별소득세", "세금공제", "종합소득세", "법인세율",
        "주민세율", "취득세율", "증여세율", "상속세율", "주택세율",
        "소득세환급", "부가가치세환급", "법인세환급", "지방소득세환급", "지방법인세환급",
        "주민세환급", "취득세환급", "증여세환급", "상속세환급", "주택세환급",

        # 대출 및 부채
        "주택담보대출", "신용대출", "자동차 담보대출", "증권담보대출", "급여대출",
        "농어업용부대출", "대학자금대출", "전세자금대출", "신차대출", "마이너스 통장 대출",
        "개인신용대출", "사업자대출", "중소기업대출", "법인대출", "주택담보대출 연체",
        "신용대출 연체", "마이너스 통장 대출 연체", "개인신용대출 연체", "사업자대출 연체",
        "중소기업대출 연체", "법인대출 연체", "주택담보대출 상환", "신용대출 상환",
        "마이너스 통장 대출 상환", "개인신용대출 상환", "사업자대출 상환", "중소기업대출 상환",
        "법인대출 상환", "주택담보대출 이자", "신용대출 이자", "마이너스 통장 대출 이자",
        "개인신용대출 이자", "사업자대출 이자", "중소기업대출 이자", "법인대출 이자",
        "주택담보대출 금리", "신용대출 금리", "마이너스 통장 대출 금리", "개인신용대출 금리",
        "사업자대출 금리", "중소기업대출 금리", "법인대출 금리", "주택담보대출 한도",
        "신용대출 한도", "마이너스 통장 대출 한도", "개인신용대출 한도", "사업자대출 한도",
        "중소기업대출 한도", "법인대출 한도",

        # 결제 수단
        "신용카드", "체크카드", "선불카드", "기프트카드", "멤버십카드", "스마트카드",
        "바코드 카드", "결제 카드", "리워드 카드", "할인카드", "캐시백카드", "충전식 카드"
    ]

    finance_category = random.choice(list(finance_categories))
    return finance_category


def get_finance_level(finance_level=None):
    # 예시
    finance_levels = {1, 2, 3, 4, 5}
    if finance_level is None:
        finance_level = random.choice(list(finance_levels))
    return finance_level


# 두 문장씩 분리
def split_text_two(text):
    # 문장을 온점(.) 기준으로 나누기
    sentences = text.split('.')

    # 결과가 빈 문자 열이 아닌 경우 에만 리스트에 추가
    sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
    sentence_pairs = []

    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            sentence_pairs.append(sentences[i] + " " + sentences[i + 1])
        else:
            sentence_pairs.append(sentences[i])
    return sentence_pairs


# 한 문장 분리
def split_text(text):
    # 문장을 온점(.) 기준으로 나누기
    sentences = text.split('.')

    # 결과가 빈 문자열이 아닌 경우에만 리스트에 추가
    sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
    return sentences
