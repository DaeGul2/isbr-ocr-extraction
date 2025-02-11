import os
import pandas as pd
import time
import requests
import json

# ✅ NAVER CLOVA OCR 설정
CLOVA_OCR_URL = "https://2khcjstlni.apigw.ntruss.com/custom/v1/38372/c0900a14255a3a2be14c0ee063c3c5536a71f856761a130c6e6f30c9ec93c899/general"
CLOVA_SECRET_KEY = "a0h2R1p3TFJOWUxqWXl3VGJLcFVsc3F1UmpJYkdtalU="  # 사용자 제공 API 키

# ✅ 이미지 파일 목록을 가져오는 경로
image_folder_path = './테스트_이미지'
image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]

# ✅ 결과를 저장할 데이터프레임 생성
results_df = pd.DataFrame(columns=['파일명', 'text'])

# ✅ NAVER CLOVA OCR 요청 함수
def call_clova_ocr(image_path):
    headers = {
        "X-OCR-SECRET": CLOVA_SECRET_KEY
    }

    payload = {
        "version": "V2",
        "requestId": str(int(time.time() * 1000)),
        "timestamp": int(time.time() * 1000),
        "images": [{"format": "jpg", "name": "ocr_image"}]
    }

    # 이미지 파일 크기 확인 (10MB 제한)
    if os.path.getsize(image_path) > 10 * 1024 * 1024:
        print(f"⚠️ 파일 크기 초과 (10MB 제한): {image_path}")
        return ""

    # 이미지 파일 업로드
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        data = {"message": json.dumps(payload)}  # ⚠️ json 대신 data로 전송

        try:
            response = requests.post(CLOVA_OCR_URL, headers=headers, data=data, files=files, timeout=15)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

            result = response.json()
            extracted_text = []

            # OCR 결과에서 텍스트 추출
            for image in result.get("images", []):
                if "fields" in image:
                    for field in image["fields"]:
                        extracted_text.append(field["inferText"])

            return "\n".join(extracted_text)

        except requests.exceptions.Timeout:
            print(f"⏳ 요청 시간 초과 (파일: {image_path})")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"❌ CLOVA OCR 요청 실패 (파일: {image_path}, 오류: {e})")
            return ""

# ✅ 각 이미지 파일에 대한 OCR 처리
for image_file in image_files:
    image_path = os.path.join(image_folder_path, image_file)
    extracted_text = call_clova_ocr(image_path)

    # OCR 결과를 데이터프레임에 추가
    new_row = pd.DataFrame({'파일명': [image_file], 'text': [extracted_text]})
    results_df = pd.concat([results_df, new_row], ignore_index=True)

# ✅ 결과 데이터프레임을 엑셀 파일로 저장
os.makedirs('./전처리텍스트_naver', exist_ok=True)
results_df.to_excel('./전처리텍스트_naver/preprocessed_output.xlsx', index=False)

print("✅ OCR 처리 완료 및 엑셀 저장 완료!")
