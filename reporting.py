import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

st.title('민원 등록하기')

m = folium.Map(location=[37.564375, 126.938871], zoom_start=16)

draw = Draw(
    export=False,
    draw_options={
        "polyline": False,
        "polygon": False,
        "circle": False,
        "rectangle": False,
        "circlemarker": False,
        "marker": True
    },
    edit_options={"edit": False}
)
draw.add_to(m)

output = st_folium(m, width=725)