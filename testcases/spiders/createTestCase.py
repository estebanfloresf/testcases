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
    start_urls = ['https://confluence.verndale.com/pages/viewpage.action?spaceKey=GEHC&title=Insights+Module']

    def parse(self, response):
        item = TestCasesItem()
        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')

        for row in table:

            components = row.select('.//td[2]/text() | .//td[2]/p/text()').extract()
            for compName in components:
                item['component'] = "Verify " + str(compName) + " component"
                print('Verify ' + compName + ' Component')
            # This path is usually the one to be used
            xpath = ".//td[3]/div[contains(@class,'content-wrapper')]//*/descendant-or-self::*"

            # This is for general requirements for pages
            # xpath = ".//td[3][contains(@class,'confluenceTd')]//*/descendant-or-self::*"
            requirements = row.select(xpath + "/ul//*/text()").extract()
            wordstolook = ['Recommendation:', 'Optional', 'Required', 'Standard Value:', 'Note:', 'Notes:',
                           'Recommended Dimensions:', 'See']
            wordtojoin = ""
            finalreq = []

            for req in requirements:

                req = req.replace(u'\xa0', u' ').replace(u'&nbsp', u'').strip()
                if (req in wordstolook):
                    wordtojoin = req

                else:
                    if (wordtojoin != ''):
                        finalreq.append(wordtojoin + ' ' + req)
                        wordtojoin = ""
                    else:
                        finalreq.append(req)

            item['generalreq'] = finalreq
            yield item


    # def parse(self, response):
    #     table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')
    #     testitem = ItemLoader()
    #
    #     for row in table:
    #         testitem = ItemLoader(TestCasesItem(), response=response)
    #         components = row.select('.//td[2]/text() | .//td[2]/p/text()').extract()
    #
    #         # Component Names
    #         for compName in components:
    #             testitem.add_value('component', compName)
    #             print('Verify ' + compName + ' Component')
    #
    #             requirements = row.select(".//td[3]/div[contains(@class,'content-wrapper')]/ul/li | .//td[3][contains(@class,'confluenceTd')]/ul/li")
    #             for req in requirements:
    #                 testitem.add_value('generalreq', req.xpath("string()").extract())
    #
    #             yield testitem.load_item()
    #
    #     return testitem
