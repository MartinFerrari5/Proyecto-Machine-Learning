from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
from unidecode import unidecode

#Inicializamos la app
app = FastAPI()

# Lectura del DataFrame

movies_merged = pd.read_parquet("../datasets/movies_merged.parquet").head(5000)
movies_merged_copy = movies_merged.copy()

# Cantidad de peliculas por mes
@app.post("/movies_month")
def movies_per_month(mes:str):
    try:
        a = movies_merged_copy[movies_merged_copy["release_date"].dt.month_name(locale='es_ES.utf-8') == mes.capitalize()]
        return {"cantidad": int(a["title"].count())}
    except (KeyError, AttributeError) as e:
        return {"error": str(e)}
    #     print("Check your input")

# Cantidad peliculas por dias
dias_norm = {
    "Miã©rcoles":"Miercoles",
    "Sã¡bado":"Sabado"
}
dias = movies_merged_copy["release_date"].dt.day_name(locale='es_Es.utf-8')
dias= dias.replace(dias_norm)

@app.post("/movies_day")
def cantidad_filmaciones_dia(dia):
    try:
        a = movies_merged_copy[dias== unidecode(dia).capitalize()]
        return int(a["title"].count())
    except:
        print("Check your input")
        

#Popularidad de la pelicula
@app.post("/movie_popularity")
def popularidad_titulo (titulo):
    titulo=titulo.lower()
    df_title = movies_merged_copy[movies_merged_copy["title"]==titulo]
    popularity = list(df_title["popularity"])[0]
    return f"""La película {titulo} fue estrenada en el año {int(list(df_title["release_year"])[0])} cuenta con una popularidad de {popularity}"""


# Valoracion de la pelicula
@app.post("/movie_votes")
def votos_titulo (titulo:str):
    titulo=titulo.lower()
    df_title = movies_merged_copy[movies_merged_copy["title"]==titulo]
    cant_votos = list(df_title["vote_count"])[0]
    if(cant_votos<2000): 
        return print(f"Lo siento, {titulo} cuenta solo con {cant_votos}, debes elegir una pelicula con almenos 2000")
    return f"""La película {titulo} fue estrenada en el año {int(list(df_title["release_year"])[0])} La misma cuenta con un total de {cant_votos} valoraciones, con un promedio de {list(df_title["vote_average"])[0]}"""
    

@app.post("/get_actor")
def get_actor(nombre):
    nombre = nombre.title()
    cuenta_movies = 0
    cuenta_dinero = 0
    for nombres,i in zip(movies_merged_copy["actors_names"],range(movies_merged_copy.shape[0])):
        # if(type(nombres) in [float,int] ): continue
        if(isinstance(nombres,np.ndarray) and nombre in nombres and nombre not in movies_merged_copy["director_names"][i]):
            cuenta_movies +=1
            cuenta_dinero += movies_merged_copy["return"].iloc[i]
    promedio = cuenta_movies/cuenta_dinero
    return f"El actor {nombre} participo en {cuenta_movies} peliculas, solo como actor, consiguiendo un total de {round(cuenta_dinero,2)} mil dolares, con un promedio de {round(promedio,2)} mil dolares por pelicula"
    


# Certificamps que todos los datos de la columna tengan datos

@app.post("/get_director")
def get_director(nombre):
    movies_merged_copy["director_names"].fillna("[]",inplace=True)
    nombre = nombre.title()
    peliculas_return = {}
    cuenta_dinero_total = 0
    for nombres,i in zip(movies_merged_copy["director_names"],range(movies_merged_copy.shape[0])):

        if(isinstance(nombres,object) and nombre in nombres):

            movie_title= movies_merged_copy["title"].str.capitalize().iloc[i]
            individual_return = movies_merged_copy["return"].iloc[i]
            release_year = movies_merged_copy["release_year"].iloc[i]
            budget = movies_merged_copy["budget"].iloc[i]
            revenue = movies_merged_copy["revenue"].iloc[i]

            peliculas_return[movie_title] = {"retorno": round(individual_return,2),
                                            "año_lanzamiento": int(release_year),
                                            "costo":budget,
                                            "revenue":revenue}
            cuenta_dinero_total += movies_merged_copy["return"].iloc[i]

    
    return f"El director {nombre} consiguio un total de {round(cuenta_dinero_total,2)} mil dolares",peliculas_return
    
