# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter, JsonItemExporter


class CSVExportPipelines(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        path = 'C:\\Users\\Esteban.Flores\\PycharmProjects\\Scrapy\\testcases\\testcases\\data\\csv\\'
        file = open(path+'%s.csv' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file, include_headers_line=True, join_multivalued='|', lineterminator='\n')
        self.exporter.fields_to_export = ['component','general','responsive']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        required_fields = ['component','general']  # your list of required fields
        if all(field in item for field in required_fields):
            self.exporter.export_item(item)
            return item
        else:
            raise DropItem("Item null")

class JsonExportPipelines(object):

        def __init__(self):
            self.files = {}

        @classmethod
        def from_crawler(cls, crawler):
            pipeline = cls()
            crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
            crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
            return pipeline

        def spider_opened(self, spider):
            path = 'C:\\Users\\Esteban.Flores\\PycharmProjects\\Scrapy\\testcases\\testcases\\data\\json\\'
            file = open(path+'%s.json' % spider.name, 'wb')
            self.files[spider] = file
            self.exporter = JsonItemExporter(file, encoding='utf-8', ensure_ascii=False)
            self.exporter.start_exporting()

        def spider_closed(self, spider):
            self.exporter.finish_exporting()
            file = self.files.pop(spider)
            file.close()

        def process_item(self, item, spider):
            required_fields = ['component']  # your list of required fields
            if all(field in item for field in required_fields):
                self.exporter.export_item(item)
                return item
            else:
                raise DropItem("Item null")
