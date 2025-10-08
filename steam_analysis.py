import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv("steam_games_last10years.csv")

silksong_info = df[df["AppID"] == "1030300"]
print(silksong_info)


#===================================1=======================================
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

#====================================2===================================
# Filtrar solo juegos difíciles
df_dificiles = df[df["Dificultad"] == 1].copy()

#Calcular horas totales estimadas
if "CCU" in df.columns:
    df_dificiles["HorasTotalesEstimadas"] = df_dificiles["AverageForever"] * df_dificiles["CCU"]
else:
    print("⚠️ No se encontró la columna 'CCU', se omitirá HorasTotalesEstimadas.")
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
#Dispersión con línea de regresión
plt.figure(figsize=(10,6))
sns.regplot(
    data=df_dificiles,
    x="ReleaseYear",
    y="AverageForever",
    scatter_kws={'alpha':0.6},
    line_kws={'color':'red'}
)

plt.title("Tiempo promedio jugado vs Año de lanzamiento (Juegos difíciles)")
plt.xlabel("Año de lanzamiento")
plt.ylabel("Horas promedio jugadas (AverageForever)")
plt.grid(True, alpha=0.3)
plt.show()

#=======================================3=====================================
#Horas totales estimadas por año (indicador empresarial)
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