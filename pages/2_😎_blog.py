import streamlit as st
import pandas as pd
from config import LOCAL_CSV

local_csv = pd.read_csv(LOCAL_CSV)


with st.sidebar:
    (start_time, end_time) = st.select_slider(
        "✏️ Post N°",
        options=local_csv.index,
        value=(
            local_csv.index[0],
            local_csv.index[ len(local_csv.index) -1 ]
        )
    )

filtered_data = local_csv[(local_csv.index >= start_time) & (local_csv.index <= end_time)]

for row in range(start_time, end_time + 1):
    row_value = filtered_data.loc[[row]]
    st.title(f"n° {row} {row_value.title.values[0]}")
    st.markdown(row_value.message.values[0])

st.dataframe(filtered_data)
