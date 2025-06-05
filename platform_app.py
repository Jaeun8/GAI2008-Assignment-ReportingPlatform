import streamlit as st

homepage = st.Page("homepage.py", title="홈페이지", icon=":material/home:")
reporting_page = st.Page("reporting.py", title="민원 신청하기", icon=":material/add_location:")
confirmation_page = st.Page("confirmation.py", title="작성된 민원 확인하기", icon=":material/check_circle:")

pg = st.navigation([homepage, reporting_page, confirmation_page])
st.set_page_config(page_title="Homepage", page_icon=":material/home:")
pg.run()