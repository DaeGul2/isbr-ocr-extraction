import pandas as pd
import os
from functions.parse_text import parse_ocr_text
from functions.classify_document import classify_document
from functions.handle_documents import handle_document
from functions.expand_results import expand_results

# 🔹 [1] Input 데이터 로드
input_path = "./data/input.xlsx"
df_input = pd.read_excel(input_path)

# 🔹 [2] Output 데이터 프레임 초기화
output_columns = [
    "수험번호", "이름", "생년월일6자리_등본", "등본_확인번호", "등본_발급날짜", "초본_확인인번호", "초본_발급날짜","생년월일6자리_초본",
    "건강보험자격득실_확인번호_건보", "건강보험자격득실_확인번호_정부24", "국민연금가입자증명_확인번호_국민연금",
    "국민연금가입자증명_확인인번호_정부24", "토익_수험번호", "토익_발급번호", "토스_수험번호", "토스_발급번호",
    "성적증명_문서확인번호", "성적증명_추정발급일", "대학교","졸업증명서_확인번호"
]
df_output = pd.DataFrame(columns=output_columns)

# 🔹 [3] 각 행을 순회하며 OCR 데이터 처리
for _, row in df_input.iterrows():
    exam_number, name, ocr_text = row["수험번호"], row["이름"], row["ocr_text"]

    # 개행 및 공백 제거 후 파싱. output : 배열(개행 및 공백이 제거된 각 페이지 OCR결과과)
    parsed_text = parse_ocr_text(ocr_text) 

    # 결과 저장을 위한 딕셔너리 (배열 형태)
    final_result = {col: [] for col in output_columns}
    final_result["수험번호"].append(exam_number)
    final_result["이름"].append(name)

    # 🔹 [4] OCR 텍스트 순회하며 파일 분류 및 데이터 추출
    for t in parsed_text:
      
        doc_type = classify_document(t)  # 문서 유형 분류
        print("doc_type : ",row['이름'],":", doc_type)
        if doc_type:
            result = handle_document(doc_type, name, t)  # 해당 문서 처리
            for key, value in result.items():
                final_result[key].extend(value)  # 결과 병합

    # 🔹 [5] 결과를 행 단위로 확장 후 저장
    expanded_rows = expand_results(final_result)
    df_output = pd.concat([df_output, expanded_rows], ignore_index=True)

# 🔹 [6] 최종 output 저장
output_path = "./data/output2.xlsx"
df_output.to_excel(output_path, index=False)
print("✅ 최종 데이터 저장 완료!")
