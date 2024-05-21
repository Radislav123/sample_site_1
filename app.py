import dash.development.base_component
import dash_bootstrap_components as dbc
from dash import Dash


def construct_app_layout() -> dbc.Container:
    navigation_bar = dbc.NavbarSimple(
        [dbc.NavItem(dbc.NavLink(page["name"], href = page["path"])) for page in dash.page_registry.values()],
    )

    layout = dbc.Container(
        [
            navigation_bar,
            dash.page_container
        ]
    )
    return layout


def run() -> None:
    app = Dash(use_pages = True, external_stylesheets = [dbc.themes.BOOTSTRAP])

    app.layout = construct_app_layout()

    app.run(debug = True)


if __name__ == "__main__":
    run()
