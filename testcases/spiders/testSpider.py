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
    start_urls = ['https://confluence.verndale.com/display/GEHC/Primary+Navigation+-+DOC']

    def parse(self, response):
        item = TestCasesItem()
        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')


        for index,row in enumerate(table):
            components = row.select('.//td[2]/text() | .//td[2]/p/text()').extract_first()
            print('\n'+str(index)+' '+str(components))

            # for comp in components:
            #     item['Component_Name'] = str(comp)

            requirements = row.xpath(".//td[3]/div[contains(@class,'content-wrapper')]")
            # wordstolook = ['Recommendation:', 'Optional', 'Required', 'Standard Value:', 'Note:', 'Notes:',
            #                'Recommended Dimensions:','See']
            # wordtojoin = ""
            # finalreq = []

            responsivereq = ".//div[contains(@class,'confluence-information-macro confluence-information-macro-information conf-macro output-block')]"
            for req in requirements.xpath(responsivereq):

                print(req.select("./p/text()").extract_first())

                # for elem in req.xpath(" .//div/p | .//div/ul/li"):
                #     if (elem.xpath("string(.//text())").extract_first() != ""):
                #         print(elem.xpath("string(.//text())").extract_first())

                for elem in req.xpath(" .//div "):

                    if(elem.xpath(".//p/span/text()").extract()):
                        for p in elem.xpath(".//p/span/text()"):
                            print("parrafo")
                    #
                    # if (elem.xpath("./ul")):
                    #     print("Lista")

                    # for subtitle in elem.xpath(".//p/text()  | .//p/span/text()").extract():
                    #     print(subtitle)
                    #     self.seekChildNodes(elem)




    def seekChildNodes(self,path):
       if(len(path.xpath(".//ul"))>0):
           for elem in path.xpath("string(.//ul/li/text())").extract():
              print(elem)
