# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings


class createTestCaseSpider(scrapy.Spider):
    name = "createTestCase"
    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]
    start_urls = ['https://confluence.verndale.com/display/GEHC/Highlights+Module']

    def parse(self, response):

        for url in self.start_urls:

            # requirements = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr[3]')
            #
            #
            # for row in requirements:
            #     item = row.select('.//text()').extract()
            #     print('Verify '+str(item)+' component')


            components = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')
            for row in components:
                item = row.select('.//text()').extract()
                print('Verify '+item[1]+' component')
