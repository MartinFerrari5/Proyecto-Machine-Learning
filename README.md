# <div style="text-align:center">INDIVIDUAL PROJECT N°1 MACHINE LEARNING OPERATIONS
<p style="text-align:center"><img  src="https://th.bing.com/th/id/OIP.9omCDNmaGGrzBwJoTYs25wAAAA?rs=1&pid=ImgDetMain"> </p>
</div>

## Content Table
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Project Structure](#proyect-structure)
4. [Execution Instructions](#execution-instructions)
5. [Conclusions](#conclusions)
6. [Datasets](#licencia)
7. [Author](#author) 


## Introduction

Welcome to my first machine learning project! In this opportunity, we worked with movies datasets and  the goal is to create an API with certain functions that respond to specific user inputs. For example, the API could provide the number of movies released in a particular month. During this process, an ETL (Extract, Transform, Load) pipeline was implemented to work with clean data, followed by an Exploratory Data Analysis (EDA) to thoroughly examine the dataset's behavior. Finally, a recommendation system was built using machine learning.

## Requirements

To understand and execute this project, knowledge in the following areas is required:

1) ***Python***
2) ***Pandas***
3) ***NumPy***
4) ***Scikit-Learn***
5) ***Project Structure***

## Project Structure

`data/`: This folder contains the datasets used.

``notebooks/``: Contains the ``.ipynb`` files where the ETL and EDA were performed.

``src/``: Contains the files necessary for the API to function.

``main.py``: Instantiates the API.

``funciones.py``: Contains all the functions present in the API.

``modelo.py``: Contains the machine learning model used for the recommendation system.

``README.md``: Documentation for this project.


# Execution Instructions

1) Clone the repository:
```
git clone https://github.com/MartinFerrari5/first_project.git
```

- It is recommended to use a virtual environment:
# Create virtual environment
```
python -m venv environment_name
```

- Activate:
``Windows``: venv\Scripts\activate

``Mac/Linux``: venv/bin/activate

2) Download libraries.
```
python -m pip install -r requirements.txt
```
3) Navigate to the /notebooks folder where you will find the ``etl.ipynb`` file. Inside, you will find the entire cleaning and transformation process applied to the datasets in their original format. The link to download these datasets is provided at the end of this ``README``.

Once step 3 has been executed, proceed to the ``eda.ipynb`` file where you will find the exploratory data analysis. A study with graphs of the cleaned data is presented.

4) Using the terminal of your choice, start the API:

```
# Navigate to the src folder
cd src

# Run the following code
uvicorn main:app --reload
```

5) <p> Once the API is running, access the URL provided by FastAPI and try it out! &#128513;</p>

## Conclusions

It was observed that a significant amount of data was empty, and another percentage presented complex structures. While this does not make the work impossible, it is of significal importance to understand and aim for an improvement in Data Quality. This will allow a better work, increase pattern and trend detection, and the ability to offer a better service, helping the company to improve every day.

## Datasets

Due to their significant size, the datasets used in .csv format can be downloaded from the following link:

<b><a href="https://drive.google.com/drive/u/0/folders/1VuwQ5M1JQ_VugOIa7mo8ET66eOhLpjsQ">Datasets Link</a></b>

## Author

This project was carried out by Martin Ferrari. Thank you all for reading, feel free to contact me on my <a href="https://www.linkedin.com/in/martin-ferrari-bb0547219/">LinkedIn</a> for any questions.







