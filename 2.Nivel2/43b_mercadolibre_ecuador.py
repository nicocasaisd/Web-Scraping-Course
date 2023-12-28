# Scraping Horizontal y Vertical
from bs4 import BeautifulSoup
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
    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']
    download_delay = 1

    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']

    rules = (
        # REGLA 1 Horizontalidad por Paginacion
        Rule(
            LinkExtractor(
                allow=r'/_Desde_\d+'
            ), follow=True),
        # REGLA 2 Verticalidad al Detalle de los productos
        Rule(
            LinkExtractor(
                allow = r'/MEC-'
            ), follow = True, callback='parse_items'),
    )

    def parse_items(self, response):
        item = ItemLoader(Articulo(), response)
        
        item.add_xpath('titulo', '//h1/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        
        soup = BeautifulSoup(response.body) 
        precio = soup.find(class_="andes-money-amount__fraction")
        precio_completo = precio.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '') # texto de todos los hijos
        item.add_value('precio', precio_completo)


        yield item.load_item()
