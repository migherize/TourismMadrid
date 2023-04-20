"""
Items para construir la estructura de raspado
author: Miguel Herize
mail: migherize@gmail.com
"""
import scrapy


class TurismoMadridItem(scrapy.Item):
    """
    Definición de los campos que conforman el objeto a guardar para los datos de turismo de Madrid.

    Atributos:
        url_route (scrapy.Field): La URL de la ruta turística.
        title (scrapy.Field): El título de la ruta turística.
        transport (scrapy.Field): Información sobre el transporte disponible para la ruta turística.
        distance (scrapy.Field): La distancia de la ruta turística.
        time (scrapy.Field): El tiempo necesario para completar la ruta turística.
        description (scrapy.Field): Una descripción detallada de la ruta turística.
        url_map_tour (scrapy.Field): La URL del mapa de la ruta turística.
        stages (scrapy.Field): Información detallada sobre las etapas o paradas de la ruta turística.
        maps_gpx (scrapy.Field): La URL del archivo GPX que contiene la información de la ruta turística.
        maps_kmz (scrapy.Field): La URL del archivo KMZ que contiene la información de la ruta turística.
        more_info (scrapy.Field): Información adicional relevante sobre la ruta turística.
        list_stages (scrapy.Field): Lista de todas las paradas de la ruta turística.
    """

    url_route = scrapy.Field()
    title = scrapy.Field()
    transport = scrapy.Field()
    distance = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    url_map_tour = scrapy.Field()
    stages = scrapy.Field()
    maps_gpx = scrapy.Field()
    maps_kmz = scrapy.Field()
    more_info = scrapy.Field()
    list_stages = scrapy.Field()
