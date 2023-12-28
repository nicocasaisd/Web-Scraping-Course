# Scraping Vertical y Horizontal a 2 niveles

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

# Abstraccion a extraer
class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()
    hotel = Field()

# CrawlSpider
class TripAdvisor(CrawlSpider):
    name = "OpinionesTripAdvisor"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 30
    }

    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    download_delay = 1


    rules = (
        # (H) Paginacion de Hoteles
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True
        ),
        # (V) Detalle de Hoteles
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@data-automation="hotel-card-title"]/a']
            ), follow=True
        ),
        # (H) Paginacion de Opiniones dentro de un hotel
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        # (V) Detalle de perfil de usuario
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]//a[contains(@class, "ui_header_link")]']
            ), follow=True, callback='parse_opinion'

        ),
    )

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')

        autor = sel.xpath('//h1/span/text()').get()
       
       
       
        ''' DEBUG DE UNA SPIDER'''
        #if autor is None:
            #inspect_response(response, self)
            #open_in_browser(response)

        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath('titulo', './/div[@class="AzIrY b _a VrCoN"]/text()')
            item.add_xpath('contenido', './/q/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
            item.add_xpath('calificacion', './/div[contains(@class, "ui_card section")]//a/div/span/@class', MapCompose(self.get_calification))
            item.add_xpath('hotel', './/div[contains(@class, "ui_card section")]//a/div/div/div/div[contains(@class, "ui_link")]/text()')
            
            yield item.load_item()

    def get_calification(self, text):
        return text.split('_')[-1]