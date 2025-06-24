import streamlit as st
import pandas as pd

# CSV 파일 로드
file_path = '3a86c372-484b-4405-89c0-4b890a7a8803.csv'
df = pd.read_csv(file_path, encoding='euc-kr')

# 컬럼 이름 전처리
df.columns = [col.replace('2025년05월_계_', '') if col.startswith('2025년05월_계_') else col for col in df.columns]

# 총인구수 컬럼 정수형 변환
df['총인구수'] = df['총인구수'].str.replace(',', '').astype(int)

# 총인구수 상위 5개 행정구역 추출
top5 = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령별 컬럼만 추출
age_columns = [col for col in top5.columns if col.isdigit() or col == '100세 이상']
for col in age_columns:
    top5[col] = top5[col].astype(str).str.replace(',', '').astype(int)

# 연령-행정구역 형태로 전치
age_df = top5[['행정구역'] + age_columns].set_index('행정구역').T

# 스트림릿 UI
st.title("2025년 5월 기준 연령별 인구 현황 분석")
st.subheader("총인구수 기준 상위 5개 행정구역의 연령별 인구 변화")

# 선 그래프 시각화
st.line_chart(age_df)

# 원본 데이터 보기
st.subheader("원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5.reset_index(drop=True))
