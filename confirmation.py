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