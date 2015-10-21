# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    alias_title = scrapy.Field()
    content = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    cover_url = scrapy.Field()
    read_count = scrapy.Field()
    comment = scrapy.Field()