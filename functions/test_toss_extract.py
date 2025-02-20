import os
import re
import pandas as pd

# ✅ 날짜 추출 함수 (가장 오래된 날짜 찾기)
def extract_earliest_birth_date(text):
    """
    OCR 텍스트에서 가장 오래된 생년월일(YYYY-MM-DD)을 찾는 함수.
    """
    pattern1 = r"(\d{4})[./-](\d{2})[./-](\d{2})"
    pattern2 = r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일"

    matches = re.findall(pattern1, text) + re.findall(pattern2, text)

    parsed_dates = []
    date_values = []
    for match in matches:
        try:
            if match[0][0]=='0':
                continue
            year, month, day = int(match[0]), int(match[1]), int(match[2])
            days_since_start = year * 365 + month * 30 + day  # 날짜를 일수로 변환하여 비교
            parsed_dates.append((year, month, day))
            date_values.append(days_since_start)
        except Exception as e:
            print(f"⚠️ 날짜 변환 오류 발생: {match} → {e}")

    # 🔹 가장 오래된(최소값) 날짜 찾기
    if parsed_dates:
        earliest_idx = date_values.index(min(date_values))  # 가장 작은 값을 가진 인덱스 찾기
        earliest_year, earliest_month, earliest_day = parsed_dates[earliest_idx]
        return f"{earliest_year}-{earliest_month:02d}-{earliest_day:02d}"  # YYYY-MM-DD 포맷 반환

    return None  # 날짜를 찾지 못한 경우

# ✅ 토스 정보 추출 함수
def extract_info_from_toss(name, text):
    """
    토스 성적표에서 필요한 정보 (수험번호, 발급번호, 생년월일) 추출
    """
    result = {
        "검출_원본":[],
        "토스_수험번호": [],
        "토스_발급번호": [],
        "토스_생년월일": []
    }
    result["검출_원본"].append(text)

    text = text.replace(" ", "").lower()  # OCR 오류 방지 & 소문자로 변환
    text = text.replace("--","-")

    # 🔹 (1) 토스 수험번호 (10자리/2자리/2자리 → 앞 6자리)
    pattern_registration = r"(\d{10}/\d{2}/\d{2})"
    match_registration = re.findall(pattern_registration, text)
    if match_registration:
        registration_number = match_registration[0].split("/")[0][:6]  # 앞 6자리 추출
        result["토스_수험번호"].append(registration_number)

    # 🔹 (2) 토스 발급번호 (6자리-10자리)
    pattern_certificate = r"(\d{6}-\d{10})"
    match_certificate = re.findall(pattern_certificate, text)
    if match_certificate:
        result["토스_발급번호"].append(match_certificate[0])  # 첫 번째 값만 저장

    # 🔹 (3) 생년월일 (가장 오래된 날짜 찾기)
    earliest_birth_date = extract_earliest_birth_date(text)
    if earliest_birth_date:
        result["토스_생년월일"].append(earliest_birth_date)

    return result

# # ✅ 입력 및 출력 파일 경로
# input_file = "./toss_input.xlsx"
# output_file = "./test_toss_output.xlsx"

# # ✅ 엑셀 파일 읽기
# df = pd.read_excel(input_file)

# # ✅ 결과를 저장할 데이터프레임 생성 (출력 컬럼 맞추기)
# output_columns = ["토스_수험번호", "토스_발급번호", "토스_생년월일"]
# results_df = pd.DataFrame(columns=output_columns)

# # ✅ 첫 번째 행(컬럼명) 제외, 각 행별 OCR 추출
# for index, row in df.iterrows():
#     file_name = row['파일명']
    
#     text = row["ocr_text"]
#     name = 1
#     # ✅ 토스 추출 함수 실행
#     extracted_data = extract_info_from_toss(name, text)

#     # ✅ 결과 데이터프레임에 추가
#     new_row = pd.DataFrame({
#         "파일명": file_name,
#         "토스_수험번호": [", ".join(extracted_data["토스_수험번호"]) if extracted_data["토스_수험번호"] else ""],
#         "토스_발급번호": [", ".join(extracted_data["토스_발급번호"]) if extracted_data["토스_발급번호"] else ""],
#         "토스_생년월일": [", ".join(extracted_data["토스_생년월일"]) if extracted_data["토스_생년월일"] else ""]
#     })

#     results_df = pd.concat([results_df, new_row], ignore_index=True)
#     # ✅ 파일명을 숫자로 변환 후 정렬 (숫자로 변환 불가능한 경우 원래 순서 유지)


# # ✅ 결과 엑셀 파일 저장
# results_df.to_excel(output_file, index=False)

# print(f"✅ 토스 추출 테스트 완료! 결과가 {output_file}에 저장되었습니다.")
