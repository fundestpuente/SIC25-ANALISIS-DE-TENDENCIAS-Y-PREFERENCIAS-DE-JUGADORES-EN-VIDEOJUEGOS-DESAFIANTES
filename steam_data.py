import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm

#Descargar datos de SteamSpy (top juegos forever)
print("🔍 Descargando datos de SteamSpy (top juegos, últimos 10 años)...")

# Usamos top 100 juegos para no sobrecargar la PC
url = "https://steamspy.com/api.php?request=top100forever"  # más ligero que 'all'
response = requests.get(url)
data_all = response.json()

for i, (appid, info) in enumerate(data_all.items()):
    print(f"\nAppID: {appid}")
    print(json.dumps(info, indent=2))
    if i >= 2:  # solo los primeros 3
        break

juegos = []
for appid, info in tqdm(data_all.items()):
    try:
        juegos.append({
            "AppID": appid,
            "Nombre": info.get("name", ""),
            "Developer": info.get("developer", ""),
            "Publisher": info.get("publisher", ""),
            "ScoreRank": info.get("score_rank", ""),
            "Owners": info.get("owners", ""),
            "AverageForever": info.get("average_forever", 0),
            "Average2Weeks": info.get("average_2weeks", 0),
            "MedianForever": info.get("median_forever", 0),
            "Median2Weeks": info.get("median_2weeks", 0),
            "CCU": info.get("ccu", 0),
            "Price": info.get("price", "0"),
            "InitialPrice": info.get("initialprice", "0"),
            "Discount": info.get("discount", "0"),
        })
    except:
        continue


#Crear DataFrame
df = pd.DataFrame(juegos)

# Asegurarse de que exista la columna 'Tags'
if 'Tags' not in df.columns:
    df['Tags'] = ""

#Calcular dificultad aproximada

keywords_dificil = ["Difficult", "Souls-like", "Hardcore"]
df['Dificultad'] = 0

#Guardar CSV
df.to_csv("steam_games_last10years.csv", index=False, encoding="utf-8-sig")
print(f"✅ Dataset generado con {len(df)} juegos. Guardado en steam_games_last10years.csv")
