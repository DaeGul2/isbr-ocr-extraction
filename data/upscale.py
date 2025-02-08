import cv2
import os
import numpy as np

input_directory = './테스트_이미지'
output_directory = './upscaled'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

image_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
scale_factor = 2

for image_file in image_files:
    file_path = os.path.join(input_directory, image_file)
    print(f"Trying to load image from {file_path}")

    # 이미지 파일을 바이트로 직접 읽기
    with open(file_path, 'rb') as file:
        byte_stream = bytearray(file.read())
        numpy_array = np.asarray(byte_stream, dtype=np.uint8)
        image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    if image is not None:
        upscaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        output_path = os.path.join(output_directory, image_file)
        cv2.imwrite(output_path, upscaled_image)
        print(f"Successfully processed and saved: {output_path}")
    else:
        print(f"Failed to load image {image_file}. Possible causes: invalid image format, corrupted file, or unsupported format.")
