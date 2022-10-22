from dataclasses import field
from datetime import datetime
from distutils.debug import DEBUG
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from map_plot import get_gps_tracks, line_chart, histogram_chart
from get_data import get_data_from_gs_sheet, get_local_data
from config import M_TO_MNI
import plotly.express as px

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
# data = get_local_data()

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

total_distance = filtered_data.distance.sum()
st.subheader(f"Distance sur la plage de temps : {total_distance / 1000:.1f} Km soit {total_distance* M_TO_MNI:.1f} Mille nautique")

st.subheader('Dernière')
col1, col2, col3 = st.columns(3)
col1.metric(label="Vitesse", value=f"{filtered_data.speed[-1]:.1f} Knt/h", delta=f"{(filtered_data.speed[-1] - filtered_data.speed[-2]):.1f} Knt/h")
col2.metric(label="Distance en km", value=f"{filtered_data.distance[-1]/1000:.2f} Km", delta=f"{(filtered_data.distance[-1] - filtered_data.distance[-2])/1000:.2f} Km")
col3.metric(label="Distance en mille marin", value=f"{filtered_data.distance[-1] * M_TO_MNI:.2f} Milles nautique", delta=f"{(filtered_data.distance[-1] - filtered_data.distance[-2]) * M_TO_MNI:.2f} Mni")

field_dst = "distance"
distance_in_m = filtered_data.copy()
distance_in_m[field_dst] = filtered_data[field_dst] / 1000

st.subheader('Vitesse par jour')
field_speed = "speed"
nb_days = len(set(filtered_data.index))
st.plotly_chart(px.scatter(filtered_data, x=filtered_data.index, y=field_speed, color=field_speed, size=field_speed), use_container_width=True)


col11, col12= st.columns(2)
with col11:
    st.subheader('Vitesse absolue')
    st.plotly_chart(line_chart(filtered_data, "abs_speed"), use_container_width=True)

with col12:
    st.subheader('Distribution de la vitesse absolut')
    st.plotly_chart(histogram_chart(filtered_data, "abs_speed"), use_container_width=True)

if st.button("Clear all cache"):
    # Clear values from *all* memoized functions:
    # i.e. clear values from both square and cube
    st.experimental_memo.clear()
