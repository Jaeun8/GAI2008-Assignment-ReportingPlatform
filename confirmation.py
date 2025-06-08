import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

def get_gsheet_connection():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        test_df = conn.read(worksheet="시트1", ttl=0)
        return conn, "시트1"
    except Exception as e1:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            test_df = conn.read(worksheet="Sheet1", ttl=0)
            return conn, "Sheet1"
        except Exception as e2:
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                test_df = conn.read(ttl=0)
                return conn, None
            except Exception as e3:
                st.error(f"구글 시트 연결 오류:\n- 시트1: {str(e1)}\n- Sheet1: {str(e2)}\n- 기본시트: {str(e3)}")
                return None, None
            
def load_complaints():
    conn, worksheet_name = get_gsheet_connection()
    
    if not conn:
        return pd.DataFrame()
    
    try:
        columns = ["접수번호", "위치", "작성자", "유형", "내용", "작성일"]
        
        if worksheet_name:
            df = conn.read(worksheet=worksheet_name, usecols=list(range(len(columns))), ttl=0)
        else:
            df = conn.read(usecols=list(range(len(columns))), ttl=0)
        
        if df.empty or len(df.columns) == 0:
            return pd.DataFrame(columns=columns)
        
        if len(df.columns) >= len(columns):
            df.columns = columns[:len(df.columns)]
        else:
            df = pd.DataFrame(columns=columns)
            
        df = df.dropna(subset=['접수번호'])
        
        return df
        
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {str(e)}")
        return pd.DataFrame()
    
def parse_location(location_str):
    try:
        lat, lng = map(float, location_str.split(', '))
        return lat, lng
    except:
        return None, None
    
st.markdown("""
<style>
    .main .block-container {
        max-width: 100%;
        padding-top: 2.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        padding-bottom: 2.5rem;
    }
    .complaint-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 10px;
    }
    .complaint-header {
        font-weight: bold;
        color: #495057;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title('🔍 민원 조회 시스템')

df = load_complaints()

if df.empty:
    st.warning("⚠️ 조회할 민원 데이터가 없습니다.")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ 민원 위치 지도")
    
    map_data = []
    for idx, row in df.iterrows():
        lat, lng = parse_location(row['위치'])
        if lat is not None and lng is not None:
            map_data.append({
                'lat': lat,
                'lon': lng,
                'receipt_number': row['접수번호'],
                'author': row['작성자'],
                'type': row['유형'],
                'content': row['내용'][:50] + '...' if len(str(row['내용'])) > 50 else row['내용'],
                'date': row['작성일']
            })
    
    if map_data:
        map_df = pd.DataFrame(map_data)
        
        type_colors = {
            '도로/교통': [255, 0, 0, 200],
            '환경/위생': [0, 255, 0, 200],
            '안전': [255, 165, 0, 200],
            '시설물': [0, 0, 255, 200],
            '기타': [128, 0, 128, 200]
        }
        
        map_df['color'] = map_df['type'].apply(lambda x: type_colors.get(x, [128, 128, 128, 200]))
        map_df['height'] = 200

        view_state = pdk.ViewState(
            latitude=map_df['lat'].mean(),
            longitude=map_df['lon'].mean(),
            zoom=13,
            pitch=45,
            bearing=0
        )
        
        layer = pdk.Layer(
            'ColumnLayer',
            data=map_df,
            get_position='[lon, lat]',
            get_fill_color='color',
            get_elevation='height',
            elevation_scale=1,
            radius=50,
            pickable=True,
            auto_highlight=True
        )
        
        tooltip = {
            "html": """
            <b>접수번호:</b> {receipt_number}<br/>
            <b>작성자:</b> {author}<br/>
            <b>유형:</b> {type}<br/>
            <b>내용:</b> {content}<br/>
            <b>작성일:</b> {date}
            """,
            "style": {
                "backgroundColor": "rgba(0,0,0,0.8)",
                "color": "white",
                "fontSize": "12px",
                "padding": "12px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.3)"
            }
        }
        
        deck = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
        )
        
        st.pydeck_chart(deck)
        
        st.markdown("### 🎨 민원 유형별 색상 범례")
        legend_cols = st.columns(5)
        type_colors_display = {
            '도로/교통': '🔴',
            '환경/위생': '🟢', 
            '안전': '🟠',
            '시설물': '🔵',
            '기타': '🟣'
        }
        for idx, (complaint_type, emoji) in enumerate(type_colors_display.items()):
            with legend_cols[idx]:
                count = len(map_df[map_df['type'] == complaint_type])
                st.markdown(f"{emoji} **{complaint_type}**<br/>({count}건)", unsafe_allow_html=True)
        
        st.info(f"📊 총 {len(map_df)}개의 민원이 3D 기둥으로 표시되었습니다. 지도를 드래그하여 각도를 조절할 수 있습니다.")
    else:
        st.warning("⚠️ 지도에 표시할 유효한 위치 데이터가 없습니다.")

with col2:
    st.subheader("👤 작성자별 민원 조회")
    
    with st.expander("🔗 구글 시트 연결 상태", expanded=False):
        conn, worksheet_name = get_gsheet_connection()
        if conn:
            st.success(f"✅ 구글 시트 연결됨")
            if worksheet_name:
                st.info(f"📄 워크시트: {worksheet_name}")
        else:
            st.error("❌ 구글 시트 연결 실패")
    
    with st.form("search_form"):
        author_name = st.text_input("작성자명", placeholder="조회할 작성자명을 입력하세요")
        search_button = st.form_submit_button("🔍 조회", use_container_width=True)
        
        if search_button and author_name:
            author_complaints = df[df['작성자'].str.contains(author_name, na=False, case=False)]
            
            if not author_complaints.empty:
                st.success(f"✅ '{author_name}'의 민원 {len(author_complaints)}건이 조회되었습니다.")
                
                for idx, complaint in author_complaints.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="complaint-card">
                            <div class="complaint-header">📋 {complaint['접수번호']}</div>
                            <strong>유형:</strong> {complaint['유형']}<br/>
                            <strong>작성일:</strong> {complaint['작성일']}<br/>
                            <strong>내용:</strong> {complaint['내용']}<br/>
                            <strong>위치:</strong> {complaint['위치']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ '{author_name}'의 민원을 찾을 수 없습니다.")
    
    st.markdown("---")
    st.markdown("### 📈 전체 민원 통계")
    st.metric("총 민원 수", len(df))
    
    if not df.empty:
        type_counts = df['유형'].value_counts()
        st.markdown("**유형별 민원 수:**")
        for complaint_type, count in type_counts.items():
            st.text(f"• {complaint_type}: {count}건")