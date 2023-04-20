"""
Araña para extraer información de la url = https://turismomadrid.es/es/rutas.html
author: Miguel Herize
mail: migherize@gmail.com
"""
import re
import scrapy
from os import path, getcwd
from turismo_madrid.items import TurismoMadridItem
from scrapy.utils.response import open_in_browser
from turismo_madrid.utils import extractor_info_with_regex
from turismo_madrid.constants import constants_and_all_xpath
from bs4 import BeautifulSoup


class TurismoMadridSpiderSpider(scrapy.Spider):
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

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "LOG_LEVEL": "INFO",
    }

    base_url = "https://turismomadrid.es"

    def __init__(self, *args, **kwargs):
        super(TurismoMadridSpiderSpider, self).__init__(*args, **kwargs)

        self.output_folder = "raw_data"
        self.output_filename = "turismo_madrid.csv"

        self.path_output = constants_and_all_xpath.path_output
        self.output_folder_name = constants_and_all_xpath.output_folder_name
        self.output_filename_name = constants_and_all_xpath.output_filename_name
        self.output_filename_refine_name = (
            constants_and_all_xpath.output_filename_refine_name
        )

    def parse(self, response):
        all_routes = response.xpath('//a[contains(@class, "enlace-ruta")]')
        if not all_routes:
            self.logger.warning("No existen enlaces para realizar la busqueda")
            return None

        self.logger.info("Existen enlaces para realizar la busqueda")

        for rout_table in all_routes:
            items = TurismoMadridItem()
            items["url_route"] = self.base_url + rout_table.xpath("./@href").get()

            div_data = rout_table.xpath("./div/div")
            title = div_data[1].xpath(".//h2/text()").get()
            items["title"] = title

            items["transport"] = self.base_url + div_data[2].xpath(".//img/@src").get()

            description_movil = div_data[2].xpath(".//p/text()").getall()
            items["distance"] = description_movil[1]
            items["time"] = description_movil[3]

            yield scrapy.Request(
                items["url_route"],
                callback=self.parse_rout_level_1,
                meta={
                    "items_main": items,
                },
                dont_filter=True,
            )

    def parse_rout_level_1(self, response):
        items_main = response.meta.get("items_main")

        all_stage = response.xpath(
            "//div[contains(@class, 'datos-etapa')]//span//text()"
        ).getall()

        items_main["stages"] = all_stage[1]
        div_info = response.xpath('//div[@class="item_fields"]/div/div')[1]
        items_main["url_map_tour"] = self.base_url + div_info.xpath(".//img/@src").get()
        items_main["description"] = div_info.xpath(".//p/text()").get()
        maps = div_info.xpath(".//a/@href").getall()
        items_main["maps_gpx"] = maps[-2]
        items_main["maps_kmz"] = maps[-1]

        if len(maps) == 3:
            items_main["more_info"] = maps[-3]

        # Rutas
        all_stage = response.xpath('//div[@class="item_fields"]/div//a')

        list_stage = []

        for rout in all_stage:
            if not re.search("etapa=\d+$", rout.xpath("./@href").get().strip()):
                # No corresponde a las rutas
                continue

            items_stage = {}

            items_stage["url_stage"] = self.base_url + rout.xpath("./@href").get()

            next_info = rout.xpath("./div/div")

            items_stage["url_image_stage"] = self.base_url + extractor_info_with_regex(
                next_info[0].xpath("./div/@style").get(),  # main_image
                r"url\('(.+)'\);$",  # url
            )

            info_rout = next_info[1].xpath(".//text()").getall()
            items_stage["info_rout"] = [
                data.strip() for data in info_rout if data.strip() != ""
            ]
            # stage
            list_stage.append(items_stage)

        items_main["list_stage"] = list_stage

        for stages in items_main["list_stage"]:
            yield scrapy.Request(
                url=stages["url_stage"],
                callback=self.parse_rout,
                meta={
                    "url": stages["url_stage"],
                    "items_main": items_main,
                },
            )
        # yield items_main

        # for link in items_main["list_stage"]:
        #    print("link", link["url_stage"])

    def parse_rout(self, response):
        url = response.meta.get("url")
        items_main = response.meta.get("items_main")
        print("voy")

        third_items_extractor = {}
        div_description = response.xpath('//div[@class="item_fields"]/div/div[p]')
        description_stage = div_description.xpath(".//p/text()").get()
        maps_gpx_kmz_stage = div_description.xpath(".//a/@href").getall()

        third_items_extractor["description"] = description_stage
        third_items_extractor["maps_gpx"] = maps_gpx_kmz_stage[-2]
        third_items_extractor["maps_kmz"] = maps_gpx_kmz_stage[-1]

        # Itinerarios
        all_info_itinerarios = response.xpath('//div[@class="item_fields"]/a')
        list_itinerario = []
        for itinerario in all_info_itinerarios:
            url_itinerario = self.base_url + itinerario.xpath("./@href").get()
            information = itinerario.xpath(".//text()").getall()
            information = [data.strip() for data in information if data.strip() != ""]
            items = {
                "url_itinerario": url_itinerario,
                "information": information,
            }
            list_itinerario.append(items)

        third_items_extractor["info_itinerarios"] = list_itinerario

        for stages in items_main["list_stage"]:
            if url == stages["url_stage"]:
                stages["info_itinerarios"] = third_items_extractor["info_itinerarios"]
                for url_itinerario in stages["info_itinerarios"]:
                    print(
                        'url_itinerario["url_itinerario"]',
                        url_itinerario["url_itinerario"],
                    )
                    yield scrapy.Request(
                        url=url_itinerario["url_itinerario"],
                        callback=self.parse_itineraty,
                        meta={
                            "url_itineraty": url_itinerario["url_itinerario"],
                            "items_main": items_main,
                        },
                    )

        # yield items_main

    def parse_itineraty(self, response):
        url = response.meta.get("url_itineraty")
        print("voy parse_itineraty", url)
        items_main = response.meta.get("items_main")

        list_place = []

        # dict_place["title"] = response.xpath(
        #    '//h1[@class="nivel1-titulo"]/text()'
        # ).get()

        all_info_pase_to_pase = response.xpath('//*[@id="component"]/div/div[6]/div')
        for one_to_one in all_info_pase_to_pase:
            dict_place = {}

            information = one_to_one.xpath("./div").getall()

            titulo_place = one_to_one.xpath(
                "./div[1]/h3[@class='titulo-punto']/div[@id='texto']/text()"
            ).getall()
            dict_place["titulo_place"] = titulo_place[0]

            description_place_all = one_to_one.xpath("./div[1]/div/p").getall()
            for string in description_place_all:
                soup = BeautifulSoup(string, "html.parser")
                description_place = soup.get_text()

            dict_place["description_place"] = description_place

            all_main_image = information[1]
            match = re.search(r"url\('(.+?)'\)", all_main_image)
            url_main_image = match.group(1)
            dict_place["url_main_image"] = url_main_image

            list_place.append(dict_place)

        for stages in items_main["list_stage"]:
            for iter in stages["info_itinerarios"]:
                if url == iter["url_itinerario"]:
                    iter["place"] = list_place

        yield items_main
