import dash_bootstrap_components as dbc
import pandas
import plotly.express
from dash import Dash, Input, Output, callback, dcc


data = pandas.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv")


# @callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = data[data.country == value]
    return plotly.express.line(dff, x = "year", y = "pop")


def run() -> None:
    app = Dash(use_pages = True)

    if False:
        app.layout = [
            dbc.ModalHeader(children = "Title of Dash App", style = {"textAlign": "center"}),
            # html.H1(children = "Title of Dash App", style = {"textAlign": "center"}),
            # dbc.DropdownMenu(data.country.unique(), "Canada", id = "dropdown-selection"),
            dcc.Dropdown(data.country.unique(), "Canada", id = "dropdown-selection"),
            dcc.Graph(id = "graph-content")
        ]

    app.run(debug = True)


if __name__ == "__main__":
    run()
