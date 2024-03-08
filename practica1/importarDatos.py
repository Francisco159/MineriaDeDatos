import pandas as pd 
from tabulate import tabulate

df = pd.read_csv('animes2.csv')
print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))



"""  obtener de los primeros registros cuales tienen el genero "Comedy"
for i in range(0, 20):
    generos = df.iloc[i, 2]
    if "Comedy" in generos:
        print(df.iloc[i, 1])"""
    

"""  -- practicando -- saber que tipo de dato son cada columna
for i in range(8):
    tipo = type(df.iloc[0, i])
    columna = df.columns[i]
    print(columna, '    tipo de dato:', tipo) 
"""


