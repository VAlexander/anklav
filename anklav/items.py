# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class ItemData(Item):
    ItemName = Field()
    ImageURL = Field()
    ItemPrice = Field()


class LinkData(Item):
    LinkURL = Field()