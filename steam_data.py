import requests
import json
import time
import heapq
import pandas as pd
from datetime import datetime
from tqdm import tqdm

#Descargar datos de SteamSpy 
print("🔍 Descargando datos de SteamSpy ...")

top_n = 2000
sleep_time = 0.2  # tiempo entre requests

max_retries = 3
retries = 0

page = 0
max_page = 86 

# Usamos top 2000 juegos para no sobrecargar la PC
heap = []  # min-heap de (AverageForever, juego_dict)
page = 0

while page <= max_page:
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        retries = 0  # resetear reintentos si fue exitoso
    except:
        retries += 1
        print(f"Error en página {page}, reintentando...")
        if retries >= max_retries:
            print(f"⚠ Saltando página {page} después de {max_retries} intentos fallidos")
            page += 1
            retries = 0
        time.sleep(1)
        continue

    if not data:
        print(" Se terminó de descargar todo SteamSpy.")
        break

    for appid, info in data.items():
        # Convertir Owners a entero
        owners_str = info.get("owners", "0").replace(",", "")
        try:
            owners = int(owners_str)
        except:
            owners = 0


        juego = {
            "AppID": appid,
            "Nombre": info.get("name", ""),
            "Developer": info.get("developer", ""),
            "Publisher": info.get("publisher", ""),
            "ScoreRank": info.get("score_rank", ""),
            "Owners": owners,
            "AverageForever": info.get("average_forever", 0),
            "Average2Weeks": info.get("average_2weeks", 0),
            "MedianForever": info.get("median_forever", 0),
            "Median2Weeks": info.get("median_2weeks", 0),
            "CCU": info.get("ccu", 0),
            "Price": info.get("price", "0"),
            "InitialPrice": info.get("initialprice", "0"),
            "Discount": info.get("discount", "0"),
            "Tags": "",        # SteamSpy top100 no trae tags
        }
        if len(heap) < top_n:
            heapq.heappush(heap, (juego["AverageForever"], juego["Owners"], juego["AppID"], juego))
        else:
            # Compara AverageForever y Owners (desempate)
            if (juego["AverageForever"] > heap[0][0] or (juego["AverageForever"] == heap[0][0] and juego["Owners"] > heap[0][1])):
                    heapq.heapreplace(heap, (juego["AverageForever"], juego["Owners"], juego["AppID"], juego))
    page += 1
    time.sleep(sleep_time)

#Crear DataFrame
df = pd.DataFrame([x[3] for x in heap])
print(f"✅ Top {len(df)} juegos seleccionado.")

#Guardar CSV
df.to_csv("steam_games.csv", index=False, encoding="utf-8-sig")
print(f"✅ Dataset generado con {len(df)} juegos. Guardado en steam_games.csv")
