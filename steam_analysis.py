import pandas as pd
import matplotlib.pyplot as plt


df= pd.read_csv("steam_games_last10years.csv")

# Imprimir las primeras 30 filas
print(df.head(30))

# Filtrar juegos difíciles
df_dificiles = df[df["Dificultad"] == 1]


#Calcular promedio
promedio_por_anio = (
    df_dificiles.groupby("ReleaseYear")["AverageForever"]
    .mean()
    .reset_index()
    .sort_values("ReleaseYear")
)

plt.figure(figsize=(10,6))
plt.plot(promedio_por_anio["ReleaseYear"], promedio_por_anio["AverageForever"], marker="o", linewidth=2)
plt.title("Promedio de tiempo jugado en juegos difíciles por año", fontsize=14)
plt.xlabel("Año de lanzamiento")
plt.ylabel("Tiempo jugado promedio (minutos)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()