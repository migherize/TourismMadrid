# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import json
from itemadapter import ItemAdapter


class TurismoMadridPipeline:
    collection_name = "scrapy_items"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.items = []
        # self.client = pymongo.MongoClient(self.mongo_uri)
        # self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # self.items.append(dict(item))

        item_exists = False
        for i, stored_item in enumerate(self.items):
            if stored_item["url_route"] == item["url_route"]:
                # Si el artículo ya existe, reemplazarlo con el nuevo artículo
                print("reemplazar")
                self.items[i] = dict(item)
                item_exists = True
                break
        # Si el artículo no existe en la lista, agregarlo a la lista
        if not item_exists:
            print("nuevo")
            self.items.append(dict(item))

        return item

    def close_spider(self, spider):
        with open("output.json", "w") as f:
            json.dump(self.items, f, indent=4)
