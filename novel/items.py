# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    count = scrapy.Field()

class CatPicItem(scrapy.Item):
    picUrl = scrapy.Field()
