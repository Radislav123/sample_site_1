import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from db import DB


dash.register_page(__name__, f"/{DB.script_path}", name = "Скрипт генерации БД", order = 2)


def prepare_script(script: str) -> str:
    return f"```sqlite{script}```"


layout = html.Div(
    [
        dbc.CardLink("Ссылка на источник", href = "https://github.com/lerocha/chinook-database", target = "_blank"),
        html.Br(),
        dcc.Markdown(prepare_script(DB.script))
    ]
)
