import os
import cv2
import numpy as np

# ✅ OpenCV 기반 전처리 함수: 노이즈 제거 + 적당한 선명화
def preprocess_image(image_path, save_path):
    """
    주어진 이미지 파일을 OpenCV를 사용해 노이즈 제거(Gaussian Blur) + 적당한 선명화 후 저장합니다.
    """
    try:
        # 이미지 불러오기 (그레이스케일 변환)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 이미지가 정상적으로 로드되었는지 확인
        if img is None:
            raise Exception(f"❌ 이미지 로드 실패: {image_path}")

        # 1️⃣ 노이즈 제거 (Gaussian Blur)
        img_denoised = cv2.GaussianBlur(img, (3, 3), 0)  # (5,5)보다 약한 블러 적용

        # 2️⃣ 적당한 선명화 (Soft Sharpening)
        sharpen_filter = np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]])  # 기존보다 약한 선명화 필터
        img_sharpen = cv2.filter2D(img_denoised, -1, sharpen_filter)

        # 전처리된 이미지 저장
        cv2.imwrite(save_path, img_sharpen)
        print(f"✅ 전처리 완료: {save_path}")

    except Exception as e:
        print(f"❌ 이미지 전처리 실패 ({image_path}): {e}")

# ✅ 폴더 내 모든 이미지 전처리 함수
def process_images_in_folder(input_folder, output_folder):
    """
    특정 폴더 내 모든 이미지 파일을 전처리한 후, 결과 폴더에 저장합니다.
    """
    # 출력 폴더 생성 (없으면 자동 생성)
    os.makedirs(output_folder, exist_ok=True)

    # 지원하는 이미지 확장자 목록
    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    # 입력 폴더 내 모든 파일 확인
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # 폴더가 아니라 파일만 처리 & 이미지 파일만 선택
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in valid_extensions:
            # 출력 파일 경로 설정
            output_path = os.path.join(output_folder, filename)
            preprocess_image(file_path, output_path)

# ✅ 실행 예시
if __name__ == "__main__":
    input_folder = "./test_images"  # 원본 이미지 폴더
    output_folder = "./processed_images_denoised_sharpened"  # 전처리된 이미지 저장 폴더

    process_images_in_folder(input_folder, output_folder)
