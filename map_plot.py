import plotly.graph_objects as go
import plotly.express as px
from config import API_TOKEN


def get_gps_tracks(gps_df_input):
    gps_df = gps_df_input
    fig = go.Figure()

    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = gps_df.lon,
        lat = gps_df.lat,
        marker=go.scattermapbox.Marker(
                color=gps_df.speed,
                colorscale=["green", "yellow", "red" ],
                opacity=0.7
            ),
        line=go.scattermapbox.Line(
                width=1,
            ),
        hovertemplate=[
            f"{point[0]:%Y/%m/%d %H:%M}"
            f"</br></br>lat : {point[1]:.2f}"
            f"</br>lon : {point[2]:.2f}"
            f"<extra>speed : {point[3]:.1f}</extra>"
            for point in gps_df.reset_index(level=0)[["datetimes", "lat", "lon", "speed"]].values
        ],

    ))


    fig.update_layout(
        font_size=11,
        autosize=False,
        height=500,
        title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,},
        title_font_size = 24,
        mapbox_accesstoken=API_TOKEN,
        mapbox_style = "mapbox://styles/mapbox/satellite-v9",
        mapbox={'center': go.layout.mapbox.Center(lat=gps_df.lat[-1], lon=gps_df.lon[-1]), 'zoom': 3},
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_layout(showlegend=False)
    # fig.update_traces(marker=dict(size=6))
    fig.update_yaxes(automargin=True)
    return fig

def line_chart(df, x, y, title=''):
    fig = px.line(df, x=df.index, y=y, title=title)
    return fig
