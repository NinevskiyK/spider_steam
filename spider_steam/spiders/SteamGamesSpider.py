import scrapy
from urllib.parse import urlencode
from spider_steam.items import GameItem
from selenium import webdriver
import time

queries = ['Assassins', 'Russia', 'стратегия']

class SteamgamesspiderSpider(scrapy.Spider):
    name = 'SteamGamesSpider'
    allowed_domains = ['store.steampowered.com']
    domain_url = 'http://store.steampowered.com/'

    def start_requests(self, page=1):
        for query in queries:
            for page in ['1', '2']:
                url = self.domain_url + 'search/?' + urlencode(
                    {'term': query, 'page': str(page), 'supportedlang': 'russian'})
                yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        for game_url in response.xpath('//div[@id="search_result_container"]/div/a/@href').getall():
            yield scrapy.Request(url=game_url, callback=self.parse_game, cookies={'mature_content': '1'},
                                 meta={'dont_cache': True})

    def parse_game(self, response):
        game = GameItem()
        name = response.xpath('//div[@class="apphub_AppName"]/text()').get()
        if 'agecheck' in response.url:
            pass # я пытался с селениумом что то придумать но ничего не работало(
        category = response.xpath('//div[@class="breadcrumbs"]/div[@class="blockbg"]/a/text()').getall()
        count_of_reviews = response.xpath('//meta[@itemprop="reviewCount"]/@content').get()
        overall_score = response.xpath(
            '//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').get()
        date_of_publication = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').get()
        developers = response.xpath('//div[@id="developers_list"]/a/text()').getall()
        tags = list(map(lambda x: x.strip(),
                        response.xpath('//div[@class="glance_tags_ctn popular_tags_ctn"]/div/a/text()').getall()))
        disc_price = response.xpath('//div[@class="discount_final_price"]/text()').get()
        avg_price = response.xpath('//div[@class="game_purchase_price price"]/text()').get()
        platforms = response. \
            xpath('//div[@class="game_area_purchase_platform"]/span[contains(@class, "platform_img")]/@class').getall()
        game["name"] = name
        game["category"] = '->'.join(category)
        game["count_of_reviews"] = count_of_reviews
        if overall_score is not None and '%' in overall_score:
            game["overall_score"] = (overall_score.split('%')[0] + '%').strip()[2:]
        game["date_of_publication"] = date_of_publication
        game["developers"] = ', '.join(developers)
        game["tags"] = ', '.join(tags)
        if disc_price is None:
            if avg_price is None:
                game["price"] = '???'
            else:
                game["price"] = avg_price.strip()
        else:
            game["price"] = disc_price.strip()
        game["platforms"] = list(set(map(lambda x: x.split()[1], platforms)))
        yield game
