## ✅ PASO 5:  Carga de Datasets

import pandas as pd

# Función para cargar los datos necesarios para la app
def cargar_datos():
    # Cargar archivo de equipos (incluye columna Logo_url)
    equipos_df = pd.read_excel("data/Equipos_2024.xlsx")

    # Convertir la URL del logo a formato Markdown para mostrar imagen en la tabla
    equipos_df["Logo"] = equipos_df["Logo_url"].apply(lambda x: f"![logo]({x})")

    # Cargar archivo de jugadores
    jugadores_df = pd.read_excel("data/Jugadores1A_2024.xlsx")
    puntos_df = pd.read_excel("data/Puntos_2024.xlsx")
    return equipos_df, jugadores_df, puntos_df  # ✅ ESTA LÍNEA ES CLAVE