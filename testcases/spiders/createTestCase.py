# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import TestCasesItem


class createTestCaseSpider(scrapy.Spider):
    name = "createTestCase"
    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]
    start_urls = ['https://confluence.verndale.com/pages/viewpage.action?spaceKey=GEHC&title=Generic+Hero']

    def parse(self, response):
        item = TestCasesItem()
        table =  response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody')

        # print(len(table))

        for row in table:
            components = row.select('.//tr/td[2]/text() | .//tr/td[2]/p/text()').extract()
            # for comp in components:
            #
            #     item['Component_Name'] = str(comp)
            #     yield item
            look = ".//tr[3]/td[3]/div[contains(@class,'content-wrapper')]"
            # requirements = row.select(look+"//*/string(p)  | "+look+"//*/ul/li/text()[normalize-space(.)]  | "+look+"//*/ul/li/span/text()[normalize-space(.)]  | "+look+"//*/ul/li/strong/span/text()[normalize-space(.)] ").extract()
            requirements = row.select(look+"//*/descendant-or-self::*/text()[normalize-space()] ").extract()


            # This is working manually hard coded
            # requirements =  row.select(look+"//*/text()[normalize-space()]").extract()
            # wordsout = ['Recommendation:','Optional','Required','Standard Value','Note:','Recommended Dimensions:']
            # save = ""
            for i,req in enumerate (requirements):
                req = req.replace(u'\xa0', u' ').strip()
                print(req)
            #
            #
            #     if(req in wordsout):
            #         save = req
            #
            #     else :
            #         if(save!=''):
            #             print(save+' '+req)
            #             save=""
            #         else:
            #             print(req)




