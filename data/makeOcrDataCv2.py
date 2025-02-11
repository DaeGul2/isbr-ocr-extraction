from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import pandas as pd
import time

# Azure Computer Vision (OCR) 설정
ocr_endpoint = "https://ocr-document-analysis.cognitiveservices.azure.com/"
ocr_key = "9RGXZTh9OrHBobvULRZmRrnkIrkHN8FpIz4K3eOPvOlZdeFefno9JQQJ99ALACNns7RXJ3w3AAAFACOGe6yO"
ocr_client = ComputerVisionClient(ocr_endpoint, CognitiveServicesCredentials(ocr_key))

# 이미지 파일 목록을 가져오는 경로
image_folder_path = './processed_images_cv2'
image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]

# 결과를 저장할 데이터프레임 생성
results_df = pd.DataFrame(columns=['파일명', 'text'])

# 각 이미지 파일에 대한 OCR 처리
for image_file in image_files:
    image_path = os.path.join(image_folder_path, image_file)
    with open(image_path, "rb") as image_stream:
        ocr_results = ocr_client.recognize_printed_text_in_stream(image=image_stream)
        text_outputs = []

        # OCR 결과에서 텍스트 추출
        for region in ocr_results.regions:
            for line in region.lines:
                line_text = ' '.join([word.text for word in line.words])
                text_outputs.append(line_text)

        full_text = '\n'.join(text_outputs)
        new_row = pd.DataFrame({'파일명': [image_file], 'text': [full_text]})
        results_df = pd.concat([results_df, new_row], ignore_index=True)

# 결과 데이터프레임을 엑셀 파일로 저장
results_df.to_excel('./전처리텍스트_cv2/preprocessed_output.xlsx', index=False)
