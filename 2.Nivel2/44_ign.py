# Scraping en 3 Dimensiones

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    tipo = Field()
    titulo = Field()
    contenido = Field()

class Review(Item):
    tipo = Field()
    titulo = Field()
    calificacion = Field()

class Video(Item):
    tipo = Field()
    titulo = Field()
    fecha_de_publicacion = Field()

# Core Class

class IgnCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 30
    }
    allowed_domains = ['latam.ign.com']
    download_delay = 1
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5&order_by=']

    rules = (
        # Horizontalidad por tipo de información
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        # Horizontalidad por paginacion
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ), follow=True
        ),
        # Regla por cada tipo de contenido donde ire verticalmente
        #REVIEWS
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_review'
        ),
        #NEWS
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news'
        ),
        #VIDEOS
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_video'
        ),
    )



    def parse_news(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_value('tipo', 'news')
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('contenido', '//div[@id="id_text"]//*/text()')

        yield item.load_item()


    
    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_value('tipo', 'review')
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('calificacion', '//div[@class="review"]//span[@class="side-wrapper side-wrapper hexagon-content"]/div/text()')

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_value('tipo', 'video')
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('fecha_de_publicacion', '//span[@class="publish-date"]/text()')

        yield item.load_item()


    
