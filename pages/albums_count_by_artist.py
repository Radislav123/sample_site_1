import dash
from dash import dash_table
import style

from db import DB


dash.register_page(__name__, "/albums_count_by_artis", name = "Количество альбомов по исполнителям")

data = [{"Исполнитель": x[0], "Количество альбомов": x[1]} for x in DB.get_artists_album_count()]

layout = dash_table.DataTable(
    data,
    style_cell_conditional = style.Table.style_cell_conditional,
    style_data_conditional = style.Table.style_data_conditional,
    style_header = style.Table.style_header,
    sort_action = "native"
)
