import pandas as pd
from fastapi import FastAPI


app = FastAPI()

ruta_df_steam_games = 'DATOS/output_steam_games_trans.parquet'
df_steam_games = pd.read_parquet (ruta_df_steam_games)

ruta_df_user_review_sentiment_analysis = 'DATOS/australian_user_reviews_sentiment_analysis.parquet'
df_user_reviews = pd.read_parquet(ruta_df_user_review_sentiment_analysis)

ruta_data_items_resultante = 'DATOS/users_items_final.parquet'
df_users_items = pd.read_parquet(ruta_data_items_resultante)

df_users_items['item_id'] = df_users_items['item_id'].astype(int)
df_user_reviews['item_id'] = df_user_reviews['item_id'].astype(int)

# Fusionar información de juegos y usuarios basada en el ID del juego y el ID de usuario
items_games = pd.merge(df_users_items, df_steam_games, left_on='item_id', right_on='id')

reviews_games = pd.merge(df_user_reviews, df_steam_games, how='inner', left_on='item_id', right_on='id')


def PlayTimeGenre(genero: str) -> dict:
    """
    Devuelve el año con más horas jugadas para el género especificado.

    Args:
        genero (str): Género del juego
    Returns:
        dict: Diccionario con el género y el año de lanzamiento con más horas jugadas
    """
    # Filtrar por género
    df_util = items_games[items_games['genres'] == genero]

    # Agrupar por el año de lanzamiento y sumar las horas jugadas
    agrupado = df_util.groupby('release_year')['playtime_forever'].sum().sort_values(ascending=False)

    # Obtener el año con más horas jugadas
    anio = agrupado.index[0]

    return {f'Año de lanzamiento con más horas jugadas para el género {genero}': int(anio)}