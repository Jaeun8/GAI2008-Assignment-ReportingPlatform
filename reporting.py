import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

st.title('📝 민원 등록하기')

def get_pos(lat, lng):
    return lat, lng

if "marker_location" not in st.session_state:
    st.session_state.marker_location = [37.564375, 126.938871]
    st.session_state.zoom = 16

m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
