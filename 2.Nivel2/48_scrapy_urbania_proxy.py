# Scraping de varias paginas del mismo dominio
# Fabricando los links

from scrapy import Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
#
from scrapy.crawler import CrawlerProcess


'''
Instalamos la libreria de ScrapeOps usando:

pip install scrapeops-scrapy-proxy-sdk

'''

# Establecemos la API_KEY
API_KEY = '28efb0dd-9b36-47c1-a1c6-cb6a47d1cb04'

class Departamento(Item):
    nombre = Field()
    direccion = Field()


class Urbaniape(CrawlSpider):
    name = "Departamentos"
    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'CLOSESPIDER_ITEMCOUNT': 20,
        # Custom Settings para Scrapeops
        'SCRAPEOPS_API_KEY' : API_KEY,
        'SCRAPEOPS_PROXY_ENABLED' : True,
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
        }
    }

    allowed_domains = ['urbania.pe']

    start_urls = [
        'https://urbania.pe/buscar/proyectos-propiedades?page=1',
        #'https://urbania.pe/buscar/proyectos-propiedades?page=2',
        #'https://urbania.pe/buscar/proyectos-propiedades?page=3',
        #'https://urbania.pe/buscar/proyectos-propiedades?page=4',
        #'https://urbania.pe/buscar/proyectos-propiedades?page=5',
        #'https://urbania.pe/buscar/proyectos-propiedades?page=6'
    ]

    #download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto/'
            ), follow=True, callback="parse_depto"
        ),
    )

    def parse_depto(self, response):
        sel = Selector(response)
        item = ItemLoader(Departamento(), sel)

        item.add_xpath('nombre', '//div[@class="development-title-container"]/h1[@class="title"]/text()', MapCompose(lambda i: i.replace('\n', '').replace('\t', '').replace('\r', '')))
        item.add_xpath('direccion', '//div[@class="development-title-container"]/p[@class="subtitle"]/text()', MapCompose(lambda i: i.replace('\n', '').replace('\t', '').replace('\r', '')))

        yield item.load_item()

# EJECUCION DESDE SCRIPT
 
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'Departamentos.json'
})
process.crawl(Urbaniape)
process.start()