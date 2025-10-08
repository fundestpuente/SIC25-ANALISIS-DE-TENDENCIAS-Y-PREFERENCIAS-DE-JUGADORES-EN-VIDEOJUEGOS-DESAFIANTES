import requests
import json
import time
import heapq
import pandas as pd
from datetime import datetime

#Descargar datos de SteamSpy 
print("🔍 Descargando datos de SteamSpy ...")

top_n = 2000 #Nos quedamos con un top 2000 que se actualiza para tener memoria constante
sleep_time = 0.2  # tiempo entre requests para no saturar la API

max_retries = 3 #Maximo de intentos en caso de que una pagina genere un bucle
retries = 0 #Intentos actuales de obtener una pagina de la API

page = 0 #Pagina actual de la API. Usamos la opcion de ir pagina por pagina (que contienen 1000 juegos c/u) para no saturar la memoria
max_page = 86 #Por medio de prueba y error, esta es la pagina hasta la que Steam Spy permite obtener sin entrar en bucle

heap = []  # min-heap de (AverageForever, juego_dict)

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
            print(f"Saltando página {page} después de {max_retries} intentos fallidos")
            page += 1
            retries = 0
        time.sleep(1) #evitar bloqueos de la API
        continue

    if not data: 
        print(" Se terminó de descargar todo SteamSpy.")
        break

    for appid, info in data.items():
        # Convertir Propietarios a entero
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
            "Tags": "",        
        }
        if len(heap) < top_n:# Si el heap aun no tiene el maximo que establecimos, agregamos directamente el nuevo juego
            heapq.heappush(heap, (juego["AverageForever"], juego["Owners"], juego["AppID"], juego)) 
            # Se utilizan 3 valores en el heap como criterio para ser ordenados ya que hay casos que averageForever y owners empataban
            #heeappush agrega y ordena automaticamente los datos de menor a mayor
        else:# Ya hay 2000 datos en el heap
            # Compara AverageForever y Owners. En caso de empate la id unica decide
            if (juego["AverageForever"] > heap[0][0] or (juego["AverageForever"] == heap[0][0] and juego["Owners"] > heap[0][1])):
                #Por la naturaleza de heap el primero siempre es el menor valor por lo que lo iremos reemplazando cuando sea necesario
                    heapq.heapreplace(heap, (juego["AverageForever"], juego["Owners"], juego["AppID"], juego))
    page += 1 #Avanzamos a la siguiente pagina
    time.sleep(sleep_time) #evitar bloqueo de la API

#Crear DataFrame
df = pd.DataFrame([x[3] for x in heap]) #heap era una tupla con el formato ("AverageForever","Owners","AppId",juego) y juego contiene la informacion que necesitamos
print(f"Top {len(df)} juegos seleccionado.")

#Guardar CSV
df.to_csv("steam_games.csv", index=False, encoding="utf-8-sig")
print(f"Dataset generado con {len(df)} juegos. Guardado en steam_games.csv")
