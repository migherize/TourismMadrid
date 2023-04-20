"""
Araña para extraer información de la url = https://turismomadrid.es/es/rutas.html
author: Miguel Herize
mail: migherize@gmail.com
"""
import re
import scrapy
from os import path, getcwd
from turismo_madrid.items import TurismoMadridItem
from turismo_madrid.utils import extractor_info_with_regex
from bs4 import BeautifulSoup


class TurismoMadridSpider(scrapy.Spider):
    """
    Esta araña de Scrapy se encarga de extraer información de la página web de itinerarios
    turísticos de Madrid. La información extraída incluye 3 fases:
        * Rutas: sendero de lugares a conocer por etapas como turista.
        * Etapas: un camino lleno de itinerarios.
        * itinerarios: un paso a paso de lugares a conocer.
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

    def parse(self, response):
        """
        Funcion para raspar los itinerarios
        """
        all_routes = response.xpath('//a[contains(@class, "enlace-ruta")]')
        if not all_routes:
            self.logger.warning("No existen enlaces para realizar la busqueda")
            return None

        self.logger.info(
            "Existen enlaces para realizar la busqueda: %s", len(all_routes)
        )

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
        """
        Funcion para raspar las rutas
        """
        items_main = response.meta.get("items_main")

        all_stage = response.xpath(
            "//div[contains(@class, 'datos-etapa')]//span//text()"
        ).getall()

        items_main["stages"] = all_stage[1]
        div_info = response.xpath('//div[@class="item_fields"]/div/div')[1]
        items_main["url_map_tour"] = self.base_url + div_info.xpath(".//img/@src").get()
        items_main["description"] = div_info.xpath(".//p/text()").get()
        maps = div_info.xpath(".//a/@href").getall()
        items_main["maps_gpx"] = self.base_url + maps[-2]
        items_main["maps_kmz"] = self.base_url + maps[-1]

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

            info_all = [data.strip() for data in info_rout if data.strip() != ""]
            if len(info_all) == 3:
                items_stage["info_rout"] = info_all[0]
                items_stage["info_title"] = info_all[1]
                items_stage["info_distance"] = info_all[2]
            else:
                items_stage["info_rout"] = info_all[0]
                items_stage["info_title"] = info_all[1]
                items_stage["info_distance"] = ""

            # stage
            list_stage.append(items_stage)

        items_main["list_stages"] = list_stage

        for stages in items_main["list_stages"]:
            yield scrapy.Request(
                url=stages["url_stage"],
                callback=self.parse_rout,
                meta={
                    "url": stages["url_stage"],
                    "items_main": items_main,
                },
            )

    def parse_rout(self, response):
        """
        Funcion para raspar los itinerarios en las rutas.
        """
        url = response.meta.get("url")
        items_main = response.meta.get("items_main")

        third_items_extractor = {}
        div_description = response.xpath('//div[@class="item_fields"]/div/div[p]')
        description_stage = div_description.xpath(".//p/text()").get()
        maps_gpx_kmz_stage = div_description.xpath(".//a/@href").getall()

        third_items_extractor["description"] = description_stage
        if maps_gpx_kmz_stage:
            if len(maps_gpx_kmz_stage) == 2:
                third_items_extractor["maps_gpx"] = (
                    self.base_url + maps_gpx_kmz_stage[-2]
                )
                third_items_extractor["maps_kmz"] = (
                    self.base_url + maps_gpx_kmz_stage[-1]
                )
            else:
                third_items_extractor["maps_gpx"] = ""
                third_items_extractor["maps_kmz"] = ""

        else:
            third_items_extractor["maps_gpx"] = ""
            third_items_extractor["maps_kmz"] = ""

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

        div_description = response.xpath('//div[@class="item_fields"]/div/div[p]')
        description_stage = div_description.xpath(".//p/text()").get()
        maps_gpx_kmz_stage = div_description.xpath(".//a/@href").getall()

        for stages in items_main["list_stages"]:
            if url == stages["url_stage"]:
                stages["stage_description"] = description_stage
                if maps_gpx_kmz_stage:
                    stages["stage_maps_gpx"] = self.base_url + maps_gpx_kmz_stage[-2]
                    stages["stage_maps_kmz"] = self.base_url + maps_gpx_kmz_stage[-1]
                else:
                    stages["stage_maps_gpx"] = ""
                    stages["stage_maps_kmz"] = ""
                stages["info_itinerarios"] = third_items_extractor["info_itinerarios"]
                for url_itinerario in stages["info_itinerarios"]:
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
        """
        Funcion para raspar los lugares y los itinerarios
        """
        url = response.meta.get("url_itineraty")
        items_main = response.meta.get("items_main")

        list_place = []

        all_info_pase_to_pase = response.xpath('//*[@id="component"]/div/div[6]/div')
        for one_to_one in all_info_pase_to_pase:
            dict_place = {}

            information = one_to_one.xpath("./div").getall()

            titulo_place = one_to_one.xpath(
                "./div[1]/h3[@class='titulo-punto']/div[@id='texto']/text()"
            ).getall()
            dict_place["titulo_place"] = titulo_place[0]

            description_place_all = one_to_one.xpath("./div[1]/div/p").getall()
            description_place = ""
            for string in description_place_all:
                soup = BeautifulSoup(string, "html.parser")
                description_place = soup.get_text()

            dict_place["description_place"] = description_place
            if len(information) == 2:
                all_main_image = information[1]
                match = re.search(r"url\('(.+?)'\)", all_main_image)
                url_main_image = match.group(1)
            else:
                url_main_image = ""

            dict_place["url_main_image"] = url_main_image

            list_place.append(dict_place)

        for stages in items_main["list_stages"]:
            if "info_itinerarios" in stages:
                for itinerarios in stages["info_itinerarios"]:
                    if url == itinerarios["url_itinerario"]:
                        itinerarios["place"] = list_place

        yield items_main
