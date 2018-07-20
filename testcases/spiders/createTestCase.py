# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import TestCasesItem
from scrapy.loader import ItemLoader


class createTestCaseSpider(scrapy.Spider):
    name = "createTestCase"
    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]
    start_urls = ['https://confluence.verndale.com/display/GEHC/Pagination']

    def parse(self, response):
        item = TestCasesItem()
        title = response.xpath('//*[@id="title-text"]/a/text()').extract_first()
        print('Documentation: '+title)
        table_xpath = '//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr'
        table = response.xpath(table_xpath)

        for index, row in enumerate(table):
            if (index > 0):
                components = row.select('.//td[2]/text() | .//td[2]/p/text()').extract()
                for compName in components:
                    item['component'] = str(compName)
                    print('Verify ' + compName + ' Component')
                # This path is usually the one to be used
                component_xpath = ".//td[3][contains(@class,'confluenceTd')]"

                description = ""
                if (row.select(component_xpath + "/a/text()").extract()):
                    requirements = row.select(component_xpath + "/a/text()").extract()
                    description = "|".join(requirements)
                else:
                    if (row.select(component_xpath + "/ul//*/text()").extract()):
                        requirements = row.select(component_xpath + "/ul//*/text()").extract()
                        description = "|".join(requirements)
                    else:
                        if (row.select(component_xpath +"/div"+ "/ul//*/text()").extract()):
                            requirements = row.select(component_xpath +"/div"+ "/ul//*/text()").extract()
                            description = "|".join(requirements)

                item['general'] = str(description)
                yield item
