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

# ✅ 성적증명서 문서확인번호 추출 함수
def extract_info_from_grade(name, text):
    """
    성적증명서에서 문서확인번호와 발급일을 추출
    """
    result = {
        "성적증명_문서확인번호": [],
        "성적증명_추정발급일": []
    }

    # 🔹 'internet' 포함 여부는 소문자로 변환해서 체크
    check_text = text.lower()

    # 🔹 'internet'이 포함되면 No) 숫자 패턴 찾기 (원본 text 사용)
    if "internet" in check_text:
        pattern_no = r"(?:No\)|no\)|nO\)|NO\))\s*(\d+)"
        match_no = re.findall(pattern_no, text)  # 원본 text에서 찾기
        if match_no:
            if len(match_no)>1:
                result["성적증명_문서확인번호"].append(match_no[-1])
            else:
                result["성적증명_문서확인번호"].extend(match_no)
    
    else:
        # 🔹 '원본확인번호'가 있으면 4-5-4-5 패턴 찾기
        if "원본확인번호" in text:
            pattern_4x5 = r"[A-Za-z0-9]{4}-[A-Za-z0-9]{5}-[A-Za-z0-9]{4}-[A-Za-z0-9]{5}"
            match_4x5 = re.findall(pattern_4x5, text)
            
            # o/O를 0으로 변환
            match_4x5 = [m.replace('o', '0').replace('O', '0') for m in match_4x5]
            
            if match_4x5:
                if len(match_4x5)>1:
                    result["성적증명_문서확인번호"].append(match_4x5[0])
                else:
                    result["성적증명_문서확인번호"].extend(match_4x5)
        
        # 🔹 '원본확인번호'가 없으면 기존 4-4-4-4 패턴 찾기
        else:
            pattern_4x4 = r"[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}"
            match_4x4 = re.findall(pattern_4x4, text)
            
            # o/O를 0으로 변환
            match_4x4 = [m.replace('o', '0').replace('O', '0') for m in match_4x4]
            
            if match_4x4:
                if len(match_4x4) > 1:
                    result["성적증명_문서확인번호"].append(match_4x4[0])
                else:
                    result["성적증명_문서확인번호"].extend(match_4x4)

    # 🔹 발급 날짜 찾기 (가장 최근 날짜만 저장)
    latest_issue_date = extract_latest_issue_date(text)
    if latest_issue_date:
        result["성적증명_추정발급일"].append(latest_issue_date)

    return result


# ✅ 입력 및 출력 파일 경로
input_file = "./grade_input.xlsx"
output_file = "./test_grade_output.xlsx"

# ✅ 엑셀 파일 읽기
df = pd.read_excel(input_file)

# ✅ 결과를 저장할 데이터프레임 생성 (출력 컬럼 맞추기)
output_columns = ["파일명", "성적증명_문서확인번호", "성적증명_추정발급일"]
results_df = pd.DataFrame(columns=output_columns)

# ✅ 첫 번째 행(컬럼명) 제외, 각 행별 OCR 추출
for index, row in df.iterrows():
    filename = row["파일명"]
    text = row["ocr_text"]

    # 🔹 파일명에서 확장자 제거
    filename = os.path.splitext(filename)[0]

    # ✅ 성적증명서 추출 함수 실행
    extracted_data = extract_info_from_grade(None, text)

    # ✅ 결과 데이터프레임에 추가
    new_row = pd.DataFrame({
        "파일명": [filename],
        "성적증명_문서확인번호": [", ".join(extracted_data["성적증명_문서확인번호"]) if extracted_data["성적증명_문서확인번호"] else ""],
        "성적증명_추정발급일": [", ".join(extracted_data["성적증명_추정발급일"]) if extracted_data["성적증명_추정발급일"] else ""]
    })

    results_df = pd.concat([results_df, new_row], ignore_index=True)

# ✅ 파일명을 숫자로 변환 후 정렬 (숫자로 변환 불가능한 경우 원래 순서 유지)
results_df["파일명"] = pd.to_numeric(results_df["파일명"], errors='coerce')
results_df = results_df.sort_values(by="파일명", ascending=True, na_position='last')
results_df["파일명"] = results_df["파일명"].astype(str)  # 다시 문자열로 변환

# ✅ 결과 엑셀 파일 저장
results_df.to_excel(output_file, index=False)

print(f"✅ 성적증명서 추출 테스트 완료! 결과가 {output_file}에 저장되었습니다.")
