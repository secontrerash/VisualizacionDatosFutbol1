## ✅ PASO 5:  Carga de Datasets

import pandas as pd
import os

def cargar_datos():
    try:
        # Cargar archivo de equipos con logos y rendimiento
        equipos_df = pd.read_excel("data/Equipos_2024.xlsx")
        equipos_df.columns = equipos_df.columns.str.strip()  # Limpiar espacios
        if "Logo_url" in equipos_df.columns:
            equipos_df["Logo"] = equipos_df["Logo_url"].apply(lambda x: f"/assets/logos/{x}" if pd.notna(x) else "")
        else:
            equipos_df["Logo"] = ""

        # Asegurarse que 'Clave' es string (por si se usa en múltiples merges)
        if "Clave" in equipos_df.columns:
            equipos_df["Clave"] = equipos_df["Clave"].astype(str).str.strip()

        # Cargar archivo de jugadores
        jugadores_df = pd.read_excel("data/Jugadores1A_2024.xlsx")
        jugadores_df.columns = jugadores_df.columns.str.strip()

        # Conversión segura de columnas numéricas
        columnas_numericas = ["Edad", "Peso", "Altura", "Minutos jugados"]
        for col in columnas_numericas:
            if col in jugadores_df.columns:
                jugadores_df[col] = pd.to_numeric(jugadores_df[col], errors="coerce")

        # Cargar archivo de puntos por fecha
        puntos_df = pd.read_excel("data/Puntos_2024.xlsx")
        puntos_df.columns = puntos_df.columns.str.strip()
        if "Clave" in puntos_df.columns:
            puntos_df["Clave"] = puntos_df["Clave"].astype(str).str.strip()

        return equipos_df, jugadores_df, puntos_df

    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")
        return None, None, None
