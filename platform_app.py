import streamlit as st

homepage = st.Page("homepage.py", title="홈페이지", icon=":material/home:")
reporting_page = st.Page("reporting.py", title="민원 등록하기", icon=":material/add_location:")
confirmation_page = st.Page("confirmation.py", title="등록된 민원 확인하기", icon=":material/search:")

pg = st.navigation([homepage, reporting_page, confirmation_page])

pg.run()