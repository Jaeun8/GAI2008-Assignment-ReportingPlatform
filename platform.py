import folium
import streamlit as st

from streamlit_folium import st_folium

st.title('민원 신고')

# center on Liberty Bell, add marker
m = folium.Map(location=[37.564375, 126.938871], zoom_start=16)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)