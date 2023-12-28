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

class Departamento(Item):
    nombre = Field()
    direccion = Field()


class Urbaniape(CrawlSpider):
    name = "Departamentos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'CLOSESPIDER_ITEMCOUNT': 20
    }

    start_urls = [
        'https://urbania.pe/buscar/proyectos-propiedades?page=1',
        'https://urbania.pe/buscar/proyectos-propiedades?page=2',
        'https://urbania.pe/buscar/proyectos-propiedades?page=3',
        'https://urbania.pe/buscar/proyectos-propiedades?page=4',
        'https://urbania.pe/buscar/proyectos-propiedades?page=5',
        'https://urbania.pe/buscar/proyectos-propiedades?page=6'
    ]

    # def start_requests(self):
    #         yield Request(
    #              url="https://urbania.pe/buscar/proyectos-propiedades?page=1", 
    #              callback=self.parse_depto
    #              )
    #         yield Request("https://urbania.pe/buscar/proyectos-propiedades?page=2", self.parse_depto)
    #         yield Request("https://urbania.pe/buscar/proyectos-propiedades?page=3", self.parse_depto)

    allowed_domains = ['urbania.pe']

    download_delay = 1

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

        item.add_xpath('nombre', '//div[@class="development-title-container"]/h1[@class="title"]/text()', MapCompose(lambda i: i.strip()))
        item.add_xpath('direccion', '//div[@class="development-title-container"]/p[@class="subtitle"]/text()', MapCompose(lambda i: i.strip()))

        yield item.load_item()