# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import ItemData
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy.orm import Session
import os.path


logger = logging.getLogger('mylogger')


Base = declarative_base()


class ShopPositions(object):
    __tablename__ = 'shop_items'
    id = Column(Integer, primary_key = True)
    item_name = Column(String)
    img_url = Column(String)
    item_price = Column(Float)

    def __init__(self, item_name, img_url, item_price):
        self.item_name = item_name
        self.img_url = img_url
        self.item_price = item_price

    def __repr__(self):
        return '<Data %s, %s, %s>' % (self.item_name, self.img_url, self.item_price)


class AnklavPipeline(object):

    def __init__(self):
        basename = os.path.dirname(__file__) + '/db/anklav.db'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)


    def process_item(self, item, spider):
        # if isinstance(item, ItemData):
        # logger.info('Item name is: "{0}" image url is: "{1}"'.format(item['ItemName'], item['ImageURL']))
        sp = ShopPositions(item['ItemName'], item['ImageURL'], item['ItemPrice'])
        self.session.add(sp)

        return item


    def close_spider(self):
        self.session.commit()
        self.session.close()


    def open_spider(self):
        self.session = Session(bind=self.engine)