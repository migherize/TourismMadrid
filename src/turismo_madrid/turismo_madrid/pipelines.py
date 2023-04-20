"""
Este pipeline procesa los artículos extraídos por Scrapy.
author: Miguel Herize
mail: migherize@gmail.com
"""

import json
import pymongo


class TurismoMadridPipeline:
    """
    Este pipeline guarda los artículos extraídos en una base de datos MongoDB y en un archivo JSON.

    El pipeline realiza las siguientes operaciones:
    - Elimina los artículos duplicados según su campo "url_route".
    - Almacena los artículos en una DB MongoDB especificada por MONGO_URI y MONGO_DATABASE.
    - Almacena los artículos en un archivo JSON llamado "output.json".

    Este pipeline se puede configurar mediante los siguientes ajustes de Scrapy:
    - ITEM_PIPELINES: especifica el orden de ejecución del pipeline.
    - MONGO_URI: especifica la URL de conexión a la base de datos MongoDB.
    - MONGO_DATABASE: especifica el nombre de la base de datos MongoDB.
    """

    col1 = "router"
    col2 = "stages"
    col3 = "itineraty"
    path_json = "/app/data/items.json"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        funcion para conectar con contenedor mongo
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        Método que se ejecuta cuando se inicia la araña.

        Este método realiza las siguientes operaciones:
        - Inicializa una lista vacía de artículos.
        - Crea una conexión a la base de datos MongoDB utilizando
        el URI especificado en las configuraciones de la araña.

        :param spider: la instancia de la araña que se está ejecutando.
        :type spider: scrapy.Spider
        """
        self.items = []
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.database = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        Procesa cada artículo extraído y lo almacena en una lista de artículos.

        Este método realiza las siguientes operaciones:
        - Comprueba si el artículo ya existe en la lista de artículos según su campo "url_route".
        - Si el artículo ya existe, lo reemplaza por el nuevo artículo.
        - Si el artículo no existe, lo agrega a la lista de artículos.

        :param item: artículo extraído por el spider.
        :type item: scrapy.Item
        :param spider: objeto Spider que está extrayendo los artículos.
        :type spider: scrapy.Spider
        :return: el artículo procesado.
        :rtype: scrapy.Item
        """

        item_exists = False
        for i, stored_item in enumerate(self.items):
            if stored_item["url_route"] == item["url_route"]:
                self.items[i] = dict(item)
                item_exists = True
                break

        if not item_exists:
            self.items.append(dict(item))

        return item

    def close_spider(self, spider):
        """
        Método que se ejecuta cuando finaliza la araña.

        Este método realiza las siguientes operaciones:
        - Escribe la lista de artículos procesados en formato JSON a un archivo en disco.
        - Inserta los artículos en la base de datos MongoDB.

        :param spider: la instancia de la araña que se está ejecutando.
        :type spider: scrapy.Spider
        """
        # Bitacora in Json
        with open(self.path_json, "w", encoding="utf-8") as file:
            json.dump(self.items, file, indent=4)

        # Save mongo
        for diccionario in self.items:
            dict_router = {}

            list_itineraty = []
            list_stages = []

            for clave, valor in diccionario.items():
                if "list_stages" in clave:
                    for stage in valor:
                        itinerary_list = stage["info_itinerarios"]
                        other_stage_info = stage.copy()
                        del other_stage_info["info_itinerarios"]
                        list_itineraty.append(itinerary_list)
                        list_stages.append(other_stage_info)
                else:
                    dict_router[clave] = valor

            list_stage_ids = []

            for stage, itinerarys in zip(list_stages, list_itineraty):
                list_itinerary_ids = (
                    self.database[self.col3].insert_many(itinerarys).inserted_ids
                )
                stage["list_itinerarys"] = list_itinerary_ids
                stage_id = self.database[self.col2].insert_one(stage).inserted_id
                list_stage_ids.append(stage_id)

            dict_router["list_stage_ids"] = list_stage_ids
            router_id = self.database[self.col1].insert_one(dict_router).inserted_id
            print("Document ID insert: ", router_id)
