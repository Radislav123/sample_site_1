import dash
from dash import dash_table

from db import DB


dash.register_page(__name__, "/albums_count_by_artis", name = "Количество альбомов по исполнителям")

data = [{"Исполнитель": x[0], "Количество альбомов": x[1]} for x in DB.get_artists_album_count()]

layout = dash_table.DataTable(
    data,
    style_cell_conditional = [
        {
            "if": {"column_id": "Исполнитель"},
            "textAlign": "left"
        }
    ],
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(220, 220, 220)",
        }
    ],
    style_header={
        "backgroundColor": "rgb(210, 210, 210)",
        "color": "black",
        "fontWeight": "bold"
    },
    sort_action = "native"
)
