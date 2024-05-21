import ast
import pandas as pd 

db = pd.read_csv("../data/titles.csv")

# crear copia de dataframe
df2 = db

# funciones que llegue a usar en el archivo
# Función para descomponer las listas de géneros
def extract_genres(genre_str):
    return ast.literal_eval(genre_str)

# Aplicar la función para descomponer las listas de géneros
df2['genres'] = df2['genres'].apply(extract_genres)

# limpiar nulos por ceros
df2['imdb_score'].fillna(0, inplace=True)
df2['imdb_votes'].fillna(0, inplace=True)
df2['tmdb_popularity'].fillna(0, inplace=True)
df2['tmdb_score'].fillna(0, inplace=True)

# cambiar fecha a datatime
df2['release_year'] = pd.to_datetime(df2['release_year'].map(str), format="%Y")

# Filtrar filas donde 'genres' no está vacío
df2 = df2[df2['genres'].map(len) > 0]

# exportar el dataframe resultante de la limpia de datos
df2.to_csv('../data/new_csv_titles.csv', index=False)

# impresion de datos
print(df2.head())




