from scrapy import cmdline
import sys
#
# if(sys.argv[0]):
#     print(" System args: %s" % sys.argv[0] )
#     cmdline.execute(("scrapy crawl testspider -a url=https://confluence.verndale.com/display/GEHC/Footer+%7C+DOC").split())
#
#
# # cmdline.execute("scrapy crawl createTestCase".split())
cmdline.execute(("scrapy crawl testspider -a "+str(sys.argv[1])).split())
#
#
# #
#


# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
#
# # 'followall' is the name of one of the spiders of the project.
# process.crawl('testspider', url='https://confluence.verndale.com/display/GEHC/Footer+%7C+DOC')
# process.start()
