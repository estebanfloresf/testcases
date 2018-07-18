from scrapy import cmdline
import os
import inspect
import logging

path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))  # script directory

print('Main File executed')

# To generate the verified labels from the input excel (uncomment line below)
# os.system('python '+path+'\\utils\\generateTC.py')
# To Make a scrape of the confluence page (uncomment line below)
# cmdline.execute("scrapy crawl createTestCase".split())

# To read excel file
os.system('python '+path+'\\utils\\readTestCases.py')
