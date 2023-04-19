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

### Documentacion

## Scrapy
Scrapy es un framework de web scraping de Python que permite extraer datos de páginas web de forma automatizada.

![webscraping](/assets/images/scrapy.png)

Scrapy es capaz de interactuar con bases de datos NoSQL, como MongoDB, para guardar los datos extraídos en una base de datos local o en la nube. Para hacer esto, Scrapy utiliza la biblioteca PyMongo para interactuar con la base de datos. 

## Mongo
MongoDB es una base de datos NoSQL que se utiliza para almacenar y procesar grandes cantidades de datos.

![webscraping](/assets/images/mongoDB.png)

MongoDB puede ser una buena opción para proyectos de web scraping en los que se espera manejar grandes cantidades de datos de forma rápida y eficiente. Esto se debe a que MongoDB es una base de datos NoSQL que permite una alta escalabilidad horizontal, lo que significa que puedes aumentar la capacidad de almacenamiento y procesamiento agregando más servidores en un clúster.