# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from ..items import TestCasesItem, Responsive, Requirements
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class TestspiderSpider(scrapy.Spider):
    name = "testspider"

    settings = get_project_settings()
    http_user = settings.get('HTTP_USER')
    http_pass = settings.get('HTTP_PASS')
    allowed_domains = ["confluence.verndale.com"]

    def __init__(self, url):
        super(TestspiderSpider, self).__init__()
        self.start_urls = [url]

    def parse(self, response):

        table = response.xpath('//*[@id="main-content"]/div/div[4]/div/div/div[1]/table/tbody/tr')

        for index, row in enumerate(table):
            testcase = TestCasesItem()
            if index > 0:
                testcase['component'] = str(row.select('.//td[2]/text() | .//td[2]/p/text()').extract_first()).strip()

                request = Request(
                    self.start_urls[0],
                    callback=self.responsive_req,
                    errback=self.errback_httpbin,
                    dont_filter=True
                )
                request.meta['testcase'] = testcase
                request.meta['row'] = row

                yield request



    def responsive_req(self, response):

        testcase = response.meta['testcase']
        row = response.meta['row']
        devices = []   # List to store all the responsive dict

        # Section Responsive Notes
        responsive_path = row.xpath(".//td[3]/div[contains(@class,'content-wrapper')]")
        path = ".//div[contains(@class,'confluence-information-macro confluence-information-macro-information conf-macro output-block')]"
        for req in responsive_path.xpath(path):

            for device in req.xpath(".//div/p/span/text()").extract():
                # Save Devices
                responsive = Responsive()
                responsive['device'] = str(device).strip(':')
                request = Request(
                    self.start_urls[0],
                    callback=self.requirements,
                    errback=self.errback_httpbin,
                    dont_filter=True
                )
                request.meta['responsive'] = responsive
                request.meta['row'] = row

                yield request
                # After creating the item appended to the devices list

                devices.append(responsive)

        # Final testcase is added the devices and requirements for each
        testcase['responsive'] = devices
        yield testcase

    def requirements(self,response):
        devices = ['Desktop','Tablet','Mobile','Desktop/Tablet','Tablet/Mobile']
        responsive = response.meta['responsive']
        requirements = []
        path = ".//div[contains(@class,'confluence-information-macro-body')]//*/text()"

        for elem in response.xpath(path).extract():
            if(str(elem).strip(':') not in responsive['device']):
                requirements.append(str(elem).strip())

        responsive['requirements'] = requirements
        yield responsive





    # Function for handling Errors
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
