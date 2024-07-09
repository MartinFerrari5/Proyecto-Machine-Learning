import pandas as pd
import numpy as np
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel

""" 

SISTEMA DE RECOMENDACION

"""

# Sistema de recomendacion

rec_system = pd.read_parquet("../datasets/rec_system.parquet").head(3000) #Aumente el numero de registros a su gusto
rec_system_copy = rec_system.copy()

# Rellenamos los posibles valores nulos
rec_system_copy.fillna({"overview":"[Unknown]",
                   "name_genre":"[Unknown]",
                   "tagline":"[Unknown]"
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

def modelo_recomendacion(movie:str):
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