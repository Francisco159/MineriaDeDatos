import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 
from typing import Tuple, Dict, List
import numpy as np
from functools import reduce
from scipy.stats import mode


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))


def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))


def k_nearest_neighbors(
    points: List[np.array], labels: np.array, input_data: List[np.array], k: int
):
    # Convertir todas las etiquetas a cadenas de texto (str)
    labels = labels.astype(str)

    input_distances = [
        [euclidean_distance(input_point, point) for point in points]
        for input_point in input_data
    ]
    points_k_nearest = [
        np.argsort(input_point_dist)[:k] for input_point_dist in input_distances
    ]
    return [
        np.unique([labels[index] for index in point_nearest], return_counts=True)[0][
            np.argmax(
                np.unique([labels[index] for index in point_nearest], return_counts=True)[
                    1
                ]
            )
        ]
        for point_nearest in points_k_nearest
    ]

def scatter_group_by(
    file_path: str, df: pd.DataFrame, x_column: str, y_column: str, label_column: str
):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = mcolors.ListedColormap([plt.cm.jet(i / len(labels)) for i in range(len(labels))])
    for i, label in enumerate(labels):
        filter_df = df.query(f"{label_column} == '{label}'")
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label, cmap=cmap(i))
    ax.legend()
    plt.savefig(file_path)
    plt.close()


# Cargar el dataset
df = pd.read_csv("../data/new_csv_titles.csv")

# Seleccionar columnas relevantes y limpiar datos
# Asegúrate de utilizar los nombres correctos de las columnas
df = df[['id', 'title', 'type', 'release_year', 'runtime', 'genres', 'imdb_score', 'imdb_votes', 'tmdb_popularity', 'tmdb_score']]
df = df.dropna()

# Crear etiquetas basadas en el puntaje IMDb (ejemplo: clasificar por score bajo, medio y alto)
bins = [0, 4, 7, 10]
labels = ['low', 'medium', 'high']
df['score_category'] = pd.cut(df['imdb_score'], bins=bins, labels=labels)

# Preparar datos para KNN
points = df[['imdb_score', 'tmdb_score']].values
categories = df['score_category'].values

# Nuevos puntos a clasificar
new_points = [
    np.array([7, 8]),  # Punto 1: imdb_score=7, tmdb_score=8
    np.array([5, 6]),  # Punto 2: imdb_score=5, tmdb_score=6
    np.array([8.5, 9])  # Punto 3: imdb_score=8.5, tmdb_score=9
]

# Aplicar KNN
k = 5
knn_result = k_nearest_neighbors(points, categories, new_points, k)

print(f"Nuevos puntos: {new_points}")
print(f"Clasificaciones: {knn_result}")

# Visualizar los datos y las nuevas clasificaciones
df_plot = pd.DataFrame(new_points, columns=['imdb_score', 'tmdb_score'])
df_plot['score_category'] = knn_result

scatter_group_by("../img_prac6/movie_knn.png", df, "imdb_score", "tmdb_score", "score_category")
