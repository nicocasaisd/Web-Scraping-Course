from typing import Any
from scrapy.http import Response
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#
from scrapy import Request

class Object(Item):
    titulo_main = Field()
    titulo_iframe = Field()

class W3SCrawler(CrawlSpider):
    name = 'w3s'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    allowed_domains = 'w3schools.com'
    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    download_delay = 2

    def parse(self, response):
        sel = Selector(response)
        titulo_main = sel.xpath('//div[@id="main"]//h1/span/text()').get()

        iframe_url = sel.xpath('//div[@id="main"]//iframe/@src').get()

        iframe_url = 'https://www.w3schools.com/html/' + iframe_url

        yield Request