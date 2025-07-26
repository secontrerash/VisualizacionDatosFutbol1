## ✅ PASO 8: Cerrar sesión

import dash
from dash import html, dcc

# Registrar la página como "/logout"
dash.register_page(__name__, path="/logout", name="Cerrar Sesión")

# Layout: limpia la sesión y redirige al login
layout = html.Div([
    dcc.Store(id="session-store", data={}, storage_type="session"),  # 🔄 Resetea la sesión
    dcc.Location(href="/login", id="logout-redirigir"),              # 🔁 Redirige al login
    html.P("Saliendo..."),                                           # (opcional) mensaje visual
])
