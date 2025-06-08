import streamlit as st

# 넓은 컨테이너 스타일 적용
st.markdown("""
<style>
    .main .block-container {
        max-width: 95%;
        padding-left: 2rem;
        padding-right: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# 메인 컨테이너
with st.container():
    # 제목
    st.title("🗺️ 위치 기반 민원 접수 시스템")
    st.markdown("---")
    
    # 시스템 소개
    st.header("📌 시스템 소개")
    st.markdown("""
    <div style='font-size: 18px; line-height: 1.8; margin: 20px 0; max-width: 100%; padding: 0 20px;'>
    이 웹앱은 지도 위에서 직접 위치를 클릭하여 민원을 등록하고 관리할 수 있는 시스템입니다.<br><br>
    누구나 클릭 한 번으로 위치 기반 민원을 작성할 수 있으며, 민원 내용은 실시간으로 Google Sheets에 저장됩니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 주요 기능
    st.header("✅ 주요 기능")
    st.markdown("""
    <div style='font-size: 16px; line-height: 1.6; margin: 15px 0; max-width: 100%; padding: 0 20px;'>
    🗺️ <strong>지도를 클릭하여 민원 위치 등록</strong><br><br>
    ✍️ <strong>작성자, 내용, 날짜 입력</strong> (기본값: 오늘 날짜)<br><br>
    📍 <strong>등록된 민원들을 지도에 시각화</strong><br><br>
    🔍 <strong>작성자 이름으로 민원 검색</strong><br><br>
    📈 <strong>날짜별 민원 수 통계 시각화</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 활용 예시
    st.header("📊 활용 예시")
    st.markdown("""
    <div style='font-size: 16px; line-height: 1.6; margin: 15px 0; max-width: 100%; padding: 0 20px;'>
    • <strong>동네 문제 제보</strong> (가로등 고장, 도로 파손 등)<br><br>
    • <strong>건의 사항 접수</strong><br><br>
    • <strong>특정 지역의 문제점 시각화</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 데이터 저장
    st.header("💾 데이터 저장")
    st.markdown("""
    <div style='font-size: 16px; line-height: 1.6; margin: 15px 0; max-width: 100%; padding: 0 20px;'>
    모든 민원 데이터는 <strong>Google Sheets에 자동 저장</strong>되어 체계적으로 관리됩니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 하단 안내
    st.markdown("---")
    st.success("👈 좌측 사이드바에서 원하는 기능을 선택하여 민원 접수 시스템을 이용해보세요!")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 작성자 정보
    st.header("👨‍💻 작성자 정보")
    
    # 개발자 정보를 2칼럼으로 배치
    dev_col1, dev_col2 = st.columns([1, 1])
    
    with dev_col1:
        st.markdown("""
        <div style='font-size: 16px; line-height: 1.4; margin: 10px 0 0 0; max-width: 100%; padding: 15px; background-color: rgba(128, 128, 128, 0.1); border-radius: 10px;'>
        <strong>🧑‍💻 개발자 1:</strong> 정태현<br>
        <strong>📧 이메일:</strong> taehyunj05@yonsei.ac.kr
        </div>
        """, unsafe_allow_html=True)
    
    with dev_col2:
        st.markdown("""
        <div style='font-size: 16px; line-height: 1.4; margin: 10px 0 0 0; max-width: 100%; padding: 15px; background-color: rgba(128, 128, 128, 0.1); border-radius: 10px;'>
        <strong>🧑‍💻 개발자 2:</strong> 김종호<br>
        <strong>📧 이메일:</strong> bostondkd@yonsei.ac.kr
        </div>
        """, unsafe_allow_html=True)
    
    # 프로젝트 공통 정보
    st.markdown("""
    <div style='font-size: 16px; line-height: 1.4; margin: 15px 0 0 0; max-width: 100%; padding: 20px; background-color: rgba(100, 149, 237, 0.1); border-radius: 10px;'>
    <strong>💬 문의사항이나 개선사항이 있으시면 언제든 연락주세요!</strong>
    </div>
    """, unsafe_allow_html=True)