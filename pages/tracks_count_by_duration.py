import functools

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

artist_dropdown_item_id_text = "artist_dropdown_item"
artist_dropdown_item_ids = {x[1]: f"{artist_dropdown_item_id_text}_{x[1]}" for x in DB.get_artists()}
artist_dropdown_ids = {value: key for key, value in artist_dropdown_item_ids.items()}
artist_names = {x[1]: x[0] for x in DB.get_artists()}
album_dropdown_item_id_text = "album_dropdown_item"
album_dropdown_item_ids = {x[1]: f"{album_dropdown_item_id_text}_{x[1]}" for x in DB.get_albums(None)}
album_dropdown_ids = {value: key for key, value in album_dropdown_item_ids.items()}
album_titles = {x[1]: x[0] for x in DB.get_albums(None)}

artist_label_id = "artist_label_id"
album_label_id = "album_label_id"

graph_types = {
    "Линия": plotly.express.line,
    "Столбик": plotly.express.bar,
    "Диаграмма рассеяния": plotly.express.scatter,
    "Диаграмма с областями": plotly.express.area,
    "Воронка": plotly.express.funnel
}
graph_type_names = list(graph_types)


@functools.cache
def get_artist_dropdown_inputs() -> list[Input]:
    return [Input(artist_dropdown_item_ids[x[1]], "n_clicks") for x in DB.get_artists()]


@functools.cache
def get_album_dropdown_inputs(artist_id: int | None) -> list[Input]:
    return [Input(album_dropdown_item_ids[x[1]], "n_clicks") for x in DB.get_albums(artist_id)]


@functools.cache
def get_artists_dropdown_items() -> list[dbc.DropdownMenuItem]:
    data = DB.get_artists()
    children = [dbc.DropdownMenuItem(x[0], artist_dropdown_item_ids[x[1]]) for x in data]
    return children


@functools.cache
def get_album_dropdown_items(artist_id: int | None) -> list[dbc.DropdownMenuItem]:
    data = DB.get_albums(artist_id)
    children = [dbc.DropdownMenuItem(x[0], album_dropdown_item_ids[x[1]]) for x in data]
    return children


def get_trigger_id() -> tuple[int | None, int | None]:
    context = dash.callback_context
    trigger_id = context.triggered_id

    artist_id = None
    album_id = None

    if trigger_id is not None:
        if album_dropdown_item_id_text in trigger_id:
            album_id = album_dropdown_ids[trigger_id]
        elif artist_dropdown_item_id_text in trigger_id:
            artist_id = artist_dropdown_ids[trigger_id]
    return artist_id, album_id


@callback(
    Output(graph_id, "figure"),
    get_artist_dropdown_inputs(),
    get_album_dropdown_inputs(None),
    Input(duration_step_slider_id, "value"),
    Input(threshold_slider_id, "value"),
    Input(graph_option_id, "value")
)
@functools.cache
def get_graph(*_) -> plotly.graph_objs.Figure:
    context = dash.callback_context
    inputs = {x["id"]: x for x in context.inputs_list}

    artist_id, album_id = get_trigger_id()
    duration_step = inputs[duration_step_slider_id]["value"] * 1000
    threshold = inputs[threshold_slider_id]["value"]
    graph_type = graph_types[inputs[graph_option_id]["value"]]

    data = [{x_axis: (x[0] + 1) * duration_step // 1000, y_axis: x[1]}
            for x in DB.get_tracks_count_by_duration(artist_id, album_id, duration_step, threshold)]
    if len(data) == 0:
        data = [{x_axis: 0, y_axis: 0}]

    figure = graph_type(data_frame = data, x = x_axis, y = y_axis, title = title)
    return figure


@callback(
    Output(artist_label_id, "children"),
    get_artist_dropdown_inputs(),
    get_album_dropdown_inputs(None)
)
@functools.cache
def get_artist_label(*_) -> str:
    artist_id, album_id = get_trigger_id()

    if artist_id is None:
        artist = "Исполнитель"
    else:
        artist = artist_names[artist_id]
    return artist


@callback(
    Output(album_label_id, "children"),
    get_artist_dropdown_inputs(),
    get_album_dropdown_inputs(None)
)
@functools.cache
def get_album_label(*_) -> str:
    artist_id, album_id = get_trigger_id()

    if album_id is None:
        album = "Альбом"
    else:
        album = album_titles[album_id]
    return album


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
        dbc.ButtonGroup(
            [
                dbc.Button(id = artist_label_id),
                dbc.DropdownMenu(id = artist_dropdown_id, children = get_artists_dropdown_items(), group = True)
            ],
        )
    ),
    html.Br(),
    html.Div(
        dbc.ButtonGroup(
            [
                dbc.Button(id = album_label_id),
                dbc.DropdownMenu(id = album_dropdown_id, children = get_album_dropdown_items(None), group = True)
            ]
        )
    ),
    html.Br(),
    html.Div(dbc.RadioItems(id = graph_option_id, options = graph_type_names, value = graph_type_names[0]))
]
