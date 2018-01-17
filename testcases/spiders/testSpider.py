# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["www.google.com"]
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        print("Hello")
        pass
