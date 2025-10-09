import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv("steam_games.csv")
df = df[df["ReleaseYear"] <= 2024]
#===================================1=======================================
#minutos a horas
df["AverageForever"] = df["AverageForever"] / 60  


# Agrupar por año y dificultad, y calcular promedio
promedio_por_anio = (
    df.groupby(["ReleaseYear", "Dificultad"])["AverageForever"]
    .mean()
    .reset_index()
    .sort_values("ReleaseYear")
)

# Separar los datos
dificiles = promedio_por_anio[promedio_por_anio["Dificultad"] == 1]
faciles = promedio_por_anio[promedio_por_anio["Dificultad"] == 0]

#====================================3===================================
# Filtrar solo juegos difíciles
df_dificiles = df[df["Dificultad"] == 1].copy()

df_dificiles["HorasTotalesEstimadas"] = df_dificiles["AverageForever"]

# Graficas
#==================================1=========================================
plt.figure(figsize=(10,6))
plt.plot(faciles["ReleaseYear"], faciles["AverageForever"], marker="o", label="Faciles", color="green", linewidth=2)
plt.plot(dificiles["ReleaseYear"], dificiles["AverageForever"], marker="o", label="Dificiles", color="red", linewidth=2)

plt.title("Promedio de tiempo jugado por anio: juegos faciles vs dificiles", fontsize=14)
plt.xlabel("Año de lanzamiento")
plt.ylabel("Tiempo jugado promedio (horas)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

#======================================2========================================
promedio_dificiles = df_dificiles.groupby("ReleaseYear")["AverageForever"].mean()
plt.figure(figsize=(10,6))
plt.plot(promedio_dificiles.index, promedio_dificiles.values, marker="o", color="red")
plt.title("Promedio de horas jugadas por juegos difíciles por año")
plt.xlabel("Año de lanzamiento")
plt.ylabel("Horas promedio jugadas")
plt.grid(True, alpha=0.5)
plt.show()


#=======================================3=====================================
#Horas totales estimadas por año 
horas_por_anio = df_dificiles.groupby("ReleaseYear")["HorasTotalesEstimadas"].sum().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(
    data=horas_por_anio,
    x="ReleaseYear",
    y="HorasTotalesEstimadas",
    marker="o"
)
plt.title("Horas totales estimadas jugadas por año (Juegos difíciles)")
plt.xlabel("Año de lanzamiento")
plt.ylabel("Horas totales estimadas (AverageForever × CCU)")
plt.grid(True, alpha=0.3)
plt.show()

#=================================4===========================================
df_dificiles = df[df["Dificultad"]==1].copy()
plt.figure(figsize=(10,6))
plt.scatter(df_dificiles["ReleaseYear"], df_dificiles["AverageForever"], alpha=0.6, color="red")
plt.title("Horas jugadas vs Año de lanzamiento (juegos difíciles)")
plt.xlabel("Año de lanzamiento")
plt.ylabel("Horas promedio jugadas")
plt.ylim(0, 500)
plt.grid(True, alpha=0.3)
plt.show()

#================================5==================================================
# Gráfico circular
labels = ["Fáciles", "Difíciles"]
sizes = [df[df["Dificultad"]==0].shape[0], df[df["Dificultad"]==1].shape[0]]
colors = ["green", "red"]

plt.figure(figsize=(7,7))
plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, explode=(0.05, 0))
plt.title("Proporción de juegos difíciles vs fáciles")
plt.show()

