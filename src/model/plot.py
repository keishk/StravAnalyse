import folium
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import HeatMap
from plotly.subplots import make_subplots


def plot_data(df, x, y, color, line):
    trend = "ols" if line else None
    fig = px.scatter(
        data_frame=df,
        x=x,
        y=y,
        trendline=trend,
        color=color,
        color_discrete_sequence=px.colors.qualitative.G10,
        width=1000,
        hover_name="name",
    )
    fig["layout"].update(margin=dict(l=25, t=25, b=0))
    return fig


def plot_heatmap(df, year):
    df = df[df.year == year]
    lats = [coord[0] for coord in df["map.polyline"].sum()]
    lons = [coord[1] for coord in df["map.polyline"].sum()]
    # Create the Map
    m = folium.Map(location=[np.median(lats), np.median(lons)], zoom_start=11)
    HeatMap(data=list(zip(lats, lons)), radius=4, blur=3,).add_to(m)
    return m


def plot_activity(df, x, y1, y2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df[x], y=df[y1], name=y1), secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df[x], y=df[y2], name=y2), secondary_y=True,
    )
    fig.update_layout(margin=dict(l=25, t=25, b=10))
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text=y1, secondary_y=False)
    fig.update_yaxes(title_text=y2, secondary_y=True)
    return fig
