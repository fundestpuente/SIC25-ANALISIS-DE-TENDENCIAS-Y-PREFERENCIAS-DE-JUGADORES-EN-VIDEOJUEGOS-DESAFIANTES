import pandas as pd
import matplotlib.pyplot as plt


df= pd.read_csv("steam_games_last10years.csv")

# Imprimir las primeras 30 filas
print(df.head())

#minutos a horas
df["AverageForever"] = df["AverageForever"] / 60  

# Agrupar por anio y dificultad, y calcular promedio
promedio_por_anio = (
    df.groupby(["ReleaseYear", "Dificultad"])["AverageForever"]
    .mean()
    .reset_index()
    .sort_values("ReleaseYear")
)

# Separar los datos
dificiles = promedio_por_anio[promedio_por_anio["Dificultad"] == 1]
faciles = promedio_por_anio[promedio_por_anio["Dificultad"] == 0]

# 📈 Graficar
plt.figure(figsize=(10,6))
plt.plot(faciles["ReleaseYear"], faciles["AverageForever"], marker="o", label="Faciles", color="green", linewidth=2)
plt.plot(dificiles["ReleaseYear"], dificiles["AverageForever"], marker="o", label="Dificiles", color="red", linewidth=2)

plt.title("Promedio de tiempo jugado por anio: juegos faciles vs dificiles", fontsize=14)
plt.xlabel("Anio de lanzamiento")
plt.ylabel("Tiempo jugado promedio (horas)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()