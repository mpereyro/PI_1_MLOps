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

def UserForGenre(genero: str) -> dict:
    """
    Devuelve el usuario que acumula más horas jugadas para el género dado
    y una lista de la acumulación de horas jugadas por año.

    Args:
        genero (str): Género del juego
    Returns:
        dict: Diccionario con el usuario y la lista de horas jugadas por año
    """
    # Filtrar por género
    df_util = items_games[items_games['genres'] == genero]

    # Agrupar por usuario y año, sumando las horas jugadas
    group = df_util.groupby(['user_id', 'release_year'])['playtime_forever'].sum().reset_index()

    # Encontrar el usuario con más horas jugadas
    user_max_playtime = group.groupby('user_id')['playtime_forever'].sum().idxmax()
    user_max_hours = group.loc[group['user_id'] == user_max_playtime]

    # Filtrar los años con horas acumuladas mayores a 0
    filtered_hours_per_year = user_max_hours.set_index('release_year')['playtime_forever'].to_dict()
    filtered_hours_per_year = {year: hours for year, hours in filtered_hours_per_year.items() if hours > 0}

    return {
        'Usuario con más horas jugadas para el género': str(user_max_playtime),
        'Acumulación de horas jugadas por año (mayores a 0)': filtered_hours_per_year
    }

def UsersRecommend(año: int) -> dict:
    # Filtrar los juegos para el año especificado
    juegos_año = reviews_games[reviews_games['release_year'] == año]

    # Filtrar los juegos más recomendados con comentarios positivos o neutrales
    juegos_recomendados = juegos_año[
        (juegos_año['recommend'] == True) & 
        (juegos_año['sentiment_analysis'].isin(['Positive', 'Neutral']))
    ]

    # Obtener el top 3 de juegos más recomendados
    top_3_juegos = juegos_recomendados.nlargest(3, 'sentiment_analysis')

    # Crear un diccionario con los top 3 juegos recomendados
    top_juegos_dict = {
        f"Top {i+1} Juego Recomendado": top_3_juegos.iloc[i]['title'] for i in range(3)
    }

    return top_juegos_dict