from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageEnhance
import os

# ✅ Azure OCR 설정
ocr_endpoint = "https://ocr-document-analysis.cognitiveservices.azure.com/"
ocr_key = "9RGXZTh9OrHBobvULRZmRrnkIrkHN8FpIz4K3eOPvOlZdeFefno9JQQJ99ALACNns7RXJ3w3AAAFACOGe6yO"
ocr_client = ComputerVisionClient(ocr_endpoint, CognitiveServicesCredentials(ocr_key))

# ✅ OCR을 실행할 이미지 파일의 경로
image_path = "./테스트_이미지/건강보험자격득실_건보.png"

# ✅ 전처리된 이미지 저장 경로
processed_image_path = "./테스트_이미지/processed_건강보험자격득실_건보.png"

# ✅ 밝기 조정 및 선명화 전처리 함수
def preprocess_image(image_path, save_path):
    # 이미지 불러오기
    img = Image.open(image_path)

    # 밝기 조정 (OCR 인식률 향상)
    # img = ImageEnhance.Brightness(img).enhance(1.2)  # 밝기를 20% 증가

    # 선명화 적용 (텍스트를 또렷하게)
    img = ImageEnhance.Sharpness(img).enhance(2.0)  # 선명도를 2배 증가

    # 전처리된 이미지 저장
    img.save(save_path)
    return save_path

# ✅ 이미지 전처리 실행
processed_image_path = preprocess_image(image_path, processed_image_path)

# ✅ Azure OCR 실행 (전처리된 이미지 사용)
with open(processed_image_path, "rb") as image_stream:
    ocr_results = ocr_client.recognize_printed_text_in_stream(image=image_stream)
    text_outputs = []

    # OCR 결과에서 텍스트 추출
    for region in ocr_results.regions:
        for line in region.lines:
            line_text = ' '.join([word.text for word in line.words])
            text_outputs.append(line_text)

    full_text = '\n'.join(text_outputs)

# ✅ 최종 OCR 결과 출력
print(full_text.lower())
