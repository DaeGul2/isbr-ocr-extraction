def classify_document(text):
    """
    주어진 텍스트가 어떤 문서 유형에 속하는지 분류.
    """
    if "주민등록표" in text:
        return "등본" if "초본" not in text else "초본"
    if "건강보험자격득실 확인서" in text:
        return "건강보험자격득실_건보" if "G" in text else "건강보험자격득실_정부24"
    if "국민연금가입자증명서" in text:
        return "국민연금가입자증명_국민연금" if "국민연금" in text else "국민연금가입자증명_정부24"
    if "TOEIC" in text or "TEST TAKER" in text:
        return "토익"
    if "TOEFL" in text or "SPEAKING" in text:
        return "토스"
    if "성적증명서" in text or "Transcript" in text:
        return "성적증명서"
    return None
