# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import TestCasesItem, ResponsiveReq, Requirements


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]
    start_urls = ['https://confluence.verndale.com/display/GEHC/Footer+%7C+DOC']

    def parse(self, response):
        testcase = TestCasesItem()

        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')

        for index, row in enumerate(table):
            responsive = ResponsiveReq()
            requirements = Requirements()
            component = row.select('.//td[2]/text() | .//td[2]/p/text()').extract_first()
            print('\n' + str(index) + ' ' + str(component))
            testcase['component'] = component

            # Section Responsive Notes
            responsive_req = row.xpath(".//td[3]/div[contains(@class,'content-wrapper')]")
            path = ".//div[contains(@class,'confluence-information-macro confluence-information-macro-information conf-macro output-block')]"
            for req in responsive_req.xpath(path):

                for elem in req.xpath(" .//div "):
                    # Save Devices

                    devices = elem.xpath("./p/span/text()").extract()

                    # Save General Requirements from Responsive Notes
                    for req in elem.xpath("./p/text()").extract():
                        responsive['requirements'] = str(req).strip()


                    levelpath = "/ul"
                    parentLevel = 0
                    band = 0
                    finalresreq = []

                    while (elem.xpath('.' + levelpath + '/li')):

                        for ulnum, ul in enumerate(elem.xpath('.' + levelpath)):

                            for linum, li in enumerate(ul.xpath('./li | ./li/span')):
                                itemreq = {}
                                key = str(ulnum) + '.' + str(linum)
                                if (band > 0): key += '.' + str(band)
                                if (li.xpath('./text()').extract()):
                                    # print(key +' ' +str(li.xpath('./text()').extract_first()))
                                    itemreq[str(key)] = li.xpath('./text()').extract_first()
                                    itemreq['device'] = devices[ulnum]

                                    finalresreq.append(itemreq)

                                if (li.xpath('./ul').extract()):
                                    band = linum

                        levelpath += '/li/' + levelpath
                        parentLevel += 1
                    print(finalresreq)

                    # responsive['requirements']= finalresreq
            testcase['responsive'] = [dict(responsive)]
            yield testcase
