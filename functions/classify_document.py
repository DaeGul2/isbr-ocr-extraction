def classify_document(text):
    """
    주어진 텍스트가 어떤 문서 유형에 속하는지 분류.
    """
    text = text.lower()
    # 등본의 특징적인 단어
    
    
    if "주민등록표" in text:
        if "등본" in text or "세대별주민" in text:
            return "등본"
        else:
            return "초본"

    # 추가적으로 세대주변경이 많으면 초본으로 판단
   
    if "건강보험자격득실" in text:
        return "건강보험자격득실_건보" if ("발급번호" in text or "확인청구" in text) else "건강보험자격득실_정부24"
    if "국민연금가입자" in text:
        return "국민연금가입자증명_국민연금" if "발급" in text else "국민연금가입자증명_정부24"
    if "toeic" in text: 
        if "speaking" in text:
            return "토스"
        else:
            return "토익"
    if "성적" in text and ("학점" in text or "문서확인번호" in text or "transcript" in text):
        return "성적증명서"
    if "졸업" in text :
        return "졸업증명서"
    return None
