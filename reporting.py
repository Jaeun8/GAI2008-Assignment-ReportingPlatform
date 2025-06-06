import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import date

st.markdown("""
<style>
    .main .block-container {
        max-width: 100%;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title('📝 민원 등록하기')

if "marker_location" not in st.session_state:
    st.session_state.marker_location = [37.564375, 126.938871]
    st.session_state.zoom = 16

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 위치 선택")
    
    m = folium.Map(
        location=st.session_state.marker_location, 
        zoom_start=st.session_state.zoom,
        tiles='OpenStreetMap'
    )

    map_data = st_folium(
        m, 
        width="100%", 
        height=500,
        key="folium_map",
        returned_objects=["last_object_clicked", "last_clicked", "last_object_dragged"]
    )

with col2:
    st.subheader("📝 민원 정보 입력")
    
    lat, lng = st.session_state.marker_location
    st.info(f"**선택된 위치**\n위도: {lat:.6f}\n경도: {lng:.6f}")
    
    with st.form("complaint_form"):
        name = st.text_input("민원 작성자 *", placeholder="이름을 입력하세요")
        
        complaint_type = st.selectbox(
            "민원 유형 *",
            ["도로/교통", "환경/위생", "안전", "시설물", "기타"]
        )
        
        content = st.text_area("민원 내용 *", placeholder="민원 내용을 입력하세요")
        
        report_date = st.date_input("작성 날짜", value=st.session_state.get('report_date', None))
        
        submit_button = st.form_submit_button("민원 신청 하기")
        
        if submit_button:
            if name and content:
                st.success("✅ 민원이 정상적으로 접수되었습니다!")
                
                st.markdown("### 📋 접수 정보")
                st.write(f"**위치:** {lat:.6f}, {lng:.6f}")
                st.write(f"**작성자:** {name}")
                st.write(f"**유형:** {complaint_type}")
                st.write(f"**내용:** {content}")
                st.write(f"**작성일:** {report_date}")
                
                import random
                receipt_number = f"CR{date.today().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
                st.write(f"**접수번호:** {receipt_number}")
            
            else:
                st.error("❌ 필수 항목을 모두 입력해주세요!")

if map_data.get("last_clicked"):
    lat, lng = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
    st.session_state.marker_location = [lat, lng]  # Update session state with new marker location
    # Redraw the map immediately with the new marker location
    m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
    folium.Marker(
        location=st.session_state.marker_location,
        draggable=False
    ).add_to(m)
    map = st_folium(m, width=620, height=580, key="folium_map")