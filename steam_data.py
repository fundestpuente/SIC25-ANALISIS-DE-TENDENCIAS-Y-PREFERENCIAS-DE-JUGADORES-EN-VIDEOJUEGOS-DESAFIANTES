import requests
import json
import time
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
            "Tags": "",        # SteamSpy top100 no trae tags
            "Languages": "",   # No disponible en esta lista
            "Genres": "",      # No disponible en esta lista
        })
    except:
        continue


#Crear DataFrame
df = pd.DataFrame(juegos)
print(f"✅ Se descargaron {len(df)} juegos de SteamSpy.")


#Obtener tags desde la API de Steam Store
print("\nObteniendo tags (géneros y categorías) desde Steam Store...")

tags_list = []
for appid in tqdm(df["AppID"], desc="Consultando API Steam Store"):
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        r = requests.get(url, timeout=6)
        data = r.json()

        if not data or not data.get(str(appid), {}).get("success"):
            tags_list.append("")
            continue

        info = data[str(appid)]["data"]
        genres = [g["description"] for g in info.get("genres", [])]
        categories = [c["description"] for c in info.get("categories", [])]
        tags = genres + categories
        tags_text = ", ".join(tags)
        tags_list.append(tags_text)
    except Exception as e:
        print(f"⚠️ Error con AppID {appid}: {e}")
        tags_list.append("")
    time.sleep(0.3)  # evitar bloquear la API

df["Tags"] = tags_list


# Clasificar juegos por dificultad
keywords_dificil = ["Hard", "Difficult", "Souls-like", "Challenging", "Roguelike", "Hardcore", "Tough", "Permadeath"]

df["Dificultad"] = df["Tags"].apply(
    lambda x: 1 if any(word.lower() in str(x).lower() for word in keywords_dificil) else 0
)


#Guardar CSV
df.to_csv("steam_games_last10years.csv", index=False, encoding="utf-8-sig")
print(f"✅ Dataset generado con {len(df)} juegos. Guardado en steam_games_last10years.csv")
