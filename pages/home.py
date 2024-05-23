import dash
from dash import dcc, html


dash.register_page(__name__, "/", name = "Главная", order = 0)

with open("README.md", 'r', encoding = "utf-8") as file:
    layout = html.Div(dcc.Markdown(file.read()))
