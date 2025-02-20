
import os
import time
import pandas as pd
import re
import json
import requests

# ✅ NAVER CLOVA OCR 설정
CLOVA_OCR_URL = "https://2khcjstlni.apigw.ntruss.com/custom/v1/38372/c0900a14255a3a2be14c0ee063c3c5536a71f856761a130c6e6f30c9ec93c899/general"
CLOVA_SECRET_KEY = "a0h2R1p3TFJOWUxqWXl3VGJLcFVsc3F1UmpJYkdtalU="  # 사용자 제공 API 키

# 자연 정렬을 위한 키 생성 함수
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# 텍스트 추출 (OCR)
def extract_text_from_image(image_path):
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
    try:
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

                return " ".join(extracted_text)

            except requests.exceptions.Timeout:
                print(f"⏳ 요청 시간 초과 (파일: {image_path})")
                return ""
            except requests.exceptions.RequestException as e:
                print(f"❌ CLOVA OCR 요청 실패 (파일: {image_path}, 오류: {e})")
                return ""
    except Exception as e:
        return f"Error: {e}"

# 최종 실행 코드
if __name__ == "__main__":
    final_data_folder = "./final_data"
    results = []

    if not os.path.exists(final_data_folder):
        print(f"폴더 {final_data_folder}가 존재하지 않습니다.")
        exit()

    folders = [f for f in os.listdir(final_data_folder) if os.path.isdir(os.path.join(final_data_folder, f))]

    for idx, folder in enumerate(folders, start=1):
        folder_path = os.path.join(final_data_folder, folder)
        ocr_text = ""

        files = sorted(os.listdir(folder_path), key=natural_sort_key)  # 자연 정렬 적용

        if not files:
            # 폴더가 비어 있는 경우
            ocr_text = "Error: 폴더가 비어 있습니다."
        else:
            try:
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        file_path = os.path.join(folder_path, file)
                        print(f"Processing file: {file_path}")
                        result_text = extract_text_from_image(file_path)

                        if "Error:" in result_text:
                            ocr_text += result_text + "\n"
                        else:
                            ocr_text += result_text + "|||분리|||"

                ocr_text = ocr_text.strip()

            except Exception as e:
                ocr_text = f"Error: {e}"

        # 결과 저장
        results.append({"연번": idx, "수험번호": folder, "ocrResult": ocr_text})

    # 데이터프레임 생성 및 엑셀 저장
    df = pd.DataFrame(results)
    output_file = "ocr_results.xlsx"
    df.to_excel(output_file, index=False)
    print(f"OCR 결과가 {output_file}에 저장되었습니다.")
