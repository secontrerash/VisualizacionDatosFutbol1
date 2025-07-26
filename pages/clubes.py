## 🧩 Código completo de clubes.py

import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from utils.data_loader import cargar_datos

dash.register_page(__name__, path="/clubes", name="Clubes")

# Cargar los datos necesarios
equipos_df, _, puntos_df = cargar_datos()

# 🧮 Leer y procesar la tabla de posiciones
tabla_df = pd.read_excel("data/Tabla_2024.xlsx")
tabla_df = tabla_df[["Club", "Pos", "Pts", "Rendimiento", "PJ", "PG", "PE", "PP", "GF", "GC"]]

# Convertir 'Rendimiento' a formato porcentaje si no lo está
if tabla_df["Rendimiento"].dtype != "O":  # Si no es objeto (str), se formatea
    tabla_df["Rendimiento"] = (tabla_df["Rendimiento"] * 100).round(2).astype(str) + '%'

# Ordenar por puntos
tabla_df = tabla_df.sort_values("Pts", ascending=False)

# 📊 Layout de la página de Clubes
layout = dbc.Container([
    html.H2("🏆 Clubes Campeonato ITAU 2024", className="text-white", style={"textAlign": "center", "marginBottom": "30px"}),
    html.H4("📊 Tabla de Posiciones", style={"textAlign": "center", "marginTop": "20px", "color": "white"}),

    html.Div(dbc.Table.from_dataframe(tabla_df, striped=True, bordered=True, hover=True, responsive=True, className="table-dark"), style={"width": "75%", "margin": "0 auto"}),

    html.Hr(),

    html.H4("📈 Evolución de Puntajes", style={"textAlign": "center", "marginTop": "30px", "color": "white"}),

    dbc.Row([
        dbc.Col([
            html.Label("Equipo 1", style={"color": "white"}),
            dcc.Dropdown(
                id="equipo1",
                options=[{"label": eq, "value": eq} for eq in puntos_df["Clave"].unique()],
                value=puntos_df["Clave"].unique()[0]
            ),
            html.Img(id="logo1", style={"width": "80px", "margin": "auto", "display": "block", "marginTop": "10px"})
        ], md=6),
        dbc.Col([
            html.Label("Equipo 2", style={"color": "white"}),
            dcc.Dropdown(
                id="equipo2",
                options=[{"label": eq, "value": eq} for eq in puntos_df["Clave"].unique()],
                value=puntos_df["Clave"].unique()[1]
            ),
            html.Img(id="logo2", style={"width": "80px", "margin": "auto", "display": "block", "marginTop": "10px"})
        ], md=6)
    ], className="mb-4"),

    dcc.Graph(id="grafico-evolucion", style={"width": "75%", "margin": "0 auto", "height": "600px"}),

    html.Hr(),

    html.H4("📊 Velocímetro de Rendimiento", style={"textAlign": "center", "marginTop": "40px", "color": "white"}),

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un Equipo", style={"color": "white"}),
            dcc.Dropdown(
                id="equipo-rendimiento",
                options=[{"label": eq, "value": eq} for eq in equipos_df["Clave"].unique()],
                value=equipos_df["Clave"].unique()[0]
            ),
            html.Img(id="logo-rendimiento", style={"width": "80px", "margin": "auto", "display": "block", "marginTop": "10px"}),
            dcc.Graph(id="grafico-rendimiento", style={"width": "75%", "margin": "0 auto", "height": "600px"})
        ])
        ]),

    html.Div([
        html.Button("🖨️ Exportar Página como PDF", id="btn-exportar-pdf-clubes", n_clicks=0, style={
            "marginTop": "40px",
            "padding": "12px 28px",
            "backgroundColor": "#007bff",
            "color": "white",
            "border": "2px solid black",
            "borderRadius": "8px",
            "fontWeight": "bold",
            "cursor": "pointer"
        })
    ], style={"textAlign": "center"})
], fluid=True)

# 📈 CALLBACK: Evolución de puntajes
@callback(
    Output("grafico-evolucion", "figure"),
    [Input("equipo1", "value"), Input("equipo2", "value")]
)
def actualizar_grafico(equipo1, equipo2):
    fechas = [col for col in puntos_df.columns if col.startswith("Fecha_")]
    df1 = puntos_df[puntos_df["Clave"] == equipo1][fechas].values.flatten()
    df2 = puntos_df[puntos_df["Clave"] == equipo2][fechas].values.flatten()
    fechas_numeradas = list(range(1, len(fechas) + 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fechas_numeradas, y=df1.cumsum(), mode='lines+markers', name=equipo1))
    fig.add_trace(go.Scatter(x=fechas_numeradas, y=df2.cumsum(), mode='lines+markers', name=equipo2))

    fig.update_layout(
        title="Evolución de Puntajes por Fecha",
        xaxis_title="Fecha",
        yaxis_title="Puntaje Acumulado",
        template="plotly_dark"
    )
    return fig

# 📊 CALLBACK: Velocímetro de rendimiento
@callback(
    Output("grafico-rendimiento", "figure"),
    Input("equipo-rendimiento", "value")
)
def actualizar_velocimetro(equipo):
    # Obtenemos directamente el rendimiento en porcentaje
    rendimiento = equipos_df[equipos_df["Clave"] == equipo]["Rendimiento"].values[0]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rendimiento,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"Rendimiento de {equipo} (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "lightblue"},
            "bgcolor": "darkgray",
            "borderwidth": 2,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 40], "color": "#ff4d4d"},
                {"range": [40, 70], "color": "#ffff66"},
                {"range": [70, 100], "color": "#66ff66"}
            ],
            "threshold": {
                "line": {"color": "cyan", "width": 4},
                "thickness": 0.75,
                "value": rendimiento
            }
        }
    ))

    fig.update_layout(template="plotly_dark")
    return fig


# 🖼️ CALLBACK: Logos visuales
@callback(
    Output("logo1", "src"),
    Input("equipo1", "value")
)
def actualizar_logo1(equipo):
    return f"/assets/logos/{equipo}.png"

@callback(
    Output("logo2", "src"),
    Input("equipo2", "value")
)
def actualizar_logo2(equipo):
    return f"/assets/logos/{equipo}.png"

@callback(
    Output("logo-rendimiento", "src"),
    Input("equipo-rendimiento", "value")
)
def actualizar_logo_rendimiento(equipo):
    return f"/assets/logos/{equipo}.png"