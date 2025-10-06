import pandas as pd

df= pd.read_csv("steam_games_last10years.csv")

# Configurar pandas para mostrar todo
pd.set_option('display.max_columns', None)   # Mostrar todas las columnas
pd.set_option('display.max_rows', 30)       # Mostrar 30 filas
pd.set_option('display.width', None)        # Evita cortes por ancho de pantalla
pd.set_option('display.max_colwidth', None) # Mostrar contenido largo completo

# Imprimir las primeras 30 filas
print(df.head(30))