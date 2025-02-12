import pandas as pd

# 엑셀 파일 읽기
input_file = "./input.xlsx"
df = pd.read_excel(input_file)

# '학교명' 컬럼에서 'XX대' 추출 (예: '서울대학교 컴퓨터공학과' -> '서울대')
df['학교명'] = df['학교명'].str.extract(r'(\S*대)')

# 새로운 파일로 저장
output_file = "./university_list.xlsx"
df[['학교명']].to_excel(output_file, index=False)

print(f"변환 완료: {output_file}")
