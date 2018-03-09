from scrapy import cmdline
import sys
#
# if(sys.argv[0]):
#     print(" System args: %s" % sys.argv[0] )
#     cmdline.execute(("scrapy crawl testspider -a url=https://confluence.verndale.com/display/GEHC/Footer+%7C+DOC").split())
#
#
cmdline.execute("scrapy crawl createTestCase".split())
# cmdline.execute(("scrapy crawl testspider -a "+str(sys.argv[1])).split())
#
#
# #
