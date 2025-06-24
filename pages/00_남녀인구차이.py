import streamlit as st
import pandas as pd

def app():
    st.title("행정구역별 남녀 인구 비율 시각화 (2025년 5월 기준)")

    # 데이터 불러오기
    df = pd.read_csv('202505_202505_연령별인구현황_월간 (1).csv', encoding='cp949')

    # 행정구역 이름 정제
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 쉼표 제거 및 정수형 변환
    df['2025년05월_남_총인구수'] = df['2025년05월_남_총인구수'].str.replace(',', '', regex=False).astype(int)
    df['2025년05월_여_총인구수'] = df['2025년05월_여_총인구수'].str.replace(',', '', regex=False).astype(int)

    # 행정구역 선택
    행정구역_목록 = sorted(df['행정구역'].unique())
    선택_행정구역 = st.selectbox("행정구역을 선택하세요:", 행정구역_목록)

    # 선택한 행정구역의 남녀 인구 합산
    선택_데이터 = df[df['행정구역'] == 선택_행정구역]
    남자_합 = 선택_데이터['2025년05월_남_총인구수'].sum()
    여자_합 = 선택_데이터['2025년05월_여_총인구수'].sum()
    전체_합 = 남자_합 + 여자_합

    # 비율 계산
    남자_비율 = round(남자_합 / 전체_합 * 100, 1)
    여자_비율 = round(여자_합 / 전체_합 * 100, 1)

    # 비율 시각화용 데이터
    df_성별 = pd.DataFrame({
        '성별': ['남자', '여자'],
        '비율': [남자_비율, 여자_비율]
    }).set_index('성별')

    # 성별 비율 표시
    st.subheader(f"📊 {선택_행정구역}의 남녀 인구 비율")
    st.bar_chart(df_성별)

    # 숫자 및 설명 출력
    st.metric(label="남자 인구 비율", value=f"{남자_비율}%")
    st.metric(label="여자 인구 비율", value=f"{여자_비율}%")

    if 남자_합 > 여자_합:
        st.success(f"💡 {선택_행정구역}에서는 남성이 {남자_합 - 여자_합:,}명 더 많습니다.")
    elif 여자_합 > 남자_합:
        st.info(f"💡 {선택_행정구역}에서는 여성이 {여자_합 - 남자_합:,}명 더 많습니다.")
    else:
        st.warning(f"⚖️ 남녀 인구수가 같습니다.")

if __name__ == '__main__':
    app()
