# Proyecto Individual: Sistema de Recomendación de videojuegos

## Desarrollo de un Sistema de Recomendación de Películas
¡Bienvenido/a al proyecto individual número 1! En este proyecto, nos enfocaremos en el desarrollo de un sistema de recomendación de videojuegos para la plataforma Steams. A través de diferentes etapas, como el ETL, análisis exploratorio de datos (EDA) y la implementación de un modelo de Machine Learning, buscamos crear un sistema que recomiende videojuegos basados en las preferencias basado en los datos provistos de años anteriores.

## Descripción del problema y rol a desarrollar
El objetivo principal de este proyecto es desarrollar un sistema de recomendación de videojuegos que proporcione sugerencias personalizadas a los usuarios. Asumiremos el rol de un MLops Engineer y trabajaremos en la extracción, transformación y carga de datos (ETL), el análisis exploratorio de datos (EDA) y el desarrollo de un modelo de Machine Learning para implementar el sistema de recomendación.

## ETL (Extracción, Transformación y Carga)
Fueron entregados tres archivos JSON comprimidos en formato GZip, identificados como steam_games.json.gz, user_reviews.json.gz y users_item.json.gz. Se emplearon funciones específicas para la extracción de los datos debido a la complejidad de su estructura. Estos archivos presentaban datos anidados, valores nulos, duplicados y, en algunos casos, requerían ajustes en su formato. Además, se llevó a cabo un proceso de análisis de sentimientos mediante la creación de la columna 'sentiment_analysis', utilizando la librería TextBlob.

Posteriormente, tras desanidar y limpiar los conjuntos de datos, se realizó un análisis detallado para identificar las funciones y los datos necesarios para cada caso. Se procedió a agrupar columnas y generar nuevos conjuntos de datos específicos, adaptados a los requisitos de cada función. Esta estrategia no solo contribuyó a optimizar el tamaño de los conjuntos de datos, sino que también permitió una gestión más eficiente de los recursos disponibles.

Finalmente, los conjuntos de datos fueron exportados en formato .csv y se pusieron en uso.

## EDA (Análisis Exploratorio de Datos)
Durante el proceso de análisis exploratorio de datos, logré identificar diversas características clave, tales como los géneros de los juegos, la evolución de los juegos recomendados a lo largo de los años y un recuento detallado del análisis de sentimientos. Sin embargo, es importante destacar que mi análisis de los datos se llevó a cabo de manera integral durante la etapa de extracción, transformación y carga (ETL), donde se realizó una cuidadosa selección de las columnas necesarias en función de las funciones específicas que se requerían.

## Desarrollo de la API
Se ha encomendado la creación de cinco funciones utilizando FASTAPI, específicamente las siguientes: PlayTimeGenre, UserForGenre, UsersRecommend, UsersNotRecommend y Sentiment_Analysis. El proceso de desarrollo de los puntos finales se llevó a cabo inicialmente en el archivo Endpoints.ipynb, donde se realizaron pruebas y se evaluaron los resultados obtenidos. Posteriormente, se trasladaron dichos resultados al archivo main.py, que se encargará de consumir la API implementando los decoradores necesarios para su funcionamiento adecuado.

## Modelo de ML 
Se entrenó un modelo de Machine Learning para hacer un sistema de recomendación de juegos para los usuarios. Se realizó una función llamada "recomendacion_usuario" que se usará con un método POST en FASTAPI.

## Deployment
Para desplegar la API en Render, configuramos la aplicación, cargamos el código, ajustamos la configuración del servidor y realizamos pruebas exhaustivas. Una vez en producción, monitoreamos su rendimiento para garantizar su disponibilidad y funcionalidad óptimas.

Les invito a visitar mi perfil de [Linkedin](https://www.linkedin.com/in/mauro-pereyro/) 
*Mauro Pereyro*
