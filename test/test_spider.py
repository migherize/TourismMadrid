"""
Test para webscrapy en https://turismomadrid.es/es/rutas.html con unittest
author: Miguel Herize
mail: migherize@gmail.com
"""
import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.turismo_madrid.turismo_madrid.spiders.turismo_madrid_spider import (
    TourismMadridSpider,
)


class TestScrapy(unittest.TestCase):
    """
    Clase para probar la araña TourismMadridSpider en la página https://turismomadrid.es/es/rutas.html
    """

    def test_spider_runs_successfully(self):
        """
        Prueba que comprueba que la araña se ejecuta correctamente en la página web de Turismo Madrid.
        """
        # Configuramos el proceso de rastreo
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        
        # Iniciamos el proceso de rastreo
        process.crawl(TourismMadridSpider)
        process.start()

        # Verificamos que la araña se ha ejecutado correctamente
        self.assertTrue(TourismMadridSpider.successful)


if __name__ == "__main__":
    unittest.main()
