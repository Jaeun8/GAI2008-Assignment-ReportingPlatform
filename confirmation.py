import streamlit as st
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