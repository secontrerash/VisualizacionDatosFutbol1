## ✅ PASO 2: Control de Inicio

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/home", name="Home")

layout = html.Div([
    dcc.Location(id='location-home'),
    dcc.Store(id='login-store', storage_type='session'),

    dbc.Row([
        dbc.Col(
            dbc.Nav([
                dbc.NavLink("Equipos", href="/clubes", active="exact"),
                dbc.NavLink("Jugadores", href="/jugadores", active="exact"),
                dbc.NavLink("Machine Learning", href="/ml", active="exact"),
                html.Hr(),
                dbc.Button("Salir", id="boton-salir", color="danger", className="mt-2")
            ], vertical=True, pills=True),
            width=2,
            style={"background-color": "#1e1e1e", "padding": "20px", "min-height": "100vh"}
        ),
        dbc.Col(
            html.Div(id="contenido-pagina"),
            width=10
        )
    ])
])

@dash.callback(
    Output("location-home", "href"),
    Input("boton-salir", "n_clicks"),
    prevent_initial_call=True
)
def salir_app(n):
    return "/"
