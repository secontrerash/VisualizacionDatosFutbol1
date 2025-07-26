## ✅ PASO 3: Página de inicio de la sesión

import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

# 🔐 Usuarios y contraseñas (puedes engancharlo a Excel si quieres)
usuarios_validos = {
    "admin": "123456",
    "usuario": "111111",
    "visita": "999999",
    "invitado": "666666"
}

# 🎨 Estilo del fondo y caja de login
estilo_fondo = {
    "backgroundImage": "url('/assets/login_background.png')",
    "backgroundSize": "cover",
    "backgroundPosition": "center",
    "height": "100vh",
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center"
}

layout = html.Div(
    style=estilo_fondo,
    children=[
        dbc.Card(
            dbc.CardBody([
                html.H2("Inicio de Sesión", className="text-center mb-4", style={"color": "white"}),
                dbc.Input(id="usuario", placeholder="Usuario", type="text", className="mb-3"),
                dbc.Input(id="password", placeholder="Contraseña", type="password", className="mb-3"),
                dbc.Button("Ingresar", id="login-button", color="primary", style={"width": "100%"}),
                html.Div(id="mensaje-login", className="text-danger mt-3 text-center")
            ]),
            style={
                "width": "100%",
                "maxWidth": "350px",
                "padding": "30px",
                "backgroundColor": "rgba(0,0,0,0.6)",
                "borderRadius": "12px"
            }
        )
    ]
)

# ✅ Callback para validar usuario y redirigir a equipos
@callback(
    # Output("mensaje-login", "children"),
    Output("url-login", "pathname", allow_duplicate=True),
    Input("login-button", "n_clicks"),
    State("usuario", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def verificar_login(n_clicks, usuario, password):
    if not usuario or not password:
        return "⚠️ Ingrese usuario y contraseña", dash.no_update

    if usuarios_validos.get(usuario) == password:
        return "", "/clubes"  # ✅ Cambia esto a donde quieres redirigir tras login
    else:
        return "⚠️ Usuario o contraseña incorrectos", dash.no_update

