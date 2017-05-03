# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# douguo Spider Item
# @author zhangjianfei
# @date 2017/04/07

import scrapy


class DgspiderUrlItem(scrapy.Item):
    url = scrapy.Field()


class DgspiderPostItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
