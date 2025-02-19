import os
import re
import pandas as pd

# ✅ 최신 발급 날짜 찾기 함수
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

# ✅ 국민연금가입자증명 정보 추출 함수
def extract_info_from_nps(name, text):
    """
    국민연금가입자증명에서 필요한 정보 (확인번호_국민연금, 확인번호_정부24, 발급일) 추출
    """
    result = {
      
        "국민연금가입자증명_확인번호_국민연금": [],
        "국민연금가입자증명_확인번호_정부24": [],
        "국민연금가입자증명_발급일": []
    }

    text = text.lower().replace("--", "-")  # 텍스트 정제
    text = text.replace("+","H")
    # 🔹 정부24 확인번호 (G + 15자리 숫자)
    pattern_gov24 = r"\d{4}-\d{4}-\d{4}-\d{4}"
    match_gov24 = re.findall(pattern_gov24, text)
    if match_gov24:
        result["국민연금가입자증명_확인번호_정부24"].append(match_gov24[0])  # 첫 번째 값만 저장

    
    # 🔹 국민연금 확인번호 (4-4-4-4 형식)
    pattern_yeongum = r"[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{6}"
    match_yeongum = re.findall(pattern_yeongum, text)
    if match_yeongum:
        result["국민연금가입자증명_확인번호_국민연금"].append(match_yeongum[0].upper())  # 첫 번째 값만 저장

    # 🔹 발급 날짜 (가장 최신 날짜만 저장)
    latest_issue_date = extract_latest_issue_date(text)
    if latest_issue_date:
        result["국민연금가입자증명_발급일"].append(latest_issue_date)

    return result

# # ✅ 입력 및 출력 파일 경로
# input_file = "./nps_input.xlsx"
# output_file = "./test_nps_output.xlsx"

# # ✅ 엑셀 파일 읽기
# df = pd.read_excel(input_file)

# # ✅ 결과를 저장할 데이터프레임 생성 (출력 컬럼 맞추기)
# output_columns = [ "국민연금가입자증명_확인번호_국민연금", "국민연금가입자증명_확인번호_정부24", "국민연금가입자증명_발급일"]
# results_df = pd.DataFrame(columns=output_columns)

# # ✅ 첫 번째 행(컬럼명) 제외, 각 행별 OCR 추출
# for index, row in df.iterrows():
#     file_name = row["파일명"].split(".")[0]  # 확장자 제거
#     text = row["ocr_text"]

#     # ✅ 국민연금가입자증명 추출 함수 실행
#     extracted_data = extract_info_from_nps(file_name, text)

#     # ✅ 결과 데이터프레임에 추가
#     new_row = pd.DataFrame({
#         "파일명": file_name,
#         "국민연금가입자증명_확인번호_국민연금": [", ".join(extracted_data["국민연금가입자증명_확인번호_국민연금"]) if extracted_data["국민연금가입자증명_확인번호_국민연금"] else ""],
#         "국민연금가입자증명_확인번호_정부24": [", ".join(extracted_data["국민연금가입자증명_확인번호_정부24"]) if extracted_data["국민연금가입자증명_확인번호_정부24"] else ""],
#         "국민연금가입자증명_발급일": [", ".join(extracted_data["국민연금가입자증명_발급일"]) if extracted_data["국민연금가입자증명_발급일"] else ""]
#     })

#     results_df = pd.concat([results_df, new_row], ignore_index=True)

# # ✅ 결과 엑셀 파일 저장
# results_df.to_excel(output_file, index=False)

# print(f"✅ 국민연금가입자증명 추출 테스트 완료! 결과가 {output_file}에 저장되었습니다.")
                  