# <div style="text-align:center">PROYECTO INDIVIDUAL N°1 MACHINE LEARNING OPERATIONS
<p align="center"><img  src="https://th.bing.com/th/id/OIP.9omCDNmaGGrzBwJoTYs25wAAAA?rs=1&pid=ImgDetMain"> </p>
</div>

<HR>

## Tabla de contenido
1. [Introducción](#introducción)
2. [Requisitos](#requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instrucciones de Ejecucion](#instrucciones-de-ejecucion)
5. [Conclusiones](#resultados-y-conclusiones)
6. [Datasets](#licencia)
7. [Autor](#autor) 


### Introduccion 
<HR>

<p style="border-left:5px solid rgba(150, 150, 105, 0.1);padding:5px;font-size:15px">Bienvenidos a todos a mi primer proyecto de machine learning. En esta oportunidad, el objetivo es crear una <i>API</i> con ciertas funciones que den respuesta a ciertos inputs del usuario. Un ejemplo: la cantidad de peliculas realizadas en un mes en especifico. Durante este proceso se ha realizado un ETL para asi poder trabajar con datos limpios y luego se realizo un EDA para poder analizar en profundidad el comportamiento de nuestro dataset. Luego, se construyo el sistema de recomendacion utilizando machine learning </p>

### Requisitos
<hr>
<p>Para el entendimiento y ejecucion del siguiente proceso se require conocimiento en las siguientes areas:</p>

1) Python
2) Pandas
3) Numpy
4) Scikit-Learn


### Estructura del proyecto:
<hr>

`data/`: Esta carpeta contiene los datasets utilizados. <br>
`notebooks/`: Contiene los archivos `.ipynb` en los cuales se realizo el <i>ETL</i> y el <i>EDA</i>.<br>
`src/`: Contiene los archivos necesarios para que la <i>API</i> funcione.<br>
*   `main.py`: Instancia la API.
*   `funciones.py`: Cuenta con todas las funciones presentes en la API.
*   `modelo.py`: Alberga el modelo de machine learning utilizado para el sistema de recomendacion.

`README.md`: Documentacion del presente proyecto.<br>



### Instrucciones de Ejecucion
<hr>

1) Como primera instancia se clonara el repositorio.
```
git clone https://github.com/MartinFerrari5/first_project.git
```
- Como recomendacion, utiliza un entorno virtual:
```
#Creacion entorno virtual
    python -m venv nombre-entorno
```
* Activacion:
    - Windows: `venv\Scripts\activate`
    - Mac/Linux: `venv/bin/activate`

2) Dirigite a la carpeta de `/notebooks` donde encontraras el archivo `etl.ipynb`, dentro de este, encontraras todo el proceso de limpieza y tranformacion realizado a los dataset en su formato original. Al final del presente <b>README</b> se encuentra el link para que los puedas descargar.

3) Una vez ejecutado el paso n°2, dirigete al archivo `eda.ipynb` en el cual encontraras el analisis exploratorio de los datos. Se presenta un estudio con graficos de los datos ya limpios

4) Haciendo uso de la terminal que gustes, inicia la <i>API</i>.

```
# Dirigete a la carpeta src 
cd src

# Corre el siguiente codigo
uvicorn main:app --reload

```
5) <p>Una vez la <i>API</i> este corriendo, ingresa a la url que FastAPI te provee, y pruebala &#128513;</p>


### Conclusiones
<hr>

* Se pudo observar que gran cantidad de los datos estaban vacios y otro porcentaje presentaba estructuras complejas. Si bien esto no imposibilita el trabajo, es de suma importancia entender y apuntar a una mejora en la <b>Calidad de los Datos</b> ya que asi, se trabaja mejor, aumenta la deteccion de patrones y tendencias y se puede ofrecer un mejor servicio, ayudando a una empresa a poder mejorarse cada dia.

### Datasets
<hr>

Al contar con un peso significante, los datasets utilizados en formato `.csv` se encuentran en el siguiente link para su descarga. <b><a href="https://drive.google.com/drive/u/0/folders/1VuwQ5M1JQ_VugOIa7mo8ET66eOhLpjsQ">Link Datasets</a></b>

### Autor
<hr>

Este proyecto fue realizado por Martin Ferrari. Muchas gracias a todos por leer, no dudes en contactarme a mi <a href="https://www.linkedin.com/in/martin-ferrari-bb0547219/">LinkedIn</a> por cualquier duda


