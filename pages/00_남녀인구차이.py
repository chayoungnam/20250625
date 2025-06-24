import streamlit as st
import pandas as pd

def app():
    st.title("행정구역별 남녀 인구 차이 시각화 (2025년 5월 기준)")

    # 데이터 불러오기
    df = pd.read_csv('202505_202505_연령별인구현황_월간 (1).csv', encoding='cp949')

    # 행정구역 이름 전처리
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 쉼표 제거 및 정수형 변환
    df['2025년05월_남_총인구수'] = df['2025년05월_남_총인구수'].str.replace(',', '', regex=False).astype(int)
    df['2025년05월_여_총인구수'] = df['2025년05월_여_총인구수'].str.replace(',', '', regex=False).astype(int)

    # 행정구역 선택
    행정구역_목록 = df['행정구역'].unique()
    선택_행정구역 = st.selectbox("행정구역을 선택하세요:", sorted(행정구역_목록))

    # 선택된 행정구역의 남녀 인구
    선택_데이터 = df[df['행정구역'] == 선택_행정구역]
    남자_인구 = 선택_데이터['2025년05월_남_총인구수'].sum()
    여자_인구 = 선택_데이터['2025년05월_여_총인구수'].sum()

    # 데이터프레임 생성 (Streamlit bar_chart 전용)
    성별_데이터 = pd.DataFrame({
        '성별': ['남자', '여자'],
        '인구수': [남자_인구, 여자_인구]
    }).set_index('성별')

    # 시각화
    st.subheader(f"📊 {선택_행정구역}의 남녀 인구 비교")
    st.bar_chart(성별_데이터)

    # 추가 정보 표시
    차이 = abs(남자_인구 - 여자_인구)
    더_많은_성별 = '남자' if 남자_인구 > 여자_인구 else '여자'
    st.write(f"💡 {선택_행정구역}에서는 **{더_많은_성별}** 인구가 **{차이:,}명** 더 많습니다.")

if __name__ == '__main__':
    app()
