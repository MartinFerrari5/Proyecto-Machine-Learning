from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
from unidecode import unidecode
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity,linear_kernel



#Inicializamos la app
app = FastAPI()

# Lectura del DataFrame

movies_merged = pd.read_parquet("../datasets/movies_merged.parquet").head(5000)
movies_merged_copy = movies_merged.copy()

month_map={
    "Enero":1,
    "Febrero":2,
    "Marzo":3,
    "Abril":4,
    "Mayo":5,
    "Junio":6,
    "Julio":7,
    "Agosto":8,
    "Septiembre":9,
    "Ocutbre":10,
    "Noviembre":  11,
    "Diciembre":12
}

# Cantidad de peliculas por mes
@app.post("/movies_month")
def movies_per_month(mes:str):
    mes = mes.capitalize()
    num_mes = month_map[mes]
    try:
        cant = movies_merged_copy[movies_merged_copy["release_date"].dt.month == num_mes]
        return {"cantidad": int(cant["title"].count())}
    except :
        return {"error": "Check your input"}
    #     print("Check your input")

# Cantidad peliculas por dias
dias={
    "Lunes":0,
    "Martes":1,
    "Miercoles":2,
    "Jueves":3,
    "Viernes":4,
    "Sabado":5,
    "Domingo":6

}

@app.post("/movies_day")
def cantidad_filmaciones_dia(dia):
    dia = unidecode(dia.title())
    num_dia = dias[dia]
    try:
        cantidad = movies_merged_copy[movies_merged_copy["release_date"].dt.day_of_week == num_dia]
        return int(cantidad["title"].count())
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



# Sistema de recomendacion

rec_system = pd.read_parquet("../datasets/rec_System.parquet").head(20000)
rec_system_copy = rec_system.copy()

rec_system_copy.fillna({"overview":"[]",
                   "name_genre":"[]",
                   "actors_names":"[]",
                   "director_names":"[]",
                   "tagline":"[]",
                   "vote_average":rec_system["vote_average"].mean()},inplace=True)


rec_system_copy["overview"] = rec_system_copy["overview"].apply(lambda x: x.split())
rec_system_copy["tagline"] = rec_system_copy["tagline"].apply(lambda x: x.split())

def collapse(valor):
    valores =[]
    for i in valor:
       valores.append(i.replace(" ",""))
    return valores


rec_system_copy["name_genre"]=rec_system_copy["name_genre"].apply(collapse)
rec_system_copy["actors_names"]=rec_system_copy["actors_names"].apply(collapse)
rec_system_copy["director_names"]=rec_system_copy["director_names"].apply(collapse)
rec_system_copy["tagline"]=rec_system_copy["tagline"].apply(collapse)

rec_system_copy["tags"] = rec_system_copy["overview"] + rec_system_copy["name_genre"] + rec_system_copy["actors_names"] + rec_system_copy["director_names"] + rec_system_copy["tagline"] 

rec_system_copy["tags"] = rec_system_copy["tags"].apply(lambda x: "".join(x))

tv = TfidfVectorizer(max_features=5000, stop_words="english")
vector = tv.fit_transform(rec_system_copy["tags"]).toarray()

cosine_sim = linear_kernel(vector,vector)

indices = pd.Series(rec_system_copy.index, index=rec_system_copy["title"]).drop_duplicates()

# @app.post("/recomendacion")
# def recomendacion(movie):
#     movie = movie.lower()
#     # index = indices[movie]
#     # sim_scores=list(enumerate(cosine_sim[index]))
#     # distances = sorted(sim_scores,reverse= True,key=lambda x: x[1])
#     # lista=[]
#     # for i in distances[1:10]:
#     #     # print(i[0])
#     #     lista.append(rec_system_copy.iloc[i[0]].title)

#     return ""


    
