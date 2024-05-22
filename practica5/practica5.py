import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers
import pandas as pd
import numpy as np
from tabulate import tabulate
import os
from io import StringIO

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))

def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x].iloc[0], numbers.Number):
        return df[x]  # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x: str, y: str) -> None:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(df[y], sm.add_constant(fixed_x)).fit()
    print(model.summary())

    coef = pd.read_html(StringIO(model.summary().tables[1].as_html()), header=0, index_col=0)[0]['coef']
    df.plot(x=x, y=y, kind='scatter')
    plt.plot(df[x], [df[y].mean() for _ in fixed_x], color='green')
    plt.plot(df[x], [coef.values[1] * val + coef.values[0] for val in fixed_x], color='red')
    plt.xticks(rotation=90)
    
    # Crear la carpeta si no existe
    output_dir = 'img_prac5'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(os.path.join(output_dir, f'lr_{y}_{x}.png'))
    plt.close()

# Cargar los datos
df = pd.read_csv("../data/new_csv_titles.csv")  

# Eliminar filas con valores NaN en 'imdb_score' o 'release_year'
df = df.dropna(subset=['imdb_score', 'release_year'])

# Agrupar por año y calcular el promedio de imdb_score
df_by_year = df.groupby('release_year').agg(imdb_score_avg=('imdb_score', 'mean'))
df_by_year.reset_index(inplace=True)

# Imprimir los primeros registros
print_tabulate(df_by_year.head())

# Realizar la regresión lineal
linear_regression(df_by_year, "release_year", "imdb_score_avg")
