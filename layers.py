import pydeck as pdk
import pandas as pd
import numpy as np

def layer_boat(data):
    line_layer = pdk.Layer(
        "HexagonLayer",
        # "LineLayer",
        data=data,
        # get_source_position="start",
        # get_target_position="end",
        get_position='[lon, lat]',
        # get_color=GET_COLOR_JS,
        # get_width=10,
        # highlight_color=[255, 255, 0],
        # picking_radius=10,
        # auto_highlight=True,
        pickable=True,
        extruded=True,
        radius=20000,
        elevation_scale=1,
        elevation_range=[1],
    )
    return line_layer


# st.pydeck_chart(pdk.Deck(
#      map_style='mapbox://styles/mapbox/light-v9',
#      initial_view_state=pdk.ViewState(
#          lat=37.76,
#          lon=-122.4,
#          zoom=11,
#          pitch=50,
#      ),
#      layers=[
#         layer_boat(data),
#      ],
#  ))

def layer2(df):
    layer = pdk.Layer(
        'HexagonLayer',
        data=df,
        get_position='[lon, lat]',
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
    )
    return layer
