from dataclasses import field
from datetime import datetime
from distutils.debug import DEBUG
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from map_plot import get_gps_tracks, line_chart, histogram_chart
from get_data import get_data_from_gs_sheet
from config import M_TO_MNI

st.set_page_config(page_title="ToNo et les deux 🐈‍⬛", layout="wide", page_icon="⛵")


# st.markdown(
#     """
#     <style>
#     .small-font {
#         font-size:12px;
#         font-style: italic;
#         color: #b1a7a6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

st.title("Le chemin parcourue en ⛵")

data = get_data_from_gs_sheet()

with st.sidebar:
    (start_time, end_time) = st.select_slider(
        "📅 Date time",
        options=data.index,
        value=(
            data.index[0],
            data.index[ len(data.index) -1 ]
        )
    )

st.subheader(f"Du {start_time} au {end_time}")
filtered_data = data[(data.index > start_time) & (data.index < end_time)]


if st.checkbox('Voir le tableau de données'):
    st.dataframe(filtered_data)

fig = get_gps_tracks(filtered_data)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric(label="Derrière vitesse", value=f"{filtered_data.speed[-1]:.1f} Knt/h", delta=f"{(filtered_data.speed[-1] - filtered_data.speed[-2]):.1f} Knt/h")
col2.metric(label="Derrière distance", value=f"{filtered_data.distance[-1]/1000:.2f} Km", delta=f"{(filtered_data.distance[-1] - filtered_data.distance[-2])/1000:.2f} Km")
col3.metric(label="Mille marin", value=f"{filtered_data.distance[-1] * M_TO_MNI:.2f} Mille nautique", delta=f"{(filtered_data.distance[-1] - filtered_data.distance[-2]) * M_TO_MNI:.2f} Mni")

col11, col12= st.columns(2)

with col11:
    st.subheader('Vitesse absolue')
    st.plotly_chart(line_chart(filtered_data, "abs_speed"), use_container_width=True)

with col12:
    field_dst = "distance"
    st.subheader('Distance en Km')
    distance_in_m = filtered_data.copy()
    distance_in_m[field_dst] = filtered_data[field_dst] / 1000
    st.plotly_chart(line_chart(distance_in_m, field_dst), use_container_width=True)


col21, col22= st.columns(2)

if DEBUG:
    with col21:
        st.subheader('Number of point by hour')
        hist_values = np.histogram(filtered_data.index.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)


st.subheader('Distribution de la vitesse absolut')
st.plotly_chart(histogram_chart(filtered_data, "abs_speed"), use_container_width=True)
