# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TurismoMadridItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    route_name = scrapy.Field()
    title = scrapy.Field()
    distance = scrapy.Field()
    time = scrapy.Field()
    stages = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    map_kmz = scrapy.Field()
    map_gpx = scrapy.Field()
    list_stages = scrapy.Field()
