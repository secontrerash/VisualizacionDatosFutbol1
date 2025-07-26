
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

dash.register_page(__name__, path="/promesas", name="Promesas Sub-23")

try:
    df = pd.read_excel("data/Sub-23-T.xlsx")
    columnas_excluir = ["Jugador", "Clave", "Club", "Equipo", "Posición principal", "Posiciones", "Pasaporte", "Pie", "Valor de mercado (Transfermarkt)"]
    df_numerico = df.drop(columns=columnas_excluir, errors="ignore")

    for col in df_numerico.columns:
        df_numerico[col] = pd.to_numeric(df_numerico[col].astype(str).str.replace("%", "").str.replace(",", "."), errors="coerce")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_numerico.fillna(0))
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_resultado = df.loc[df_numerico.index].copy()
    df_resultado["Perfil"] = kmeans.fit_predict(X_scaled)
    pca = PCA(n_components=2)
    pca_coords = pca.fit_transform(X_scaled)
    df_resultado["PCA_1"] = pca_coords[:, 0]
    df_resultado["PCA_2"] = pca_coords[:, 1]

    df_resultado["Titular"] = ((df_resultado["Edad"] < 22) & (df_resultado["Minutos %"] > 50)).astype(int)

    X = X_scaled
    y = df_resultado["Titular"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_proba = model.predict_proba(X)[:, 1]
    df_resultado["Prob_Titular"] = (y_proba * 100).round(2)

    importancias = model.feature_importances_
    importancia_top = sorted(zip(df_numerico.columns, importancias), key=lambda x: x[1], reverse=True)[:10]

    layout = html.Div([
        html.H2("🎯 Perfiles de Jugadores Sub-23", className="text-white text-center my-4"),
        dcc.Markdown("""
#### 🎨 Interpretación de los Perfiles Detectados

**🟦 Perfil 0 – "Equilibrado ofensivo"**  
Jugadores completos, técnicamente fiables y físicamente competentes.  
_Edad media 21.3 años – buenos regates (58%), pases precisos (81%) y ganan más del 54% de los duelos._

**🟩 Perfil 1 – "Ofensivo creativo"**  
Pequeños, habilidosos y con gol.  
_Altura promedio 174 cm – destacan por goles (1.9), desmarques (42%) y regates (52%)._

**🟧 Perfil 2 – "Finalizador potente"**  
Altos, físicos y decisivos frente al arco.  
_Altura 187 cm – anotan más goles (4.0), pero contribuyen poco en juego asociado._

**🟥 Perfil 3 – "Defensor clásico"**  
Gigantes silenciosos que despejan y entregan limpio.  
_Altura 185 cm – lideran en duelos ganados (67%) y precisión de pase (83%)._
""", style={"backgroundColor": "#111", "color": "#eee", "padding": "20px", "borderRadius": "10px"}),
        dcc.Dropdown(id="filtro-perfil", options=[{"label": f"Perfil {i}", "value": i} for i in sorted(df_resultado["Perfil"].unique())], value=None, placeholder="Filtrar por perfil", style={"marginBottom": "20px"}),
        dcc.Graph(id="grafico-perfiles", style={"width": "75%", "margin": "0 auto"}),
        html.H4("📋 Top 20 Jugadores Sub-23", className="text-white mt-4"),
        dbc.Table.from_dataframe(df_resultado[["Jugador", "Edad", "Altura", "Peso", "Perfil"]].head(20), striped=True, bordered=True, hover=True, class_name="table-dark", style={"width": "75%", "margin": "0 auto"}),
        html.H4("🔮 Predicción de Titularidad (Top 10 Probabilidades)", className="text-white mt-5"),
        dbc.Table.from_dataframe(df_resultado.sort_values("Prob_Titular", ascending=False)[["Jugador", "Edad", "Minutos %", "Perfil", "Prob_Titular"]].head(10), striped=True, bordered=True, hover=True, class_name="table-dark", style={"width": "75%", "margin": "0 auto"}),
        dcc.Graph(figure=go.Figure(data=go.Bar(x=[x[1] for x in importancia_top], y=[x[0] for x in importancia_top], orientation="h")).update_layout(title="Importancia de Variables", template="plotly_dark", height=400), style={"width": "75%", "margin": "0 auto"}),
        html.Div([html.Button("📥 Exportar página como PDF", id="btn-exportar-pdf-sub23", n_clicks=0, style={"marginTop": "40px", "padding": "12px 28px", "backgroundColor": "#007bff", "color": "white", "border": "2px solid black", "borderRadius": "8px", "fontWeight": "bold", "cursor": "pointer"})], style={"textAlign": "center"})
    ])

    @callback(Output("grafico-perfiles", "figure"), Input("filtro-perfil", "value"))
    def actualizar_grafico(perfil):
        df_filtrado = df_resultado if perfil is None else df_resultado[df_resultado["Perfil"] == perfil]
        fig = px.scatter(df_filtrado, x="PCA_1", y="PCA_2", color=df_filtrado["Perfil"].astype(str), hover_data=["Jugador", "Edad", "Altura", "Peso"], title="Mapa de Perfiles Sub-23", labels={"Perfil": "Perfil"}, color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(template="plotly_dark", height=600)
        return fig

    @callback(Output("btn-exportar-pdf-sub23", "n_clicks"), Input("btn-exportar-pdf-sub23", "n_clicks"), prevent_initial_call=True)
    def exportar_pdf(n):
        print("Exportación PDF (placeholder)")
        return n

except Exception as e:
    layout = html.Div([
        html.H2("⚠️ Error al cargar datos", className="text-danger text-center my-5"),
        html.Pre(str(e), className="text-white text-center")
    ])
