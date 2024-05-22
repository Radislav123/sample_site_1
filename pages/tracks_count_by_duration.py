import functools

import dash
import plotly.express
from dash import Input, Output, callback, dcc, html

from db import DB


title = "Количество произведений по длительности"
dash.register_page(__name__, "/tracks_count_by_duration", name = title)

graph_id = "graph_id"
duration_step_slider_id = "duration_step_slider_id"
percentage_slider_id = "percentage_slider_id"

x_axis = "Длительность в секундах"
y_axis = "Количество произведений"


@callback(
    Output(graph_id, "figure"),
    Input(duration_step_slider_id, "value"),
    Input(percentage_slider_id, "value")
)
@functools.cache
def update_graph(duration_step: int, threshold: int):
    data = [{x_axis: (x[0] + 1) * duration_step // 1000, y_axis: x[1]}
            for x in DB.get_tracks_count_by_duration(duration_step, threshold)]
    figure = plotly.express.line(data, x_axis, y_axis, title = title)
    return figure


layout = [
    dcc.Graph(id = graph_id),
    html.P("Шаг длительности:"),
    dcc.Slider(id = duration_step_slider_id, min = 1000, max = 10000, value = 5000, step = 1000),
    html.P("Порог:"),
    dcc.Slider(id = percentage_slider_id, min = 0, max = 20, value = 0, step = 2)
]
