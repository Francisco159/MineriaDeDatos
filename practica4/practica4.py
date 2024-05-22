import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import shapiro, levene
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def anova(df_aux: pd.DataFrame, str_ols: str):
    # Ajustar el modelo
    model = ols(str_ols, data=df_aux).fit()
    
    # Prueba de Shapiro-Wilk para la normalidad de los residuos
    shapiro_test = shapiro(model.resid)
    
    # Prueba de Levene para la homogeneidad de varianzas
    levene_test = levene(*[df_aux['imdb_score'][df_aux['type'] == grupo] for grupo in df_aux['type'].unique()])
    
    # ANOVA
    anova_df = sm.stats.anova_lm(model, typ=2)
    
    # Imprimir los resultados de las pruebas de normalidad y homogeneidad
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")
    print("\nLevene's Test:")
    print(f"Statistic: {levene_test.statistic}, p-value: {levene_test.pvalue}")
    
    # Imprimir los resultados del ANOVA y realizar la prueba de Tukey si es significativo
    if anova_df["PR(>F)"][0] < 0.05:
        print("Hay diferencias significativas")
        print(anova_df)
        
        # Prueba post-hoc de Tukey
        tukey_result = pairwise_tukeyhsd(endog=df_aux['imdb_score'], groups=df_aux['type'], alpha=0.05)
        print("\nResultados de la prueba de Tukey:")
        print(tukey_result)
    else:
        print("No hay diferencias significativas")
        print(anova_df)

def anova_1(file_name: str):
    df_complete = pd.read_csv(file_name)
    
    # Convertir la columna 'release_year' a datetime y luego extraer el año
    df_complete['release_year'] = pd.to_datetime(df_complete['release_year'], errors='coerce').dt.year
    
    # Eliminar filas con valores NaN en 'imdb_score', 'release_year' o 'type'
    df_complete = df_complete.dropna(subset=['imdb_score', 'release_year', 'type'])
    
    # Filtrar los datos relevantes y renombrar la columna 'imdb_score'
    df_aux = df_complete[['release_year', 'type', 'imdb_score']]
    
    print(df_aux.head())
    
    # Realizar el ANOVA
    anova(df_aux, "imdb_score ~ C(release_year) + C(type)")

# Llamar a la función con el nombre del archivo CSV
anova_1('../data/new_csv_titles.csv')
