import os
from PIL import Image, ImageEnhance, ImageFilter

# ✅ 전처리 함수: 선명화 + 대비 조정 + 노이즈 제거
def preprocess_image(image_path, save_path):
    """
    주어진 이미지 파일을 대비 및 선명도를 조정한 후 저장합니다.
    """
    try:
        # 이미지 열기 및 흑백 변환 (Grayscale)
        img = Image.open(image_path)


        # 선명화 적용 (텍스트를 또렷하게)
        img = ImageEnhance.Sharpness(img).enhance(2.0)  # 선명도 2배 증가

        

        # 전처리된 이미지 저장
        img.save(save_path)
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
    input_folder = "./테스트_이미지"  # 원본 이미지 폴더
    output_folder = "./processed_images"  # 전처리된 이미지 저장 폴더

    process_images_in_folder(input_folder, output_folder)
