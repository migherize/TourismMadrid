# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TurismoMadridItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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
    list_stage = scrapy.Field()
