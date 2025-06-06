import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

st.title('📝 민원 등록하기')

if "marker_location" not in st.session_state:
    st.session_state.marker_location = [37.564375, 126.938871]
    st.session_state.zoom = 16

m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)

marker = folium.Marker(
    location=st.session_state.marker_location,
    draggable=False
)
marker.add_to(m)

map = st_folium(m, width=620, height=580, key="folium_map")

if map.get("last_clicked"):
    lat, lng = map["last_clicked"]["lat"], map["last_clicked"]["lng"]
    st.session_state.marker_location = [lat, lng]  # Update session state with new marker location
    st.session_state.zoom = map["zoom"]
    # Redraw the map immediately with the new marker location
    m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
    folium.Marker(
        location=st.session_state.marker_location,
        draggable=False
    ).add_to(m)
    map = st_folium(m, width=620, height=580, key="folium_map")

st.write(f"위도: {st.session_state.marker_location[0]:.6f}, 경도: {st.session_state.marker_location[1]:.6f}")