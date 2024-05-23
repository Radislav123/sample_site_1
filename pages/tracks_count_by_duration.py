import dash
import dash_bootstrap_components as dbc
import plotly.express
import plotly.graph_objs
from dash import Input, Output, callback, dcc, html

from db import DB


title = "Количество произведений по длительности"
dash.register_page(__name__, "/tracks_count_by_duration", name = title)

graph_id = "graph_id"
graph_option_id = "graph_option_id"
duration_step_slider_id = "duration_step_slider_id"
threshold_slider_id = "threshold_slider_id"
artist_dropdown_id = "artist_dropdown_id"
album_dropdown_id = "album_dropdown_id"

x_axis = "Длительность в секундах"
y_axis = "Количество произведений"

graph_types = {
    "Линия": plotly.express.line,
    "Столбик": plotly.express.bar,
    "Диаграмма рассеяния": plotly.express.scatter,
    "Диаграмма с областями": plotly.express.area,
    "Воронка": plotly.express.funnel
}
graph_type_names = list(graph_types)

DropdownItem = dict[str, int | None]


@callback(
    Output(graph_id, "figure"),
    Input(artist_dropdown_id, "value"),
    Input(album_dropdown_id, "value"),
    Input(duration_step_slider_id, "value"),
    Input(threshold_slider_id, "value"),
    Input(graph_option_id, "value")
)
def get_graph(
        artist: DropdownItem | str,
        album: DropdownItem | str,
        duration_step: int,
        threshold: int,
        graph_type_name: str
) -> plotly.graph_objs.Figure:
    if isinstance(artist, dict):
        artist_id = artist["value"]
    elif artist.isnumeric():
        artist_id = int(artist)
    else:
        artist_id = None

    if isinstance(album, dict):
        album_id = album["value"]
    elif album.isnumeric():
        album_id = int(album)
    else:
        album_id = None

    context = dash.callback_context
    if context.triggered_id == artist_dropdown_id:
        album_id = None

    duration_step = duration_step * 1000
    data = [{x_axis: (x[0] + 1) * duration_step // 1000, y_axis: x[1]}
            for x in DB.get_tracks_count_by_duration(artist_id, album_id, duration_step, threshold)]
    if len(data) == 0:
        data = [{x_axis: 0, y_axis: 0}]

    figure = graph_types[graph_type_name](data_frame = data, x = x_axis, y = y_axis, title = title)
    return figure


def get_artist_dropdown_items() -> list[DropdownItem]:
    artist_dropdown_items = [{"label": x[0], "value": x[1]} for x in DB.get_artists()]
    artist_dropdown_items.insert(0, {"label": "Все исполнители", "value": None})
    return artist_dropdown_items


@callback(
    Output(album_dropdown_id, "options"),
    Output(album_dropdown_id, "value"),
    Input(artist_dropdown_id, "value")
)
def get_album_dropdown_items(artist: DropdownItem | int) -> tuple[list[DropdownItem], DropdownItem]:
    if isinstance(artist, dict):
        artist_id = artist["value"]
    else:
        artist_id = artist

    album_dropdown_items = [{"label": x[0], "value": x[1]} for x in DB.get_albums(artist_id)]
    album_dropdown_items.insert(0, {"label": "Все альбомы", "value": None})
    return album_dropdown_items, album_dropdown_items[0]


layout = [
    html.Div(dcc.Graph(id = graph_id)),
    html.Br(),
    html.Div(
        [
            html.P("Шаг длительности:"),
            dcc.Slider(id = duration_step_slider_id, min = 1, max = 10, value = 5, step = 1)]
    ),
    html.Br(),
    html.Div(
        [
            html.P("Порог:"),
            dcc.Slider(id = threshold_slider_id, min = 0, max = 20, value = 0, step = 2)]
    ),
    html.Br(),
    html.Div(
        dbc.Select(
            id = artist_dropdown_id,
            options = get_artist_dropdown_items(),
            value = get_artist_dropdown_items()[0]
        )
    ),
    html.Br(),
    html.Div(dbc.Select(id = album_dropdown_id, value = get_album_dropdown_items(None)[0])),
    html.Br(),
    html.Div(dbc.RadioItems(id = graph_option_id, options = graph_type_names, value = graph_type_names[0]))
]
