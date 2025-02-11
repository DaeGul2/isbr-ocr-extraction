from datetime import datetime

def extract_latest_issue_date(text):
    """
    문서에서 'YYYY.MM.DD', 'YYYY/MM/DD', 'YYYY-MM-DD', 'YYYY년MM월DD일' 형식의 날짜를 추출 후 가장 최근 날짜 반환
    """
    # 1️⃣ 기존 형식 (YYYY.MM.DD, YYYY/MM/DD, YYYY-MM-DD)
    pattern1 = r"\d{4}[./-]\d{2}[./-]\d{2}"
    
    # 2️⃣ 한글 포함 형식 (YYYY년MM월DD일)
    pattern2 = r"\d{4}년\d{1,2}월\d{1,2}일"
    
    # 두 가지 패턴을 모두 찾기
    matches = re.findall(f"{pattern1}|{pattern2}", text)

    # 날짜 변환 (YYYY-MM-DD 형태로 통일)
    parsed_dates = []
    for date in matches:
        if "년" in date:  # 한글 포함 날짜 변환
            date = date.replace("년", "-").replace("월", "-").replace("일", "")
        date = date.replace("/", "-").replace(".", "-")  # YYYY-MM-DD 형식으로 변환
        try:
            parsed_dates.append(datetime.strptime(date, "%Y-%m-%d"))
        except ValueError:
            continue  # 잘못된 날짜 형식은 무시
    
    # 가장 최근 날짜 찾기
    if parsed_dates:
        latest_date = max(parsed_dates)  # 최신 날짜 선택
        return latest_date.strftime("%Y-%m-%d")  # 최종 출력 형식

    return None  # 날짜를 찾지 못한 경우
