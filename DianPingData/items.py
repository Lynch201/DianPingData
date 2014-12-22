# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()


class DianPingTag(scrapy.Item):
    tag = scrapy.Field()
    url = scrapy.Field()


class ShopDetail(scrapy.Item):
    name = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
    tel = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    link = scrapy.Field()
