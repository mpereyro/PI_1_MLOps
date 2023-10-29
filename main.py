from fastapi import FastAPI
from typing import List
import pandas as pd
import time

df_steam_games = pd.read_csv ('C:/Users/Mauro/Desktop/HENRY/Proyecto_individual/PI_1_MLOps/PI_MLOps-STEAM/steam_games.json/output_steam_games.csv')
df_user_reviews = pd.read_csv('C:/Users/Mauro/Desktop/HENRY/Proyecto_individual/PI_1_MLOps/PI_MLOps-STEAM/user_reviews.json/australian_user_reviews_sentiment_analysis.csv')
df_users_items = pd.read_csv('C:/Users/Mauro/Desktop/HENRY/Proyecto_individual/PI_1_MLOps/PI_MLOps-STEAM/users_items.json/users_items.csv')

app = FastAPI()

items_games = pd.merge(df_users_items, df_steam_games, how='inner', on=['item_id', 'title'])
reviews_games = pd.merge(df_user_reviews, df_steam_games, how='inner', on='item_id')

# Decorador para medir el tiempo de ejecución
def calcular_tiempo_ejecucion(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        print(f"Tiempo de ejecución de '{func.__name__}': {tiempo_transcurrido} segundos")
        return resultado
    return wrapper

@app.get("/PlayTimeGenre/{genero}")
@calcular_tiempo_ejecucion  # Aplicamos el decorador
def play_time_by_genre(genero: str):
    # Filtra los juegos por género
    games_in_genre = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]

    # Fusiona los datos de juegos y usuarios
    merged_data = pd.merge(df_users_items, games_in_genre, left_on='item_id', right_on='id')

    # Agrupa por juego y calcula el tiempo de juego promedio
    result = merged_data.groupby('title')['playtime_forever'].mean().reset_index()

    return result.to_dict(orient='records')

@app.get("/user_for_genre/{genero}")
@calcular_tiempo_ejecucion  # Aplicamos el decorador
async def UserForGenre(genero: str):
    # Paso 1: Filtrar los juegos del género especificado
    juegos_genero = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False, regex=False)]

    if juegos_genero.empty:
        return {"message": f"No se encontraron juegos del género '{genero}'."}

    # Paso 2: Unir el DataFrame filtrado con df_users_items
    df_filtrado_y_items = pd.merge(df_users_items, juegos_genero, left_on='item_id', right_on='id')

    # Paso 3: Calcular la acumulación de horas jugadas por usuario para el género dado
    horas_acumuladas = df_filtrado_y_items.groupby('user_id')['playtime_forever'].sum().reset_index()
    
    # Paso 4: Encontrar el usuario que acumula más horas jugadas
    usuario_max_horas = horas_acumuladas.loc[horas_acumuladas['playtime_forever'].idxmax()]

    # Paso 5: Calcular la acumulación de horas jugadas por año para ese usuario en el género especificado
    usuario_id = usuario_max_horas['user_id']
    usuario_juego_genero = df_filtrado_y_items[(df_filtrado_y_items['user_id'] == usuario_id) & (df_filtrado_y_items['genres'] == genero)]
    usuario_acumulacion_anual = usuario_juego_genero.groupby(usuario_juego_genero['release_date'].dt.year)['playtime_forever'].sum().reset_index()

    # Paso 6: Devolver el resultado
    return {
        "usuario": usuario_id,
        "acumulacion_anual_horas": usuario_acumulacion_anual.to_dict(orient="records")
    }

@app.get("/users_recommend/{año}")
@calcular_tiempo_ejecucion  # Aplicamos el decorador
async def UsersRecommend(año: int):
    # Paso 1: Filtrar las reseñas por el año especificado y donde recommend es verdadero
    reseñas_filtradas = df_user_reviews[(df_user_reviews['posted'].dt.year == año) & (df_user_reviews['recommend'] == True)]

    if reseñas_filtradas.empty:
        return {"message": f"No se encontraron reseñas recomendadas para el año {año}."}

    # Paso 2: Unir el DataFrame filtrado con df_steam_games
    df = pd.merge(reseñas_filtradas, df_steam_games, left_on='item_id', right_on='id')

    # Paso 3: Calcular la cantidad de reseñas positivas o neutrales para cada juego
    reseñas_positivas_neutrales = df[(df['sentiment_analysis'] == 1) | (df['sentiment_analysis'] == 2)]
    juegos_con_recomendaciones = reseñas_positivas_neutrales.groupby('app_name')['id_x'].count().reset_index()

    # Paso 4: Clasificar los juegos en función de la cantidad de reseñas positivas o neutrales
    juegos_ordenados = juegos_con_recomendaciones.sort_values(by='id_x', ascending=False)

    # Paso 5: Seleccionar los 3 juegos principales y devolverlos
    top_3_juegos = juegos_ordenados.head(3)

    return top_3_juegos.to_dict(orient="records")

@app.get("/users_not_recommend/{año}")
@calcular_tiempo_ejecucion  # Aplicamos el decorador
async def UsersNotRecommend(año: int):
    # Paso 1: Filtrar las reseñas por el año especificado y donde recommend es falso
    reseñas_filtradas = df_user_reviews[(df_user_reviews['posted'].dt.year == año) & (df_user_reviews['recommend'] == False)]

    if reseñas_filtradas.empty:
        return {"message": f"No se encontraron reseñas no recomendadas para el año {año}."}

    # Paso 2: Unir el DataFrame filtrado con df_steam_games
    df = pd.merge(reseñas_filtradas, df_steam_games, left_on='item_id', right_on='id')

    # Paso 3: Filtrar las reseñas negativas
    reseñas_negativas = df[df['sentiment_analysis'] == 0]

    if reseñas_negativas.empty:
        return {"message": f"No se encontraron reseñas negativas para el año {año}."}

    # Paso 4: Calcular la cantidad de reseñas negativas para cada juego
    juegos_con_reseñas_negativas = reseñas_negativas.groupby('app_name')['id_x'].count().reset_index()

    # Paso 5: Clasificar los juegos en función de la cantidad de reseñas negativas
    juegos_ordenados = juegos_con_reseñas_negativas.sort_values(by='id_x', ascending=False)

    # Paso 6: Seleccionar los 3 juegos principales y devolverlos
    top_3_juegos_no_recomendados = juegos_ordenados.head(3)

    return top_3_juegos_no_recomendados.to_dict(orient="records")

@app.get("/sentiment_analysis/{año}")
@calcular_tiempo_ejecucion  # Aplicamos el decorador
async def sentiment_analysis(año: int):
    # Paso 1: Filtrar las reseñas por el año especificado
    reseñas_por_año = df_user_reviews[df_user_reviews['posted'].dt.year == año]

    if reseñas_por_año.empty:
        return {"message": f"No se encontraron reseñas para el año {año}."}

    # Paso 2: Contar la cantidad de registros de reseñas categorizados con un análisis de sentimiento
    cantidad_sentimiento = reseñas_por_año['sentiment_analysis'].value_counts().reset_index()
    cantidad_sentimiento.columns = ['sentiment', 'count']

    # Paso 3: Devolver la lista de categorías de sentimiento y su cantidad
    return cantidad_sentimiento.to_dict(orient="records")
