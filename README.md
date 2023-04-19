# TourismMadrid
**TourismMadrid** es un proyecto con el Framework Scrapy de Python diseñado para extraer información turística de la página web oficial turismomadrid.

![FastApi](/assets/images/home.png)


## Ambiente: 

### Reto de extracción de información de páginas web y construcción de base de datos
Este repositorio contiene un proyecto para extraer información de una página web (https://turismomadrid.es/es/rutas.html) que ofrece itinerarios para hacer turismo en Madrid. El objetivo del proyecto es construir un script que descargue la información y la almacene en una base de datos de elección.

### Herramientas necesarias

Para llevar a cabo este proyecto, se necesitan las siguientes herramientas:

* Python 3.x
* Scrapy (versión 2.x recomendada).
* Una base de datos a elección (Elasticsearch o No Relacional).

![webscraping](/assets/images/webscraping.png)

### Proceso de extracción de información

El proceso de extracción de información se llevará a cabo utilizando el framework Scrapy de Python. Scrapy es una herramienta de web scraping que nos permitirá extraer de manera eficiente información estructurada de la página web.

### Proceso de almacenamiento en base de datos
Una vez que la información ha sido extraída, se almacenará en una base de datos a elección. Se utiliza una base de datos No relacional como Mongo o Elasticsearch para almacenar la información.

## Documentacion

### Scrapy

Scrapy es un framework de web scraping de Python que permite extraer datos de páginas web de forma automatizada.

![webscraping](/assets/images/scrapy.png)

Scrapy es capaz de interactuar con bases de datos NoSQL, como MongoDB, para guardar los datos extraídos en una base de datos local o en la nube. Para hacer esto, Scrapy utiliza la biblioteca PyMongo para interactuar con la base de datos. 

### Mongo
MongoDB es una base de datos NoSQL que se utiliza para almacenar y procesar grandes cantidades de datos.

![webscraping](/assets/images/mongoDB.png)

MongoDB puede ser una buena opción para proyectos de web scraping en los que se espera manejar grandes cantidades de datos de forma rápida y eficiente. Esto se debe a que MongoDB es una base de datos NoSQL que permite una alta escalabilidad horizontal, lo que significa que puedes aumentar la capacidad de almacenamiento y procesamiento agregando más servidores en un clúster.

## Requisitos
1. Python 3.10
2. Pip 23.0
3. Scrapy >= 2.5
4. Base de datos: MongoDB

## Instalación
1. Clonar el repositorio
    ```
    git clone https://github.com/migherize/Reino_del_Trebol.git
    ```

2. Variables de entorno .env

    * PYTHONPATH

        La variable de entorno pythonpath especifica una lista de directorios desde la que se pueden importar los módulos. Para este proyecto se necesitan:
        
        * PATH_YOUR_LOCAL/

        ## Crear archivo .env
        ```
        touch .env
        ```
        #### Ejemplo .env
        ```
        -   PYTHONPATH="$PYTHONPATH:/PATH_YOUR_LOCAL_REPO/"

## Uso
1. Ejecutar el proyecto

    ```
    docker-compose -f docker-compose-dev.yml up --build
    ```

2. Ejecutar el proyecto scrapy
    
    Para ello debemos tener instalado el sistema de gestion de paquetes pip.
    ```
    pip install --upgrade pip
    ```

    Luego con un gestor de entornos virtuales construiremos un entorno virtual para el proyecto, con el gestor de tu preferencia.
    
    * Entorno con [Pipenv](https://pypi.org/project/pipenv/):
        ```
            pip install pipenv

            pipenv install
            
            pipenv shell

            pipenv install -r requirements.txt
        ```

    * Entorno con [Virtualenv](https://pypi.org/project/virtualenv/):
        ```
        python -m venv TourismMadrid

        source TourismMadrid/bin/activate

        cd TourismMadrid

        pipenv install -r requirements.txt
        
        ```
    
    ```
    cd src/turismo_madrid

    scrapy crawl turismo_madrid_spider
    ```


## Test

Para realizar test de prueba, en la carpeta /test/ ejecutar:
    Usabilidad:

    ```
    python3 -m unittest test_spider.py  
    ```

## Contribución

¡Todas las contribuciones son bienvenidas! Si quieres ayudar a mejorar este proyecto, puedes hacerlo a través de pull requests. Si tienes alguna duda o sugerencia, no dudes en crear un issue en este repositorio.

1. Fork del repositorio
2. Crear una rama

    ```
    git checkout -b feature/nueva-funcionalidad
    ```