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
    start_urls = ['https://confluence.verndale.com/pages/viewpage.action?spaceKey=GEHC&title=Primary+Navigation+-+DOC']

    def parse(self, response):
        item = TestCasesItem()
        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')


        for row in table:

            components = row.select('.//td[2]/text() | .//td[2]/p/text()').extract()
            for comp in components:
                item['Component_Name'] = str(comp)

                requirements = row.select(
                    ".//td[3]/div[contains(@class,'content-wrapper')]//*/descendant-or-self::*/text()[normalize-space()]").extract()
                wordstolook = ['Recommendation:', 'Optional', 'Required', 'Standard Value:', 'Note:', 'Notes:',
                               'Recommended Dimensions:','See']
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

                item['Requirements'] = finalreq
                yield item
                # print(comp+' Component has been generated')
                print('Verify '+comp+' Component')
