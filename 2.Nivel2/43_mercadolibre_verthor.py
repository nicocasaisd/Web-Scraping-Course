# Scraping Horizontal y Vertical

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

# Definimos la abstraccion a extraer
class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

# Definimos la clase core
class MercadolibreCrawler(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    start_urls = ['https://listado.mercadolibre.com.ar/deportes-fitness/artes-marciales-boxeo/_NoIndex_True?original_category_landing=true']
    download_delay = 1

    allowed_domains = ['listado.mercadolibre.com.ar', 'mercadolibre.com.ar', 'articulo.mercadolibre.com.ar']

    rules = (
        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ), follow=True

        ),
        # Detalle de los productos
        Rule(
            LinkExtractor(
                allow = r'/MLA'
            ), follow = True, callback='parse_item'

        ),
    )

    def parse_item(self, response):
        item = ItemLoader(Articulo(), response)
        
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()')
        item.add_xpath('precio', '//div[@class="ui-pdp-price__main-container"]//span[@class="andes-money-amount__fraction"]//text()')

        yield item.load_item()
