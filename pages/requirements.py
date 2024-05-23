import dash
from dash import dcc, html


path = "requirements.txt"
dash.register_page(__name__, f"/{path}", name = "Зависимости", order = 1)

def preprocess(data: str) -> str:
    data = data.split()
    data = "  \n".join(data)
    return data

with open(path, 'r', encoding = "utf-16le") as file:
    layout = html.Div(dcc.Markdown(preprocess(file.read())))
