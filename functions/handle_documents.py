from functions.extractors.extract_dungbon import extract_info_from_dungbon
from functions.extractors.extract_chobon import extract_info_from_chobon
from functions.extractors.extract_health_insurance import extract_info_from_health_insurance
from functions.extractors.extract_national_pension import extract_info_from_national_pension
from functions.extractors.extract_toeic import extract_info_from_toeic
from functions.extractors.extract_toss import extract_info_from_toss
from functions.extractors.extract_transcript import extract_info_from_transcript
from functions.extractors.extract_graduation import extract_info_from_graduation

def handle_document(doc_type, name, text):
    """
    문서 유형에 따라 필요한 데이터를 추출.
    """
    extractors = {
        "등본": extract_info_from_dungbon,
        "초본": extract_info_from_chobon,
        "건강보험자격득실_건보": extract_info_from_health_insurance,
        "건강보험자격득실_정부24": extract_info_from_health_insurance,
        "국민연금가입자증명_국민연금": extract_info_from_national_pension,
        "국민연금가입자증명_정부24": extract_info_from_national_pension,
        "토익": extract_info_from_toeic,
        "토스": extract_info_from_toss,
        "성적증명서": extract_info_from_transcript,
        "졸업증명서":extract_info_from_graduation,
    }

    # 문서 유형이 정의된 경우 해당 함수 실행, 없으면 빈 딕셔너리 반환
    return extractors.get(doc_type, lambda n, t: {})(name, text)
