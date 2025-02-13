def parse_ocr_text(ocr_text):
    """
    개행 및 공백을 제거한 후 '|||' 기준으로 텍스트를 분할하여 리스트로 반환.
    """
    if not isinstance(ocr_text, str):
        return []
    
    cleaned_text = ocr_text.replace("\n", "").replace(" ", "")  # 개행 및 공백 제거
    return cleaned_text.split("|||분리|||")  # '|||' 기준으로 분할
