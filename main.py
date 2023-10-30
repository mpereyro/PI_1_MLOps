import pandas as pd
from fastapi import FastAPI


app = FastAPI()

items_games_filtered = pd.read_parquet ('DATOS/items_games_filtered.parquet')

def PlayTimeGenre(genero: str) -> dict:
    """
    Devuelve el año con más horas jugadas para el género especificado.

    Args:
        genero (str): Género del juego
    Returns:
        dict: Diccionario con el género y el año de lanzamiento con más horas jugadas
    """
    # Filtrar por género
    df_util = items_games_filtered[items_games_filtered['genres'] == genero]

    if df_util.empty:
        return f"No hay datos para el género {genero}"

    # Agrupar por el año de lanzamiento y sumar las horas jugadas
    agrupado = df_util.groupby('release_year')['playtime_forever'].sum().sort_values(ascending=False)

    # Obtener el año con más horas jugadas
    anio = agrupado.index[0]

    return {f'Año de lanzamiento con más horas jugadas para el género {genero}': int(anio)}
