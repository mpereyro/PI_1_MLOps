import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Cargar el archivo Parquet
items_games_filtrado = pd.read_parquet('DATOS/summary_df.parquet')

# Ruta raíz
@app.get("/")
async def read_root():
    return {"message": "¡La aplicación está funcionando!"}

# Ruta para la función PlayTimeGenre
@app.get("/PlayTimeGenre/{genero}")
async def get_play_time_genre(genero: str):
    """
    Devuelve el año con más horas jugadas para el género especificado.

    Args:
        genero (str): Género del juego
    Returns:
        dict: Diccionario con el género y el año de lanzamiento con más horas jugadas
    """
    # Filtrar el DataFrame para el género específico
    df_genre = items_games_filtrado[items_games_filtrado['Género'] == genero]

    # Encontrar el año con más horas jugadas para el género dado
    max_hours_year = df_genre.loc[df_genre['Total_Horas_Jugadas'].idxmax()]['Año_Max_Horas_Jugadas']

    return {f'Año de lanzamiento con más horas jugadas para el género {genero}': int(max_hours_year)}
