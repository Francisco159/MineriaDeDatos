import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ast

def crear_df(archivo: str) -> pd.DataFrame:
    df = pd.read_csv(archivo)
    return df

def graficar_prom_imdb_score_por_anio_y_tipo(dfc: pd.DataFrame, columna: str):
    # Convertir la columna 'release_year' a datetime y luego extraer el año
    dfc['release_year'] = pd.to_datetime(dfc['release_year'], errors='coerce').dt.year

    # Agrupar por 'release_year' y 'type' y calcular el promedio de la columna
    grouped_df = dfc.groupby(['release_year', 'type'])[columna].mean().reset_index()

    # Separar los datos por tipo
    movies_df = grouped_df[grouped_df['type'] == 'MOVIE']
    shows_df = grouped_df[grouped_df['type'] == 'SHOW']

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar los datos
    ax.plot(movies_df['release_year'], movies_df[columna], label='Movie', marker='o')
    ax.plot(shows_df['release_year'], shows_df[columna], label='Show', marker='o')

    #Agregar títulos y etiquetas
    ax.set_title(f'Promedio de {columna} por Año y Tipo')
    ax.set_xlabel('Año')
    ax.set_ylabel(f'{columna} Promedio')
    ax.legend()

    # Mostrar la gráfica
    plt.savefig(f'../img_prac3/{columna}.png')
    plt.close()

def grafica_pastel_conteo_de_titulos_por_tipo(dfc: pd.DataFrame):
    df_type = dfc.groupby('type')['title'].count()
    
    labels = 'SHOW', 'MOVIE'
    sizes = [df_type['SHOW'], df_type['MOVIE']]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%')
    plt.savefig(f'../img_prac3/conteo_titulos_por_tipo.png')
    plt.close()

def grafica_conteo_titulos_por_genero(tipo: str, dfc: pd.DataFrame):
    shows_df = dfc[dfc['type'] == tipo]

    # Inicializar un contador para los géneros
    contando_generos = Counter()

    # Contar géneros
    for generos in shows_df['genres']:
        # Convertir la cadena de texto a una lista
        lista_generos_eval = ast.literal_eval(generos)
        # Actualizar el contador
        contando_generos.update(lista_generos_eval)
        
    # Rellenar las listas de géneros y contadores
    lista_generos = list(contando_generos.keys())
    lista_contador = list(contando_generos.values())

    # Asegurar que la lista de colores tenga la misma longitud que los géneros
    colores = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange'] * (len(lista_generos) // 4 + 1)
    colores = colores[:len(lista_generos)]
    

    plt.figure(figsize=(12, 8))
    bars = plt.bar(lista_generos, lista_contador, color=colores)
    plt.xlabel('Géneros')
    plt.ylabel('Contador')
    plt.title(f'Contador de géneros para {tipo}s')
    plt.xticks(rotation=45)
    plt.savefig(f'../img_prac3/conteo_titulos_{tipo}_por_genero.png')
    plt.close()
    
def grafica_conteo_titulos_por_anio(dfc: pd.DataFrame):
    titulos_anios = dfc.groupby('release_year')['title'].count()
    # Convertir los índices (años) y los valores (contadores) en listas separadas
    list_anios = titulos_anios.index.tolist()
    list_count = titulos_anios.values.tolist()

    plt.stem(list_anios, list_count)
    plt.savefig('../img_prac3/conteo_titulos_por_anio.png')

    

if __name__ == '__main__':
    df = crear_df('../data/new_csv_titles.csv')
    graficar_prom_imdb_score_por_anio_y_tipo(df, 'imdb_score')
    grafica_pastel_conteo_de_titulos_por_tipo(df)
    grafica_conteo_titulos_por_genero('SHOW', df)
    grafica_conteo_titulos_por_genero('MOVIE', df)
    grafica_conteo_titulos_por_anio(df)
