from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


#Inicializamos la app
app = FastAPI()

# Lectura del DataFrame

movies_merged = pd.read_parquet("../datasets/movies_merged.parquet").head(5000)
movies_merged_copy = movies_merged.copy()

""" 

FUNCION QUE RETORNA LA CANTIDAD DE PELICULAS POR MES

 """

# Mappeo de los meses con sus respectivos indices
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

@app.post("/cantidad_filmaciones_mes")
def cantidad_filmaciones_mes(mes:str):
    mes = mes.capitalize()
    try:
        num_mes = month_map[mes]
        cant = movies_merged_copy[movies_merged_copy["release_date"].dt.month == num_mes]
        return {"mes": mes
            ,"cantidad": int(cant["title"].count())}
    except :
        return {"error": "Check your input"}
    #     print("Check your input")


""" 

FUNCION QUE RETORNA LA CANTIDAD DE PELICULAS POR DIA

"""


# Mappeo de los dias con sus respectivos indices
dias={
    "Lunes":0,
    "Martes":1,
    "Miercoles":2,
    "Jueves":3,
    "Viernes":4,
    "Sabado":5,
    "Domingo":6

}
# Cantidad peliculas por dias

@app.post("/cantidad_filmaciones_dia")
def cantidad_filmaciones_dia(dia):
    dia = unidecode(dia.title())
    try:
        num_dia = dias[dia]
        cantidad = movies_merged_copy[movies_merged_copy["release_date"].dt.day_of_week == num_dia]
        return {"dia": dia 
            ,"cantidad": int(cantidad["title"].count())}
    except:
        return "Check your input"
        

""" 

FUNCION QUE RETORNA LA PELICULA, SU AÑO DE LANZAMIENTO Y SU POPULARIDAD

"""

#Popularidad de la pelicula
@app.post("/score_titulo")
def score_titulo (titulo:str):
    titulo=titulo.lower()
    try:
        df_title = movies_merged_copy[movies_merged_copy["title"]==titulo]
        popularity = list(df_title["vote_average"])[0]
        return f"""La película {titulo.title()} fue estrenada en el año {int(list(df_title["release_year"])[0])} cuenta con una score de {popularity}/10"""
    except:
        return f"La pelicula {titulo} no se encuentra en la base de datos"


""" 

FUNCION QUE RETORNA LA PELICULA, SU AÑO DE LANZAMIENTO, LA CANTIDAD DE VOTOS EL VALOR PROMEDIO DE LOS MISMOS

"""


# Valoracion de la pelicula
@app.post("/votos_titulo")
def votos_titulo (titulo:str):
    titulo=titulo.lower()
    try:
        df_title = movies_merged_copy[movies_merged_copy["title"]==titulo]
        if(df_title.shape[0]==0):
            return f"La pelicula {titulo} no se encuentra en la base de datos"
        cant_votos = list(df_title["vote_count"])[0]
        if(cant_votos<2000): 
            return f"Lo siento, {titulo.title()} cuenta solo con {cant_votos} valoraciones, debes elegir una pelicula con almenos 2000"
        return f"""La película {titulo.title()} fue estrenada en el año {int(list(df_title["release_year"])[0])} La misma cuenta con un total de {cant_votos} valoraciones, con un promedio de {list(df_title["vote_average"])[0]}"""
    except:
        f"La pelicula {titulo} no se encuentra en la base de datos"
    


""" 

FUNCION QUE RETORNA EL ACTOR, EN CUANTAS PELICULAS PARTICIPO, EL DINERO RECAUDADO POR TODAS LAS PELICULAS Y EL DINERO PROMEDIO QUE GANO

"""

@app.post("/get_actor")
def get_actor(nombre:str):
    nombre = nombre.title()
    cuenta_movies = 0
    cuenta_dinero = 0
    try:
        for nombres,i in zip(movies_merged_copy["actors_names"],range(movies_merged_copy.shape[0])):
            # if(type(nombres) in [float,int] ): continue
            if(isinstance(nombres,np.ndarray) and nombre in nombres and nombre not in movies_merged_copy["director_names"][i]):
                cuenta_movies +=1
                cuenta_dinero += movies_merged_copy["return"].iloc[i]
        promedio = cuenta_movies/cuenta_dinero
        return f"El actor {nombre} participo en {cuenta_movies} peliculas, solo como actor, consiguiendo un total de {round(cuenta_dinero,2)} mil dolares, con un promedio de {round(promedio,2)} mil dolares por pelicula"
    except:
        return f"{nombre} no se encuentra en la base de datos"
    


""" 

FUNCION QUE RETORNA EL DIRECTOR, EL DINERO RECAUDADO POR TODAS LAS PELICULAS Y UNA PEQUEÑA DESCRIPCION DE LAS PELICULAS QUE REALIZO

"""

# Certificamps que todos los datos de la columna tengan datos


@app.post("/get_director")
def get_director(nombre):
    movies_merged_copy["director_names"].fillna("Unknown",inplace=True)
    nombre = nombre.title()
    peliculas_return = {}
    cuenta_dinero_total = 0
    try:
        for nombres,i in zip(movies_merged_copy["director_names"],range(movies_merged_copy.shape[0])):

            if(isinstance(nombres,object) and nombre in nombres):

                movie_title= movies_merged_copy["title"].str.title().iloc[i]
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
    except:
        return f"{nombre} no se encuentra en la base de datos"


""" 

SISTEMA DE RECOMENDACION

"""

# Sistema de recomendacion

rec_system = pd.read_parquet("../datasets/rec_system.parquet").head(3000)
rec_system_copy = rec_system.copy()

# Rellenamos los posibles valores nulos
rec_system_copy.fillna({"overview":"[Unknown]",
                   "name_genre":"[Unknown]",
                   "actors_names":"[Unknown]",
                   "director_names":"[Unknown]",
                   "tagline":"[Unknown]",
                   "company":"[Unknown]",
                   },inplace=True)


# Transformar a lista los valores que parquet reconoce como datos de tipo ndarray
def collapse(valor):
    valores =[]
    for i in valor:
       valores.append(i)
    return valores

rec_system_copy["name_genre"]=rec_system_copy["name_genre"].apply(collapse)

#Transformamos en string la columna de genero
rec_system_copy["name_genre"] = rec_system_copy["name_genre"].apply(lambda x: ",".join(x))

#Unimos todo en una columna
rec_system_copy["tags"] =  rec_system_copy["name_genre"]  + " " + rec_system_copy["title"] + " " + str(rec_system_copy["vote_average"]) + " "       #+ rec_system_copy["actors_names"] + rec_system_copy["director_names"]  


rec_system_copy["tags"] = rec_system_copy["tags"].apply(lambda x: "".join(x.replace(","," ")))

tv = TfidfVectorizer(max_features=5000, stop_words="english")
vector = tv.fit_transform(rec_system_copy["tags"]).toarray()

cosine_sim = linear_kernel(vector,vector)

indices = pd.Series(rec_system_copy.index, index=rec_system_copy["title"]).drop_duplicates()

@app.post("/recomendacion")
def recomendacion(movie:str):
    movie = movie.lower()
    num=5
    try:
        index = indices[movie]
        sim_scores=list(enumerate(cosine_sim[index]))
        distances = sorted(sim_scores,reverse= True,key=lambda x: x[1])
        lista=[]
        for i in distances[1:num+1]:
            # print(i[0])
            titulo = rec_system_copy.iloc[i[0]].title
            lista.append(titulo.title())
        return lista
    except: 
        return f"La pelicula {movie} no se encuentra en la base de datos"


    
