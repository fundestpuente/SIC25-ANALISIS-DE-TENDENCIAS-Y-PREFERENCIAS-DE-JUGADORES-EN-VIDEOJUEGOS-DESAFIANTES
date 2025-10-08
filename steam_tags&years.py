import requests
import json
import time
import pandas as pd
from datetime import datetime
from tqdm import tqdm

#Se recolecta los tags y el anio de lanzamiento en un script separado por cuestion de optimizar memoria
df= pd.read_csv("steam_games.csv")
#Obtener tags desde la API de Steam Store
print("\nObteniendo tags (géneros y categorías) desde Steam Store...")

tags_list = []
release_years = []

#Recorremos y recolectamos la informacion de los juegos que ya tenemos en el csv
for appid in tqdm(df["AppID"], desc="Consultando API Steam Store"):
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        r = requests.get(url, timeout=6)
        data = r.json()

        if not data or not data.get(str(appid), {}).get("success"): #Si no hay informacion en la API agregamos valores vacios
            tags_list.append("")
            release_years.append(None)
            continue

        info = data[str(appid)]["data"]
        genres = []
        for g in info.get("genres", []): #Intentamos obtener solo la lista de generos, si no hay informacion devolvemos una lista vacia
            genres.append(g["description"])
        categories = []
        for c in info.get("categories", []):#Intentamos obtener solo la lista de categorias, si no hay informacion devolvemos una lista vacia
            categories.append(g["description"])
        tags = genres + categories
        tags_text = ", ".join(tags) #Volvemos una cadena la lista resultante de tags
        tags_list.append(tags_text)

        release_date = info.get("release_date", {}).get("date", "")
        # Steam puede tener formatos como "12 Feb, 2020" o solo "2020"
        year = None
        for part in release_date.split():
            if part.isdigit() and len(part) == 4:  # detecta un año si tiene 4 digitos
                year = int(part)
                break
        release_years.append(year)

    except Exception as e:
        print(f"Error con AppID {appid}: {e}")
        tags_list.append("")
    time.sleep(0.3)  # evitar bloquear la API


#Agregamos los valores al dataFrame
df["Tags"] = tags_list 
df["ReleaseYear"] = release_years


# Clasificar juegos por dificultad
keywords_dificil = ["Hard", "Difficult", "Challenging", "Tough", "Hardcore", "Souls-like",
    "Roguelike", "Roguelite", "Permadeath", "Extreme", "Expert", "Insane",
    "Nightmare", "Survival", "Strategy", "Manual", "Skill", "Intense",
    "Realistic", "Complex", "High Difficulty"]
#Tags tipicos en la plataforma Steam para juegos considerados dificiles

df["Dificultad"] = df["Tags"].apply(
    lambda x: 1 if any(word.lower() in str(x).lower() for word in keywords_dificil) else 0)
#Si contiene alguna de las palabras claves que definimos en sus Tags lo catalgamos como un juego dificil == 1, si es facil ==0