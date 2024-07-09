from fastapi import FastAPI
import pandas as pd
from funciones import (cant_film_mes,cant_film_dia,score,votos,actor_name,director_name)
from modelo import modelo_recomendacion
#Inicializamos la app
app = FastAPI()
#FUNCION QUE RETORNA LA CANTIDAD DE PELICULAS POR MES


@app.post("/cantidad_filmaciones_mes")
def cantidad_filmaciones_mes(mes):
    return cant_film_mes(mes)

#FUNCION QUE RETORNA LA CANTIDAD DE PELICULAS POR DIA


@app.post("/cantidad_filmaciones_dia")
def cantidad_filmaciones_dia(dia):
    return cant_film_dia(dia)
        

 
#FUNCION QUE RETORNA LA PELICULA, SU AÑO DE LANZAMIENTO Y SU POPULARIDAD

#Popularidad de la pelicula
@app.post("/score_titulo")
def score_titulo(titulo):
    return score(titulo)



#FUNCION QUE RETORNA LA PELICULA, SU AÑO DE LANZAMIENTO, LA CANTIDAD DE VOTOS EL VALOR PROMEDIO DE LOS MISMOS

# Valoracion de la pelicula
@app.post("/votos_titulo")
def votos_titulo(titulo):
    return votos(titulo)
    


#FUNCION QUE RETORNA EL ACTOR, EN CUANTAS PELICULAS PARTICIPO, EL DINERO RECAUDADO POR TODAS LAS PELICULAS Y EL DINERO PROMEDIO QUE GANO

@app.post("/get_actor")
def get_actor(actor):
    return actor_name(actor)
    

# FUNCION QUE RETORNA EL DIRECTOR, EL DINERO RECAUDADO POR TODAS LAS PELICULAS Y UNA PEQUEÑA DESCRIPCION DE LAS PELICULAS QUE REALIZO

@app.post("/get_director")
def get_director(director):
    return director_name(director)


@app.post("/recomendacion")
def recomendacion(titulo):
    return modelo_recomendacion(titulo)