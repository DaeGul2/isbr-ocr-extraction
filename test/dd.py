import pandas as pd

# 엑셀 파일 읽기
input_file = "./input.xlsx"
df = pd.read_excel(input_file)

# '학교명' 컬럼에서 'XX대학'까지 찾기 (앞에 공백 허용)
df['학교명'] = df['학교명'].str.extract(r'([\S\s]*대학)')

# '대학' -> '대' 변환
df['학교명'] = df['학교명'].str.replace('대학$', '대', regex=True)

# 공백 제거 (문자열 내 모든 공백 제거)
df['학교명'] = df['학교명'].str.replace(' ', '', regex=True)

# NaN 값 제거
df = df.dropna(subset=['학교명'])

# 새로운 파일로 저장
output_file = "./university_list.xlsx"
df[['학교명']].to_excel(output_file, index=False)

print(f"변환 완료: {output_file}")
