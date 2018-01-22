# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestCasesItem(scrapy.Item):
    component = scrapy.Field()
    requirements = scrapy.Field()
    responsive = scrapy.Field()
    pass


class Requirements(scrapy.Item):
    # type => general or device accordingly
    # type = scrapy.Field()
    level = scrapy.Field()
    description = scrapy.Field()
    pass


class ResponsiveReq(scrapy.Item):
    device = scrapy.Field()
    requirements = scrapy.Field()
    pass
