
## ✅ PASO 6: Estadísticas de Jugadores

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import cargar_datos

dash.register_page(__name__, path="/jugadores", name="Jugadores")

# Cargar los datos
_, jugadores_df, _ = cargar_datos()

# 🔁 Datos base
equipos = jugadores_df["Club"].dropna().unique()
metricas_boxplot = ["Edad", "Altura", "Peso", "Minutos jugados"]
metricas_radar = [
    "Duelos aéreos ganados %",
    "Duelos ganados %",
    "Precisión centros %",
    "Precisión desmarques %",
    "Precisión pases %",
    "Regates realizados %",
    "Duelos defensivos ganados %",
    "Duelos atacantes ganados %",
    "Precisión pases hacia atrás %"
]

# 🎨 Estilos
estilo_seccion = {
    "padding": "25px",
    "marginBottom": "25px",
    "backgroundColor": "#1f1f1f", "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
    "borderRadius": "10px"
}
titulo_seccion = {"color": "white", "marginBottom": "15px", "fontSize": "24px", "fontWeight": "bold"}

# 🔥 Generar Heatmap
def generar_heatmap():
    heatmap_data = jugadores_df.groupby(["Club", "Posición principal"]).size().unstack(fill_value=0)
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Posición", y="Club", color="Cantidad"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="Blues",
        text_auto=True
    )
    fig.update_traces(textfont_size=12)
    fig.update_layout(
        title="Distribución de jugadores por Club y Posición",
        xaxis_title="Posición",
        yaxis_title="Club",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font_color="white"
    )
    return fig

layout = html.Div([
    
html.H2(
    "👕 Jugadores Campeonato Itau 2024",
    style={
        "textAlign": "center",
        "color": "#ffffff",
        "fontSize": "32px",
        "marginBottom": "40px",
        "fontWeight": "bold",
        "textShadow": "0 2px 4px rgba(0,0,0,0.5)"
    }
),

    # 🔥 1. Mapa de calor por posición
    html.Div([
        html.H4("🏃‍♂️. Distribución de Jugadores por Equipo y Posición", style=titulo_seccion),
        dcc.Graph(id="heatmap-posicion", figure=generar_heatmap(), config={"displayModeBar": False}, style={"width": "75%", "height": "600px", "margin": "0 auto"})
    ], style=estilo_seccion),

    # 📊 2. Comparar métricas (Boxplot)
    html.Div([
        html.H4("📊. Comparar Métricas por Equipo", style=titulo_seccion),
        dbc.Label("Selecciona una métrica:", style={"color": "white"}),
        dcc.Dropdown(
            id="metrica-boxplot",
            options=[{"label": m, "value": m} for m in metricas_boxplot],
            value="Edad",
            style={"border": "2px solid black", "borderRadius": "5px"}
        ),
        dcc.Graph(id="grafico-boxplot", style={"width": "75%", "margin": "0 auto", "height": "600px"})
    ], style=estilo_seccion),

    # 📈 3. Barras por jugador
    html.Div([
        html.H4("📈. Métrica General por Equipo (Barras por Jugador)", style=titulo_seccion),
        dbc.Row([
            dbc.Col([
                dbc.Label("Selecciona un Club:", style={"color": "white"}),
                dcc.Dropdown(
                    id="club-general",
                    options=[{"label": eq, "value": eq} for eq in equipos],
                    value=equipos[0],
                    style={"border": "2px solid black", "borderRadius": "5px"}
                )
            ], md=6),
            dbc.Col([
                dbc.Label("Selecciona una Métrica:", style={"color": "white"}),
                dcc.Dropdown(
                    id="metrica-general",
                    options=[{"label": m, "value": m} for m in metricas_boxplot],
                    value="Minutos jugados",
                    style={"border": "2px solid black", "borderRadius": "5px"}
                )
            ], md=6),
        ]),
        html.Br(),
        html.Div(id="logo-club-general", style={"textAlign": "center"}),
        dcc.Graph(id="grafico-general", style={"width": "75%", "margin": "0 auto", "height": "600px"})
    ], style=estilo_seccion),

    # 🧭 4. Radar del Jugador
    html.Div([
        html.H4("🔍. Análisis Individual del Jugador (Radar de Barras)", style=titulo_seccion),
        dbc.Row([
            dbc.Col([
                dbc.Label("Selecciona un Club:", style={"color": "white"}),
                dcc.Dropdown(
                    id="club-radar",
                    options=[{"label": club, "value": club} for club in equipos],
                    placeholder="Selecciona un club",
                    style={"border": "2px solid black", "borderRadius": "5px"}
                )
            ], md=6),
            dbc.Col([
                dbc.Label("Selecciona un Jugador:", style={"color": "white"}),
                dcc.Dropdown(id="jugador-radar", placeholder="Selecciona un jugador")
            ], md=6),
        ]),
        html.Br(),
        dcc.Graph(id="grafico-radar", config={"displayModeBar": False}, style={"width": "75%", "margin": "0 auto", "height": "600px"})
    ], style=estilo_seccion),

    html.Div([
        html.Button("Exportar a PDF", id="btn-exportar", n_clicks=0, style={
            "marginBottom": "20px",
            "padding": "10px 20px",
            "fontWeight": "bold",
            "border": "2px solid white",
            "backgroundColor": "#007bff", "boxShadow": "0 2px 10px rgba(0, 123, 255, 0.6)",
            "color": "white",
            "cursor": "pointer"
        })
    ], style={"textAlign": "center"}),
    dcc.Interval(id='interval-print', interval=500, n_intervals=0, disabled=True),

], style={"backgroundColor": "#121212", "padding": "20px"})


