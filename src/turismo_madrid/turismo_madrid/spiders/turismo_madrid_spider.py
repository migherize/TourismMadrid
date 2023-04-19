"""
Araña para extraer información de la url = https://turismomadrid.es/es/rutas.html
author: Miguel Herize
mail: migherize@gmail.com
"""
import re
import os
import scrapy

import requests
from pathlib import Path

from scrapy.utils.response import open_in_browser

from ..items import TurismoMadridItem
from ..utils import extractor_info_with_regex
from ..constants import constants_and_all_xpath

from os import path, getcwd


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
        all_routes = response.xpath(constants_and_all_xpath.xpath_url_routes)

        if not all_routes:
            self.logger.warning("No existen enlaces para realizar la busqueda")
            return None

        self.logger.info("Existen enlaces para realizar la busqueda")

        first_items_extractor = {
            "url_rout": "",
            "url_main_image": "",
            "main_header": "",
            "main_description": "",
            "url_image_movil": "",
            "distancia": "",
            "duracion": "",
        }

        for rout_table in all_routes:
            # ----------------------------------------------------------------------------
            # extraer la url de la ruta
            first_items_extractor["url_rout"] = (
                self.base_url
                + rout_table.xpath(constants_and_all_xpath.xpath_href).get()
            )

            # ----------------------------------------------------------------------------
            # extraer la informacion de cada ruta de turismo
            div_data = rout_table.xpath(constants_and_all_xpath.xpath_info_first_table)

            # a) url de la imagen principal
            url_main_image = extractor_info_with_regex(
                div_data[0]
                .xpath(constants_and_all_xpath.xpath_style)
                .get(),  # main_image
                r"url\('(.+)'\);$",  # url
            )
            first_items_extractor["url_main_image"] = self.base_url + url_main_image

            # b) Informacion de la cabecera
            first_items_extractor["main_header"] = (
                div_data[1].xpath(constants_and_all_xpath.xpath_header_2).get()
            )

            # c) Descripcion principal
            first_items_extractor["main_description"] = (
                div_data[1].xpath(constants_and_all_xpath.xpath_paragraph).get()
            )

            # d) url de la imagen del metodo de viaje
            first_items_extractor["url_image_movil"] = (
                self.base_url
                + div_data[2].xpath(constants_and_all_xpath.xpath_image).get()
            )

            description_movil = (
                div_data[2].xpath(constants_and_all_xpath.xpath_paragraph).getall()
            )
            first_items_extractor["distancia"] = description_movil[1]
            first_items_extractor["duracion"] = description_movil[3]
            # print("first_items_extractor", first_items_extractor)
        yield first_items_extractor
