"""
Araña para extraer información de la url = https://turismomadrid.es/es/rutas.html
author: Miguel Herize
mail: migherize@gmail.com
"""

import scrapy
from scrapy.utils.response import open_in_browser


class TourismMadridSpider(scrapy.Spider):
    """
    Esta araña de Scrapy se encarga de extraer información de la página web de itinerarios
    turísticos de Madrid. La información extraída incluye el nombre del itinerario, la
    descripción, la duración, los lugares de interés y los precios.

    Attributes:
        name (str): El nombre de la araña.
        start_urls (list): La lista de URLs de inicio para el web scraping.
        custom_settings (dict): Un diccionario con las configuraciones personalizadas para
            la araña, como el tiempo de espera y la concurrencia.
    """

    name = "turismo_madrid_spider"
    allowed_domains = ["turismomadrid.es"]
    start_urls = ["https://turismomadrid.es/es/rutas.html"]
    successful = True
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        # "LOG_LEVEL": "INFO",
    }

    base_url = "https://turismomadrid.es"

    def __init__(self, *args, **kwargs):
        super(TourismMadridSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        Genera las solicitudes HTTP iniciales para la araña, utilizando
        la URL definida en el atributo `start_urls`.

        Yields:
            scrapy.Request: Un objeto Request para la primera página a visitar.
        """
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.open_page,
            dont_filter=True,
            meta={"dont_redirect": True},
        )

    def open_page(self, response):
        """
        Abre la respuesta en el navegador para hacer pruebas.

        Args:
            response (scrapy.http.Response): La respuesta HTTP recibida.

        Returns:
            None
        """
        print(f"Texto de respuesta: {response.text}")
        open_in_browser(response)
