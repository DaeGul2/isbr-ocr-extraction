from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

# Azure Computer Vision (OCR) 설정
ocr_endpoint = "https://ocr-document-analysis.cognitiveservices.azure.com/"
ocr_key = "9RGXZTh9OrHBobvULRZmRrnkIrkHN8FpIz4K3eOPvOlZdeFefno9JQQJ99ALACNns7RXJ3w3AAAFACOGe6yO"
ocr_client = ComputerVisionClient(ocr_endpoint, CognitiveServicesCredentials(ocr_key))

# OCR을 실행할 이미지 파일의 경로
image_path = './테스트_이미지/토스.png'  # 'sample_image.jpg'를 원하는 파일명으로 교체하세요.

# 이미지 파일을 열고 OCR 실행
with open(image_path, "rb") as image_stream:
    ocr_results = ocr_client.recognize_printed_text_in_stream(image=image_stream)
    text_outputs = []

    # OCR 결과에서 텍스트 추출
    for region in ocr_results.regions:
        for line in region.lines:
            line_text = ' '.join([word.text for word in line.words])
            text_outputs.append(line_text)

    full_text = '\n'.join(text_outputs)

# 추출된 텍스트 출력
print(full_text.lower())
