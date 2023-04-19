import sys

sys.path.append("/Users/migherize/Sourcetree/TourismMadrid-1/")
import unittest

# from scrapy.utils.test import get_crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.turismo_madrid.turismo_madrid.spiders.turismo_madrid_spider import (
    TourismMadridSpider,
)


class TestScrapy(unittest.TestCase):
    def test_spider_runs_successfully(self):
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(
            TourismMadridSpider
        )  # Usamos la clase de la araña, no una instancia
        process.start()
        self.assertTrue(TourismMadridSpider.successful)


if __name__ == "__main__":
    unittest.main()
