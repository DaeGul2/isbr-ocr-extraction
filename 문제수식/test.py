import win32com.client
import time
import pyautogui

# ✅ 한컴 오피스 실행 (기존 한글이 있으면 그대로 사용)
try:
    hwp = win32com.client.Dispatch("HWPFrame.HwpObject")  # 기존 실행된 한글 가져오기
except:
    hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")  # 새로 실행

hwp.XHwpWindows.Item(0).Visible = True  # 한글 창 보이기

# ✅ 빈 문서가 아닌, 현재 열린 문서 그대로 사용
# ✅ 수식 입력 모드 실행 (Ctrl + F10)
hwp.HAction.Run("EquationCreate")

# ✅ 수식 편집기 로딩 대기 (수식 편집기에 자동으로 커서가 위치함)
time.sleep(1.5)

# 🔹 **현재 활성화된 수식 편집기에 'test' 입력**
pyautogui.write("test")

# ✅ 수식 입력 후 Enter 키로 확정
pyautogui.press("enter")

# ✅ 한글 프로그램 유지 (파일 저장 없이)
print("✅ 수식 편집기에 'test' 입력 완료. 한글이 열린 상태입니다.")
