# app.py

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Crear app con soporte para múltiples páginas
app = dash.Dash(
    __name__,
    use_pages=True,  # Permite usar las páginas dinámicamente desde /pages
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SLATE],
    title="TFM Dashboard"
)
server = app.server

# Usuarios válidos
usuarios_validos = {
    "admin": "123456",
    "usuario": "111111",
    "visita": "999999",
    "invitado": "666666"
}

# Menú lateral
sidebar = html.Div([
    html.Img(src="/assets/logo_menu.png", style={"width": "100%", "margin-bottom": "2rem"}),
    dbc.Nav([
        dbc.NavLink("Equipos", href="/clubes", active="exact"),
        dbc.NavLink("Jugadores", href="/jugadores", active="exact"),
        dbc.NavLink("Machine Learning", href="/ml", active="exact"),
        dbc.NavLink("Promesas Sub-23", href="/promesas", active="exact"),
        dbc.NavLink("Salir", href="/", active="exact"),
    ], vertical=True, pills=True),
], style={
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#1e1e2f",
    "color": "white"
})

# Layout para login
login_layout = html.Div([
    html.Div([
        html.H2("Inicio de Sesión", style={"color": "white", "margin-bottom": "20px"}),
        dbc.Input(id="usuario", placeholder="Usuario", type="text", className="mb-3"),
        dbc.Input(id="password", placeholder="Contraseña", type="password", className="mb-3"),
        dbc.Button("Ingresar", id="login-button", color="primary", className="w-100"),
        html.Div(id="mensaje-login", className="mt-2", style={"color": "red", "text-align": "center"})
    ], style={
        "background-color": "rgba(0, 0, 0, 0.7)",
        "padding": "2rem",
        "border-radius": "10px",
        "width": "300px",
        "margin": "auto"
    }),
], style={
    "height": "100vh",
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    "background-image": "url('/assets/login_background.png')",
    "background-size": "cover",
    "background-position": "center"
})

# Layout principal con menú y contenedor de páginas
main_layout = html.Div([
    sidebar,
    html.Div(dash.page_container, style={"margin-left": "18rem", "padding": "2rem"})
])

# Layout general controlado por login
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Mostrar login o dashboard según URL
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/" or pathname is None:
        return login_layout
    else:
        return main_layout

# Validación de usuario
@app.callback(
    Output("url", "pathname"),
    Output("mensaje-login", "children"),
    Input("login-button", "n_clicks"),
    State("usuario", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login(n_clicks, usuario, password):
    if not usuario or not password:
        return dash.no_update, "⚠️ Ingrese usuario y contraseña"
    elif usuario in usuarios_validos and usuarios_validos[usuario] == password:
        return "/clubes", ""
    else:
        return dash.no_update, "⚠️ Usuario o contraseña incorrectos"

# Ejecutar app
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
