import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/menu", name="Menú Principal")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("🏠 Menú Principal", className="text-center text-white mb-4"),
            dbc.Nav([
                dbc.NavLink("Equipos", href="/clubes", active="exact"),
                dbc.NavLink("Jugadores", href="/jugadores", active="exact"),
                dbc.NavLink("Machine Learning", href="/ml", active="exact"),
                dbc.NavLink("Salir", href="/", active="exact"),
            ], vertical=True, pills=True),
        ], width=3),
        dbc.Col([
            html.Div("Selecciona una opción del menú para comenzar.", className="text-white text-center")
        ])
    ])
], fluid=True, style={
    "height": "100vh",
    "backgroundColor": "#1e1e1e",
    "paddingTop": "30px"
})
