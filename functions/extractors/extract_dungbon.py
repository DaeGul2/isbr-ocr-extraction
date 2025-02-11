import re
from functions.extractors.utils import extract_latest_issue_date  # 발급일 추출 함수

def extract_info_from_dungbon(name, text):
    """
    등본에서 필요한 정보 (자격번호, 발급날짜, 주민등록번호) 추출
    """
    result = {
        "이름": name,  # 이름 포함
        "등본_자격번호": [],
        "등본_발급날짜": [],
        "생년월일6자리_등본": []
    }

    text = text.replace(" ", "")  # OCR 오류 방지

    # 🔹 등본 자격번호 (4-4-4-4 형식)
    serial_number_match = re.findall(r"\d{4}-\d{4}-\d{4}-\d{4}", text)
    if serial_number_match:
        result["등본_자격번호"].extend(serial_number_match)

    # 🔹 발급 날짜 (가장 최근 날짜만 저장)
    latest_issue_date = extract_latest_issue_date(text)
    if latest_issue_date:
        result["등본_발급날짜"].append(latest_issue_date)

    # 🔹 주민등록번호에서 생년월일 추출 (6자리-7자리)
    id_number_match = re.findall(r"\d{6}-\d{7}", text)
    if id_number_match:
        birth_dates = [num.split("-")[0] for num in id_number_match]
        result["생년월일6자리_등본"].extend(birth_dates)

    return result
