import ast
from collections import Counter
import pandas as pd 

def crear_df(archivo: str) -> pd.DataFrame:
    df = pd.read_csv(archivo)
    return df

def titulo():
    print("--------------------------------------------------------------------")
    print('ESTADISTICA DESCRIPTIVA')
    print("--------------------------------------------------------------------\n\n")
    print("--------------------------------------------------------------------")

# min - max

def min_max_titulos_por_duracion(tipo: str, dfc: pd.DataFrame):
    mostrar_df_por_tipos = dfc[dfc['type'] == tipo]
    max_duracion = mostrar_df_por_tipos['runtime'].max()
    min_duracion = mostrar_df_por_tipos['runtime'].min()
    titulo_max_duracion = mostrar_df_por_tipos[mostrar_df_por_tipos['runtime'] == max_duracion]
    titulo_min_duracion = mostrar_df_por_tipos[mostrar_df_por_tipos['runtime'] == min_duracion]
    if tipo == 'SHOW':
        print("Serie con mayor duracion (en minutos):")
        print(f"{titulo_max_duracion[['title', 'runtime']]}")
        print("Serie con menor duracion (en minutos):")
        print(f"{titulo_min_duracion[['title', 'runtime']]}")
    elif tipo == 'MOVIE':
        print("Pelicula con mayor duracion (en minutos):")
        print(f"{titulo_max_duracion[['title', 'runtime']]}")
        print("Pelicula con menor duracion (en minutos):")
        print(f"{titulo_min_duracion[['title', 'runtime']]}")

def min_max_titulos_por_columnas_imdb_tmdb(dfc: pd.DataFrame, campo: str):
    mostrar_df_por_show = dfc[dfc['type'] == 'SHOW']
    mostrar_df_por_movie = dfc[dfc['type'] == 'MOVIE']
    max_campo_show = mostrar_df_por_show[campo].max()
    min_campo_show = mostrar_df_por_show[campo].min()
    max_campo_movie = mostrar_df_por_movie[campo].max()
    min_campo_movie = mostrar_df_por_movie[campo].min()
    titulo_max_campo_show = mostrar_df_por_show[mostrar_df_por_show[campo] == max_campo_show]
    titulo_min_campo_show = mostrar_df_por_show[mostrar_df_por_show[campo] == min_campo_show]
    titulo_max_campo_movie = mostrar_df_por_movie[mostrar_df_por_movie[campo] == max_campo_movie]
    titulo_min_campo_movie = mostrar_df_por_movie[mostrar_df_por_movie[campo] == min_campo_movie]
    print(f"Serie con mayor {campo}:")
    print(f"{titulo_max_campo_show[['title', campo]]}")
    print("--------------------------------------------------------------------")
    print(f"Serie con menor {campo}:")
    print(f"{titulo_min_campo_show[['title', campo]]}")
    print("--------------------------------------------------------------------")
    print(f"Pelicula con mayor {campo}:")
    print(f"{titulo_max_campo_movie[['title', campo]]}")
    print("--------------------------------------------------------------------")
    print(f"Pelicula con menor {campo}:")
    print(f"{titulo_min_campo_movie[['title', campo]]}")

# conteos

def contar_titulos_por_tipo(dfc: pd.DataFrame):
    print('Conteo de titulos por tipo (SHOW, MOVIE)')
    df_type = dfc.groupby('type')['title'].count()
    print(df_type)

def contar_titulos_por_genero(tipo: str, dfc: pd.DataFrame):
    shows_df = dfc[dfc['type'] == tipo]

    # Inicializar un contador para los géneros
    contando_generos = Counter()

    # Contar géneros
    for generos in shows_df['genres']:
        # Convertir la cadena de texto a una lista
        lista_generos = ast.literal_eval(generos)
        # Actualizar el contador
        contando_generos.update(lista_generos)

    if tipo == 'SHOW':
        print("Titulos por genero del tipo SHOW")
    elif tipo == 'MOVIE':
        print("Titulos por genero del tipo MOVIE")

    # Imprimir los resultados
    for generos, contador in contando_generos.items():
        print(f'{generos} ----> {contador}')

def contar_titulos_por_anio(dfc: pd.DataFrame):
    titulos_anios = dfc.groupby('release_year')['title'].count()
    print(titulos_anios)

# sumatoria

def sumatoria_imdb_tmdb_por_anio(dfc: pd.DataFrame):
    suma_imdb_score = dfc.groupby('release_year')['imdb_score'].sum()
    suma_imdb_votes = dfc.groupby('release_year')['imdb_votes'].sum()
    suma_tmdb_popularity = dfc.groupby('release_year')['tmdb_popularity'].sum()
    suma_tmdb_score = dfc.groupby('release_year')['tmdb_score'].sum()
    print("Suma de imdb_score por anio")
    print(suma_imdb_score)
    print("--------------------------------------------------------------------")
    print("Suma de imdb_votes por anio")
    print(suma_imdb_votes)
    print("--------------------------------------------------------------------")
    print("Suma de tmdb_popularity por anio")
    print(suma_tmdb_popularity)
    print("--------------------------------------------------------------------")
    print("Suma de tmdb_score por anio")
    print(suma_tmdb_score)

