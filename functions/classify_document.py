def classify_document(text):
    """
    주어진 텍스트가 어떤 문서 유형에 속하는지 분류.
    """
    text = text.lower()


    # 등본의 특징적인 단어    
    if "주민등록표" in text:
        if "이등본" in text :
            return "등본"
        elif "이초본" in text:
            return "초본"
        elif "세대별" in text :
            return "등본"
        else:
            return "초본"

    # 추가적으로 세대주변경이 많으면 초본으로 판단
   
    if "강보험자격득" in text:
        return "건강보험자격득실"


    if "국민연금가입자" in text :
        return "국민연금가입자증명"
    

    if "toeic" in text: 
        if "성적" in text and ("학점" in text or "문서확인번호" in text or "transcript" in text):
            return "성적증명서"
        if "peakin" in text:
            return "토스"
        else:
            return "토익"
        

    if "성적" in text and ("학점" in text or "문서확인번호" in text or "transcript" in text):
        return "성적증명서"
    

    if "졸업" in text or "학위수여" in text:
        return "졸업증명서"
    
    
    return None
