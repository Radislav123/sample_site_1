import dash
from dash import html


dash.register_page(__name__, "/test")

layout = html.Div(
    [
        html.H1("This is our test page"),
        html.Div("This is our test page content."),
    ]
)
