import folium
import streamlit as st
from streamlit_folium import st_folium

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