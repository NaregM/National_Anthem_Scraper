import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scrapy
from scrapy import Selector
from scrapy.http import Response, HtmlResponse, TextResponse
from scrapy.crawler import CrawlerProcess

import requests

import urllib

import os
import sys

import time

import re

from urllib.request import Request, urlopen

import pickle

# -----------------------------------------------------------------------------------------------------------------------

NA_dict = dict()

req = Request('http://www.nationalanthems.info/', headers={'User-Agent': 'Chrome'})
webpage_html = urlopen(req).read().decode("utf8")  # decode because req is in bytes

sel = Selector(text = webpage_html)
country_list = [x[32:][:-4] for x in sel.xpath('//a[contains(@href, ".htm")]/@href').extract()]

# -----------------------------------------------------------------------------------------------------------------------

class YourSpider(scrapy.Spider):

    name = 'yourspider'

    def start_requests(self):

        for c in countries[:20]:

            yield scrapy.Request(url = "http://www.nationalanthems.info/" + c + ".htm", callback=self.parse)

    def parse(self, response):

        national_anthem = ' '.join(response.xpath('//div[text()="English translation"]/following::div/text()').extract())

        if len(national_anthem) == 0:

            national_anthem = ' '.join(response.xpath('//div[text()="English lyrics"]/following::div/text()').extract())

        if len(national_anthem) == 0:

            return

        national_anthem = re.sub('\n', " ", national_anthem)
        national_anthem = re.sub('\r', " ", national_anthem)
        national_anthem = re.sub('\t', " ", national_anthem)


        c = ' '.join(response.xpath('//title/text()').extract())
        c = re.sub(' – nationalanthems.info', '', c)

        NA_dict[c] = national_anthem


# Run the Spider
process = CrawlerProcess()
process.crawl(YourSpider)
process.start()

df = pd.DataFrame.from_dict(NA_dict, orient = 'index', columns = ["National Anthem"])

df.to_csv('national_anthems.csv')
pickle.dump(df, open( "national_anthems.pickle", "wb" ))
