import os
import re
import pandas as pd

def extract_latest_issue_date(text):
    """
    OCR 텍스트에서 가장 최신 발급 날짜를 찾는 함수.
    """
    # 1️⃣ YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD (월/일 2자리)
    pattern1 = r"(\d{4})[./-](\d{2})[./-](\d{2})"

    # 2️⃣ YYYY-M-DD, YYYY/M/DD, YYYY.M.DD (월 1자리, 일 2자리)
    pattern2 = r"(\d{4})[./-](\d{1})[./-](\d{2})"

    # 3️⃣ YYYY-MM-D, YYYY/MM/D, YYYY.MM.D (월 2자리, 일 1자리)
    pattern3 = r"(\d{4})[./-](\d{2})[./-](\d{1})"

    # 4️⃣ YYYY-M-D, YYYY/M/D, YYYY.M.D (월/일 모두 1자리)
    pattern4 = r"(\d{4})[./-](\d{1})[./-](\d{1})"

    # 5️⃣ 한글 포함 YYYY년 MM월 DD일, YYYY년 M월 D일 등
    pattern5 = r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일"

    # 🔹 모든 패턴에서 날짜 찾기
    matches = (
        re.findall(pattern1, text)
        + re.findall(pattern2, text)
        + re.findall(pattern3, text)
        + re.findall(pattern4, text)
        + re.findall(pattern5, text)
    )

    # 🔹 날짜 변환 및 최신 날짜 찾기
    parsed_dates = []
    date_values = []
    for match in matches:
        try:
            year, month, day = int(match[0]), int(match[1]), int(match[2])
            days_since_start = year * 365 + month * 30 + day  # 날짜를 일수로 변환하여 비교
            parsed_dates.append((year, month, day))
            date_values.append(days_since_start)
        except Exception as e:
            print(f"⚠️ 날짜 변환 오류 발생: {match} → {e}")

    # 🔹 최신 날짜 찾기 (max 적용)
    if parsed_dates:
        latest_idx = date_values.index(max(date_values))  # 가장 큰 값을 가진 인덱스 찾기
        latest_year, latest_month, latest_day = parsed_dates[latest_idx]
        return f"{latest_year}-{latest_month:02d}-{latest_day:02d}"  # YYYY-MM-DD 포맷으로 반환

    return None  # 날짜를 찾지 못한 경우

# ✅ 주민등록번호 앞 6자리 추출 함수 (여러 개 검출 시 첫 번째 값 선택)
def extract_birth_date_from_text(text):
    """
    '주민등록번호'라는 단어 뒤에 나오는 6자리 숫자를 찾고, 여러 개가 검출되면 첫 번째 값 반환.
    """
    matches = re.findall(r"주민등록번호.*?(\d{6})", text)
    return matches[0] if matches else None  # 첫 번째 값 선택

# ✅ 초본 정보 추출 함수
def extract_info_from_chobon(name, text):
    """
    초본에서 필요한 정보 (자격번호, 발급날짜, 주민등록번호) 추출
    """
    result = {
        
        "초본_확인번호": [],
        "초본_발급날짜": [],
        "초본_생년월일6자리": []
    }

    text = text.replace(" ", "")  # OCR 오류 방지
    text = text.replace("--","-")

    # 🔹 초본 자격번호 (4-4-4-4 형식)
    serial_number_match = re.findall(r"\d{4}-\d{4}-\d{4}-\d{4}", text)
    if serial_number_match:
        result["초본_확인번호"].extend(serial_number_match)

    # 🔹 발급 날짜 (가장 최근 날짜만 저장)
    latest_issue_date = extract_latest_issue_date(text)
    if latest_issue_date:
        result["초본_발급날짜"].append(latest_issue_date)

    # 🔹 특정 name과 연결된 주민등록번호에서 앞 6자리 추출
    birth_date = extract_birth_date_from_text(text)
    if birth_date:
        result["초본_생년월일6자리"].append(birth_date)

    return result

# # ✅ 입력 및 출력 파일 경로
# input_file = "./chobon_input.xlsx"
# output_file = "./test_chobon_output.xlsx"

# # ✅ 엑셀 파일 읽기
# df = pd.read_excel(input_file)

# # ✅ 결과를 저장할 데이터프레임 생성 (출력 컬럼 맞추기)
# output_columns = ["이름", "초본_확인번호", "초본_발급날짜", "초본_생년월일6자리"]
# results_df = pd.DataFrame(columns=output_columns)

# # ✅ 첫 번째 행(컬럼명) 제외, 각 행별 OCR 추출
# for index, row in df.iterrows():
#     file_name = row["파일명"]
#     text = row["ocr_text"]

#     # ✅ 초본 추출 함수 실행
#     extracted_data = extract_info_from_chobon( text)

#     # ✅ 결과 데이터프레임에 추가
#     new_row = pd.DataFrame({
#         "파일명":file_name,
#         "초본_확인번호": [", ".join(extracted_data["초본_확인번호"]) if extracted_data["초본_확인번호"] else ""],
#         "초본_발급날짜": [", ".join(extracted_data["초본_발급날짜"]) if extracted_data["초본_발급날짜"] else ""],
#         "초본_생년월일6자리": [", ".join(extracted_data["초본_생년월일6자리"]) if extracted_data["초본_생년월일6자리"] else ""]
#     })

#     results_df = pd.concat([results_df, new_row], ignore_index=True)

# # ✅ 결과 엑셀 파일 저장
# results_df.to_excel(output_file, index=False)

# print(f"✅ 초본 추출 테스트 완료! 결과가 {output_file}에 저장되었습니다.")
