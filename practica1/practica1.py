import pandas as pd 

db = pd.read_csv("../data/titles.csv")

# crear copia de dataframe
df2 = db

# limpiar nulos por ceros
df2['imdb_score'].fillna(0, inplace=True)
df2['imdb_votes'].fillna(0, inplace=True)
df2['tmdb_popularity'].fillna(0, inplace=True)
df2['tmdb_score'].fillna(0, inplace=True)

# cambiar fecha a datatime
df2['release_year'] = pd.to_datetime(df2['release_year'].map(str), format="%Y")

# exportar el dataframe resultante de la limpia de datos
df2.to_csv('../data/new_csv_titles.csv', index=False)

# impresion de datos
print(df2.head())




