import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers
import pandas as pd
from tabulate import tabulate
from statsmodels.stats.outliers_influence import summary_table
from typing import Tuple, Dict
import numpy as np

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))

def transform_variable(df: pd.DataFrame, x:str)->pd.Series:
    if isinstance(df[x][df.index[0]], numbers.Number):
        return df[x] # type: pd.Series
    elif x == 'release_year':  # Verificamos si la columna es 'release_year'
        return pd.to_datetime(df[x])  # Convertimos la columna a tipo fecha
    else:
        return pd.Series([i for i in range(0, len(df[x]))])

def linear_regression(df: pd.DataFrame, x:str, y: str)->Dict[str, float]:
    fixed_x = transform_variable(df, x)
    if x == 'release_year':  # Verificamos si la columna es 'release_year'
        fixed_x = fixed_x.dt.year.astype(float)  # Convertimos el año a tipo float
    model = sm.OLS(df[y], sm.add_constant(fixed_x)).fit()
    return {'m': model.params[1], 'b': model.params[0], 'r2': model.rsquared, 'r2_adj': model.rsquared_adj}

def plt_lr(df: pd.DataFrame, x:str, y: str, m: float, b: float, r2: float, r2_adj: float, colors: Tuple[str,str]):
    fixed_x = transform_variable(df, x)
    if x == 'release_year':  # Verificamos si la columna es 'release_year'
        fixed_x = fixed_x.dt.year.astype(float)  # Convertimos el año a tipo float
    plt.scatter(df[x], df[y], color=colors[0], label='Data')
    plt.plot(fixed_x, m * fixed_x + b, color=colors[1], label='Regression Line')  # Aquí usamos fixed_x en lugar de df[x]
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title('Linear Regression')
    plt.legend()
    plt.savefig('../img_prac8/forecasting.png')
    plt.close()

# Aquí se leen los datos del DataFrame, reemplaza 'df' con tu DataFrame
df = pd.read_csv('../data/new_csv_titles.csv')  

# Ajusta los nombres de las columnas según tu conjunto de datos
x = "release_year"
y = "imdb_votes"

#Realiza la regresión lineal y grafica los resultados
result = linear_regression(df, x, y)
print("Coeficiente m:", result['m'])
print("Intercepto b:", result['b'])
print("R-cuadrado:", result['r2'])
print("R-cuadrado ajustado:", result['r2_adj'])
plt_lr(df, x, y, result['m'], result['b'], result['r2'], result['r2_adj'], colors=('blue', 'red'))
