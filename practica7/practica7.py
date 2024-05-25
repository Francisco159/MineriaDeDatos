import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List 

def generate_df(data: pd.DataFrame) -> pd.DataFrame:
    # Assuming 'imdb_score' and 'tmdb_score' are relevant columns for clustering
    return data[['imdb_score', 'tmdb_score']]

def scatter_group_by(file_path: str, df: pd.DataFrame, x_column: str, y_column: str, label_column: str):
    fig, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = plt.cm.get_cmap('hsv', len(labels) + 1)
    for i, label in enumerate(labels):
        filter_df = df[df[label_column] == label]
        ax.scatter(filter_df[x_column], filter_df[y_column], label=label, color=cmap(i))
    ax.legend()
    plt.savefig(file_path)
    plt.close()

def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))

def k_means(points: List[np.array], k: int):
    DIM = len(points[0])
    N = len(points)
    num_cluster = k
    iterations = 15

    x = np.array(points)
    y = np.random.randint(0, num_cluster, N)

    mean = np.zeros((num_cluster, DIM))
    for t in range(iterations):
        for k in range(num_cluster):
            mean[k] = np.mean(x[y == k], axis=0)

        for i in range(N):
            dist = np.sum((mean - x[i]) ** 2, axis=1)
            pred = np.argmin(dist)
            y[i] = pred

    for kl in range(num_cluster):
        xp = x[y == kl, 0]
        yp = x[y == kl, 1]
        plt.scatter(xp, yp)
    plt.savefig("../img_prac7/kmeans.png")
    plt.close()
    return mean

# Generar DataFrame de nuestro conjunto de datos
data = pd.read_csv("../data/new_csv_titles.csv")  
df = generate_df(data)

# Visualizar el DataFrame antes de aplicar K-means
print(df.head())

# Aplicar K-means
points = df.to_numpy()
kn = k_means(points, 3)  # Cambiar el número de clusters según sea necesario
print("Centroides de los clusters:", kn)

# Visualizar los resultados de K-means
scatter_group_by("../img_prac7/clusters.png", df, "imdb_score", "tmdb_score", "type")