# moda

def moda_generos_por_tipo_y_anio(dfc: pd.DataFrame):
    
    # Convertir la columna 'release_year' a datetime y luego extraer el año
    dfc['release_year'] = pd.to_datetime(dfc['release_year'], errors='coerce').dt.year

    # Convertir la columna 'genres' de cadenas a listas
    dfc['genres'] = dfc['genres'].apply(ast.literal_eval)
    
    # Inicializar un diccionario para almacenar los resultados
    results = {}

    # Iterar por cada año único
    for year in dfc['release_year'].unique():
        results[year] = {}
    
        # Filtrar los datos por año
        df_year = dfc[dfc['release_year'] == year]
    
        # Filtrar por tipo (SHOW y MOVIE) y contar géneros
        for content_type in ['SHOW', 'MOVIE']:
            df_type = df_year[df_year['type'] == content_type]
        
            # Contar la frecuencia de cada género
            genre_counter = Counter()
            for genres in df_type['genres']:
                genre_counter.update(genres)
        
            # Encontrar el género más común
            if genre_counter:
                most_common_genre, count = genre_counter.most_common(1)[0]
                results[year][content_type] = (most_common_genre, count)

    # Imprimir los resultados
    for year, types in results.items():
        print(f"{year}:")
        for content_type, (genre, count) in types.items():
            print(f"{content_type} ----> {genre} ---> {count} apariciones")

# media

def media_imdb_tmdb_por_tipo_anio(dfc: pd.DataFrame, columna: str):
    
    # Convertir la columna 'release_year' a datetime y luego extraer el año
    dfc['release_year'] = pd.to_datetime(dfc['release_year'], errors='coerce').dt.year
    
    # Agrupar por 'release_year' y 'type' y calcular el promedio de la columna
    grouped_df = dfc.groupby(['release_year', 'type'])[columna].mean().reset_index()

    if columna == 'imdb_score':
        print(f"Promedio de {columna} por cada tipo y anio")
    elif columna == 'imdb_votes':
        print(f"Promedio de {columna} por cada tipo y anio")
    elif columna == 'tmdb_popularity':
        print(f"Promedio de {columna} por cada tipo y anio")
    elif columna == 'tmdb_score':
        print(f"Promedio de {columna} por cada tipo y anio")

    # Imprimir los resultados
    for year in grouped_df['release_year'].unique():
        print(f"{year}:")
        year_df = grouped_df[grouped_df['release_year'] == year]
        for index, row in year_df.iterrows():
            print(f"{row['type'].lower()} ----> prom: {row[columna]:.1f}")


if __name__ == "__main__":
    df = crear_df('../data/new_csv_titles.csv')
    titulo()
    min_max_titulos_por_duracion('SHOW', df)
    print("--------------------------------------------------------------------")
    min_max_titulos_por_duracion('MOVIE', df)
    print("--------------------------------------------------------------------")
    min_max_titulos_por_columnas_imdb_tmdb(df, 'imdb_score')
    print("--------------------------------------------------------------------")
    min_max_titulos_por_columnas_imdb_tmdb(df, 'imdb_votes')
    print("--------------------------------------------------------------------")
    min_max_titulos_por_columnas_imdb_tmdb(df, 'tmdb_popularity')
    print("--------------------------------------------------------------------")
    min_max_titulos_por_columnas_imdb_tmdb(df, 'tmdb_score')
    print("--------------------------------------------------------------------")

    contar_titulos_por_tipo(df)
    print("--------------------------------------------------------------------")
    contar_titulos_por_genero('SHOW', df)
    print("--------------------------------------------------------------------")
    contar_titulos_por_genero('MOVIE', df)
    print("--------------------------------------------------------------------")
    contar_titulos_por_anio(df)
    print("--------------------------------------------------------------------")
    
    sumatoria_imdb_tmdb_por_anio(df)
    print("--------------------------------------------------------------------")

    moda_generos_por_tipo_y_anio(df)
    print("--------------------------------------------------------------------")

    media_imdb_tmdb_por_tipo_anio(df, 'imdb_score')
    print("--------------------------------------------------------------------")
    media_imdb_tmdb_por_tipo_anio(df, 'imdb_votes')
    print("--------------------------------------------------------------------")
    media_imdb_tmdb_por_tipo_anio(df, 'tmdb_popularity')
    print("--------------------------------------------------------------------")
    media_imdb_tmdb_por_tipo_anio(df, 'tmdb_score')
    print("--------------------------------------------------------------------")