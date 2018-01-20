# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import TestCasesItem


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]
    start_urls = ['https://confluence.verndale.com/display/GEHC/Footer+%7C+DOC']

    def parse(self, response):
        item = TestCasesItem()
        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')

        for index, row in enumerate(table):
            component = row.select('.//td[2]/text() | .//td[2]/p/text()').extract_first()
            print('\n' + str(index) + ' ' + str(component))
            item['component'] = component

            responsive_req = row.xpath(".//td[3]/div[contains(@class,'content-wrapper')]")
            # wordstolook = ['Recommendation:', 'Optional', 'Required', 'Standard Value:', 'Note:', 'Notes:',
            #                'Recommended Dimensions:','See']
            # wordtojoin = ""
            # finalreq = []

            responsive = {}
            resp_devices = []
            resp_general = []
            resp_devices_req = []

            path = ".//div[contains(@class,'confluence-information-macro confluence-information-macro-information conf-macro output-block')]"
            for req in responsive_req.xpath(path):

                # print(req.select("./p/text()").extract_first())

                for elem in req.xpath(" .//div "):
                    resp_devices = elem.xpath("./p/span/text()").extract()
                    resp_general = elem.xpath("./p/text()").extract()

                    # for p in elem.xpath("  ./p"):
                    #
                    #     if(p.select('.//text()').extract_first()):
                    #         print( p.select('.//text()').extract())
                    # print(devices)

                    if (elem.xpath("./ul")):
                        resp_devices_req = self.seekNestedLists(elem,index)
            print(list(zip(resp_devices,resp_devices_req)))


    def seekNestedLists(self, path,index):
        all = []
        for indexUL,ul in enumerate(path.xpath("./ul")):


            if (ul.xpath("./li/text() | ./li/span[not(contains(@class,'confluence-embedded-file-wrapper confluence-embedded-manual-size'))]/text()")):
                # for indexLI,li in enumerate(ul.xpath('./li/text() | ./li/span/text()').extract()):
                all.append(ul.xpath('./li/text() | ./li/span/text()').extract())
        return all
                # if (ul.xpath('./li/ul')):
                #         self.seekNestedLists(ul.xpath('./li'),str(index)+'-'+str(indexLI+1))



