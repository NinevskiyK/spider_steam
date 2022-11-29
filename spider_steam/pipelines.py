# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class SpiderSteamPipeline:
    def open_spider(self, spider):
        self.file = open("games.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + '\n'
        if item['date_of_publication'] is not None and item["date_of_publication"][-4:] >= '2000': # Иногда стим просит проверить возраст и как это обойти я не знаю(
            self.file.write(line)
        return item
