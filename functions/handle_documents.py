def handle_document(doc_type, name, text):
    """
    문서 유형에 따라 필요한 데이터를 추출.
    """
    result = {
        "등본_자격번호": [], "등본_발급날짜": [], "초본_자격번호": [], "초본_발급날짜": [],
        "건강보험자격득실_번호_건보": [], "건강보험자격득실_번호_정부24": [], 
        "국민연금가입자증명_번호_국민연금": [], "국민연금가입자증명_번호_정부24": [],
        "토익_수험번호": [], "토익_발급번호": [], "토스_수험번호": [], "토스_발급번호": [],
        "성적증명_문서확인번호": [], "성적증명_추정발급일": [], "대학교": []
    }

    if doc_type == "등본":
        # 등본 관련 정보 추출 (예: 정규표현식으로 4-4-4-4 형식 찾기)
        pass  
    elif doc_type == "초본":
        pass  
    elif doc_type == "건강보험자격득실_건보":
        pass  
    elif doc_type == "건강보험자격득실_정부24":
        pass  
    elif doc_type == "국민연금가입자증명_국민연금":
        pass  
    elif doc_type == "국민연금가입자증명_정부24":
        pass  
    elif doc_type == "토익":
        pass  
    elif doc_type == "토스":
        pass  
    elif doc_type == "성적증명서":
        pass  

    return result
