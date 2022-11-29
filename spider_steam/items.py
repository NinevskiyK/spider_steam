# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    count_of_reviews = scrapy.Field()
    overall_score = scrapy.Field()
    date_of_publication = scrapy.Field()
    developers = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
    pass
