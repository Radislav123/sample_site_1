import dash
import plotly.express
from dash import Input, Output, callback, dcc, html

from db import DB


title = "Количество произведений по длительности"
dash.register_page(__name__, "/tracks_count_by_duration", name = title)
graph_id = "graph"
slider_id = "slider"


# todo: replace 10000 by callback
# data = [{"Длительность": x[0], "Количество произведений": x[1]} for x in DB.get_tracks_count_by_duration(10000)]


@callback(Output(graph_id, "figure"), Input(slider_id, "value"))
def update_graph(duration_step: int):
    x_axis = "Длительность в секундах"
    y_axis = "Количество произведений"
    data = [{x_axis: x[0] / 1000, y_axis: x[2]} for x in DB.get_tracks_count_by_duration(duration_step)]
    figure = plotly.express.line(data, x_axis, y_axis, title = title)
    return figure


layout = [
    dcc.Graph(id = graph_id),
    html.P("Шаг длительности:"),
    dcc.Slider(id = slider_id, min = 1000, max = 10000, value = 5000, step = 1000),
]
