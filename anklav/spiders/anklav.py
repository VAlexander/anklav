# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import ItemData, LinkData


class AnklavSpider(scrapy.Spider):
    name = "anklav"
    allowed_domains = ["anklav.ua"]
    start_urls = [
                  'http://anklav.ua/5001-kompyuteryi-seti/',
                  'http://anklav.ua/5113-smartfonyi-telefonyi/',
                  'http://anklav.ua/5135-ofis/',
                  'http://anklav.ua/5172-foto/',
                  'http://anklav.ua/5198-tv-audio-video/',
                  'http://anklav.ua/5225-byitovaya-tehnika/',
                  'http://anklav.ua/5310-detskie-tovaryi/',
                  'http://anklav.ua/5372-vse-dlya-doma/',
                  'http://anklav.ua/5411-avtozvuk-video-navigatsiya/',
                  'http://anklav.ua/5419-sport-otdyih/',
                  'http://anklav.ua/5456-instrumenty/',
                 ]

    def parse(self, response):
        self.logger.info(response.url)

        links = response.xpath('//a[@class="cat_name"]/@href').extract()
        if len(links) > 0:
            for next_link in links:
                next_link = response.urljoin(next_link)
                yield scrapy.Request(next_link, callback=self.parse)

        yield self.register_link(response.url)
        for item in response.xpath('//div[@class="productbox hover"]').extract():
            selector = Selector(text=item)
            yield self.parse_item(selector)


    def parse_item(self, selector):
        newItem = ItemData()
        newItem['ItemName'] = selector.xpath('//h5/a/text()').extract_first()
        newItem['ImageURL'] = selector.xpath('//a[@class="product_image"]//img[@class="secondimg"]/@src').extract()[0]
        if selector.xpath('//p[@class="price_container"]').extract_first() is not None:
            newItem['ItemPrice'] = selector.xpath('//p[@class="price_container"]/span[@class="price"]/text()').extract_first()
        else:
            newItem['ItemPrice'] = 'N/A'

        return newItem


    def register_link(self, url):
        newLinkData = LinkData()
        newLinkData['LinkURL'] = url

        return newLinkData