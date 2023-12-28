
# Ejemplo de Scraping Vertical en TripAdvisor

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


#Definimos nuestra abstraccion

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"
        ),
    )

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class="gbXAQ"]/text()')
        #item.add_xpath('descripcion', '//div[@class="fIrGe _T"]/text()') 
            #Evitamos usar selectores con nombres de clases raros porque se cambian periodicamente
        item.add_xpath('descripcion', '//div[contains(@data-ssrev-handlers, "Description")]//div[1]/text()')
        item.add_xpath('amenities', '//div[contains(@data-ssrev-handlers, "amenities")]/div/div[@data-test-target]/text()')

        yield item.load_item()

