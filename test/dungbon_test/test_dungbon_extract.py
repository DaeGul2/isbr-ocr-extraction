import os
import re
import pandas as pd

# ✅ 최신 발급 날짜 찾기 함수
def extract_latest_issue_date(text):
    """
    OCR 텍스트에서 가장 최근 발급 날짜를 찾는 함수.
    """
    # 1️⃣ 일반 날짜 포맷 (YYYY.MM.DD, YYYY/MM/DD, YYYY-MM-DD)
    pattern1 = r"\d{4}[./-]\d{2}[./-]\d{2}"
    
    # 2️⃣ 한글 포함 날짜 포맷 (YYYY년MM월DD일)
    pattern2 = r"\d{4}년\d{1,2}월\d{1,2}일"
    
    # 🔹 모든 날짜 찾기
    matches = re.findall(f"{pattern1}|{pattern2}", text)
    
    # 🔹 날짜 변환 & 최신 날짜 찾기
    if matches:
        # 날짜 포맷 통일 (YYYY-MM-DD 형식으로 변환)
        formatted_dates = [re.sub(r"[년월]", "-", date).replace("일", "") for date in matches]
        latest_date = max(formatted_dates)  # 가장 최신 날짜 찾기
        return latest_date

    return None  # 날짜를 찾지 못한 경우

# ✅ 주민등록번호(생년월일) 추출 함수
def extract_resident_registration_number(name, text):
    """
    주어진 name과 매칭되는 주민등록번호(6자리)를 추출
    1. text에서 name 뒤의 100글자를 가져옴 (여러 개 가능)
    2. 가져온 부분에서 주민등록번호 패턴을 찾아 0번 인덱스를 반환
    """
    extracted_sections = []
    matches = re.finditer(rf"{name}(.{{0,100}})", text)  # name 뒤 100글자 가져오기

    for match in matches:
        extracted_sections.append(match.group(1))  # name 이후 100글자 저장

    for section in extracted_sections:
        resident_number_match = re.findall(r"\d{6}-\d{7}", section)  # 주민등록번호 패턴 찾기
        if resident_number_match:
            return resident_number_match[0][:6]  # 첫 번째 주민등록번호의 앞 6자리 반환

    return None  # 매칭되는 주민번호가 없으면 None 반환

# ✅ 등본 정보 추출 함수
def extract_info_from_dungbon(name, text):
    """
    등본에서 필요한 정보 (자격번호, 발급날짜, 주민등록번호) 추출
    """
    result = {
        "이름": name,
        "등본_확인번호": [],
        "등본_발급날짜": [],
        "생년월일6자리_등본": []
    }

    text = text.replace(" ", "")  # OCR 오류 방지

    # 🔹 등본 자격번호 (4-4-4-4 형식)
    serial_number_match = re.findall(r"\d{4}-\d{4}-\d{4}-\d{4}", text)
    if serial_number_match:
        result["등본_확인번호"].extend(serial_number_match)

    # 🔹 발급 날짜 (가장 최근 날짜만 저장)
    latest_issue_date = extract_latest_issue_date(text)
    if latest_issue_date:
        result["등본_발급날짜"].append(latest_issue_date)

    # 🔹 특정 name과 연결된 주민등록번호에서 앞 6자리 추출
    birth_date = extract_resident_registration_number(name, text)
    if birth_date:
        result["생년월일6자리_등본"].append(birth_date)

    return result

# ✅ 입력 및 출력 파일 경로
input_file = "./dungbon_input.xlsx"
output_file = "./test_dungbon_output.xlsx"

# ✅ 엑셀 파일 읽기
df = pd.read_excel(input_file)

# ✅ 결과를 저장할 데이터프레임 생성 (출력 컬럼 맞추기)
output_columns = ["이름", "등본_확인번호", "등본_발급날짜", "생년월일6자리_등본"]
results_df = pd.DataFrame(columns=output_columns)

# ✅ 첫 번째 행(컬럼명) 제외, 각 행별 OCR 추출
for index, row in df.iterrows():
    name = row["이름"]
    text = row["ocr_text"]

    # ✅ 등본 추출 함수 실행
    extracted_data = extract_info_from_dungbon(name, text)

    # ✅ 결과 데이터프레임에 추가
    new_row = pd.DataFrame({
        "이름": [extracted_data["이름"]],
        "등본_확인번호": [", ".join(extracted_data["등본_확인번호"]) if extracted_data["등본_확인번호"] else ""],
        "등본_발급날짜": [", ".join(extracted_data["등본_발급날짜"]) if extracted_data["등본_발급날짜"] else ""],
        "생년월일6자리_등본": [", ".join(extracted_data["생년월일6자리_등본"]) if extracted_data["생년월일6자리_등본"] else ""]
    })

    results_df = pd.concat([results_df, new_row], ignore_index=True)

# ✅ 결과 엑셀 파일 저장
results_df.to_excel(output_file, index=False)

print(f"✅ 등본 추출 테스트 완료! 결과가 {output_file}에 저장되었습니다.")
