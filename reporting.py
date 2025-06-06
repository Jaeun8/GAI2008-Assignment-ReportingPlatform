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

    popup_html = """
    <div style="font-family: Arial, sans-serif; white-space: nowrap; font-size: 14px;">
        <b>민원 위치<br>
    </div>
    """

    folium.Marker(
        location=st.session_state.marker_location,
        popup=folium.Popup(popup_html, max_width=200),
        tooltip="클릭하거나 드래그하여 위치를 변경하세요",
        draggable=True,
        icon=folium.Icon(color='red', icon='exclamation-sign')
    ).add_to(m)
    
    m.add_child(folium.LatLngPopup())

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
        
        content = st.text_area(
            "민원 내용 *", 
            placeholder="민원 내용을 자세히 입력하세요",
            height=150
        )
        
        report_date = st.date_input("작성 날짜", value=date.today())
        
        submit_button = st.form_submit_button("민원 신청하기", use_container_width=True)
        
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

if map_data:
    if map_data.get("last_object_dragged"):
        new_lat = map_data["last_object_dragged"]["lat"]
        new_lng = map_data["last_object_dragged"]["lng"]
        if [new_lat, new_lng] != st.session_state.marker_location:
            st.session_state.marker_location = [new_lat, new_lng]
            st.rerun()
    
    elif map_data.get("last_clicked"):
        new_lat = map_data["last_clicked"]["lat"]
        new_lng = map_data["last_clicked"]["lng"]
        if [new_lat, new_lng] != st.session_state.marker_location:
            st.session_state.marker_location = [new_lat, new_lng]
            st.rerun()

st.markdown("---")
st.markdown("""
### 📖 사용법 안내
1. **위치 선택**: 지도에서 원하는 위치를 클릭하거나 마커를 드래그하여 위치를 설정하세요
2. **정보 입력**: 우측 폼에서 민원 관련 정보를 입력하세요
3. **신청 완료**: '민원 신청하기' 버튼을 클릭하여 민원을 접수하세요
""")

st.markdown("""
<style>
    .stForm {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    .stSuccess {
        padding: 15px;
        border-radius: 5px;
    }
    
    .stInfo {
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)