# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from items import ItemData


class AnklavSpider(scrapy.Spider):
    name = "anklav"
    allowed_domains = ["anklav.ua"]
    start_urls = [#'http://anklav.ua/',
                  # 'http://anklav.ua/5001-kompyuteryi-seti/',
                  'http://anklav.ua/5014-zaschitnyie-plenki-i-stekla-dlya-planshetov/',
                  # 'http://anklav.ua/5012-planshetyi/',
                 ]

    def parse(self, response):
        self.logger.info(response.url)

        links = response.xpath('//a[@class="cat_name"]/@href').extract()
        if len(links) > 0:
            for next_link in links:
                next_link = response.urljoin(next_link)
                yield scrapy.Request(next_link, callback=self.parse)

        for item in response.xpath('//div[@class="productbox hover"]').extract():
            selector = Selector(text=item)
            yield self.parse_item(selector)



    # def parse_item(self, selector):
    #     newItem = ItemData()
    #     l = ItemLoader(newItem,selector=selector)
    #     l.add_xpath('ItemName', '//h5/a/text()')
    #     l.add_xpath('ImageURL', '//a[@class="product_image"]/img[@class="secondimg"]/@src')
    #     l.add_xpath('ItemDescr', '//div[@class="description"]/text()')
    #
    #     return l.load_item()


    def parse_item(self, selector):
        newItem = ItemData()
        newItem['ItemName'] = selector.xpath('//h5/a/text()')
        newItem['ImageURL'] = selector.xpath('//a[@class="product_image"]//img[@class="secondimg"]/@src')
        newItem['ItemPrice'] = selector.xpath('//p[@class="price_container"]/span[@class="price"]/text()')

        return newItem