# 📊 Callback Boxplot
@dash.callback(
    Output("grafico-boxplot", "figure"),
    Input("metrica-boxplot", "value")
)
def actualizar_boxplot(metrica):
    df_filtrado = jugadores_df[jugadores_df[metrica].notna()]
    fig = px.box(df_filtrado, x="Club", y=metrica, color="Club")
    fig.update_layout(
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font_color="white"
    )
    return fig

# 📈 Callback Barras por jugador
@dash.callback(
    Output("grafico-general", "figure"),
    Output("logo-club-general", "children"),
    Input("club-general", "value"),
    Input("metrica-general", "value")
)
def actualizar_general(club, metrica):
    datos = jugadores_df[jugadores_df["Club"] == club]
    fig = px.bar(datos, x="Jugador", y=metrica, color="Jugador", text=metrica)
    fig.update_layout(
        xaxis_title="Jugador", yaxis_title=metrica,
        paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white"
    )
    logo_url = datos["Logo_url"].iloc[0] if "Logo_url" in datos.columns else ""
    logo_html = html.Img(src=logo_url, height="70px") if logo_url else ""
    return fig, logo_html

# 🎯 Callback radar: actualizar jugadores por club
@dash.callback(
    Output("jugador-radar", "options"),
    Input("club-radar", "value")
)
def actualizar_jugadores(club):
    if club:
        jugadores = jugadores_df[jugadores_df["Club"] == club]["Jugador"].dropna().unique()
        return [{"label": j, "value": j} for j in jugadores]
    return []

# 🧭 Callback radar: gráfico radial
@dash.callback(
    Output("grafico-radar", "figure"),
    Input("club-radar", "value"),
    Input("jugador-radar", "value")
)
def actualizar_radar(club, jugador):
    if not jugador or not club:
        return go.Figure()

    datos = jugadores_df[(jugadores_df["Club"] == club) & (jugadores_df["Jugador"] == jugador)]

    if datos.empty:
        return go.Figure()

    valores = datos.iloc[0][metricas_radar].fillna(0).astype(float)

    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=valores,
        theta=metricas_radar,
        name=jugador,
        marker_color=px.colors.qualitative.Set3,
        marker_line_color="white",
        marker_line_width=1.2,
        opacity=0.9
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="#1a1a1a",
            radialaxis=dict(
                showticklabels=True,
                ticks='',
                gridcolor='gray',
                linecolor='white',
                color='white'
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
                color='white'
            )
        ),
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font_color="white",
        showlegend=False,
        margin=dict(t=50, b=30, l=30, r=30)
    )

    return fig

# 📄 Callback para exportar a PDF usando impresión del navegador
dash.clientside_callback(
    '''
    function(n_clicks) {
        if (n_clicks > 0) {
            window.print();
        }
        return window.dash_clientside.no_update;
    }
    ''',
    Output("interval-print", "n_intervals"),
    Input("btn-exportar", "n_clicks")
)
