from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from map_plot import get_gps_tracks, line_chart
from data_computations import get_speeds
from layers import layer2, layer_boat
from random_data import rand_lat_lon
from get_data import get_data, get_data_from_gs_sheet


from config import DATE_COLUMN



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

st.title("Boat tracks")

# FIXME: don't work yet
df_gs_sheet = get_data_from_gs_sheet()


if st.checkbox('Show gs data'):
    st.dataframe(df_gs_sheet)
data = get_data()


# data = rows

with st.sidebar:
    (start_time, end_time) = st.select_slider(
        "📅 Date time",
        options=data.index,
        value=(
            data.index[0],
            data.index[ len(data.index) -1 ]
        )
    )

st.subheader(f"{start_time} : {end_time}")
# filtered_data = data.loc[start_time:end_time]
filtered_data = data[(data.index > start_time) & (data.index < end_time)]
# filtered_data = data[data[DATE_COLUMN] == minute_to_filter]

# st.subheader(f'Map of gps point at {minute_to_filter}:00')
# st.map(filtered_data)
fig = get_gps_tracks(filtered_data)
st.plotly_chart(fig, use_container_width=True)
if st.checkbox('Show raw data'):
    st.dataframe(filtered_data)

col1, col2 = st.columns(2)
col1.metric(label="Last speed", value=f"{filtered_data.speed[-1]:.1f} Knt/h", delta=f"{(filtered_data.speed[-1] - filtered_data.speed[-2]):.1f} Knt/h")
col2.metric(label="Last Distance", value=f"{filtered_data.distance[-1]:.1f} Knt", delta=f"{(filtered_data.distance[-1] - filtered_data.distance[-2]):.1f} Knt")

col11, col12= st.columns(2)


with col11:
    st.subheader('The absolute speed')
    st.plotly_chart(line_chart(filtered_data, "datetimes", "abs_speed"), use_container_width=True)

with col12:
    st.subheader('Distance')
    st.plotly_chart(line_chart(filtered_data, "datetimes", "distance"), use_container_width=True)
    # st.line_chart(data.abs_speed)



col21, col22= st.columns(2)

with col21:
    st.subheader('Number of point by hour')
    hist_values = np.histogram(filtered_data.index.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)
