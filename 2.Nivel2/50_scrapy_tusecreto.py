# Scraping de tusecreto.com.ar (web.archive.org)

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#
from scrapy.shell import inspect_response
#
from scrapy.crawler import CrawlerProcess
#
import re
from datetime import datetime
#
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class Secreto(Item):
    id = Field()
    fecha = Field()
    edad = Field()
    sexo = Field()
    cuerpo = Field()

class TuSecretoCrawler(CrawlSpider):
    name = 'tusecreto_crawler'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        #'DEPTH_LIMIT': 1, # Para definir que solo se vaya a un nivel de profundidad
        'FEED_EXPORT_ENCODING': 'utf-8', # Para evitar problemas con codificacion de simbolos
        'CLOSESPIDER_PAGECOUNT':10,
        #'CONCURRENT_REQUESTS': 4,
    }
    
    allowed_domains = ['web.archive.org']

    start_urls = [
        'https://web.archive.org/web/20051110224553/http://tusecreto.com.ar/index.php?show=4',
        'https://web.archive.org/web/20060428034856/http://www.tusecreto.com.ar/', #2006-04-28
        'https://web.archive.org/web/20050829050156/http://www.tusecreto.com.ar/', #2005-08-29
        'https://web.archive.org/web/20050810000134/http://www.tusecreto.com.ar/', #2005-08-10

    ]

    download_delay = 1

    rules = (
            Rule(
                LinkExtractor(
                    allow=r'index.php\?show=\d+',
                    restrict_xpaths='//div[@id="navegador"]'
                ), follow=True, callback="parse_start_url"
            ),
        )
    
    ids_seen = set()

    def parse_start_url(self, response):

        sel = Selector(response)

        secretos = sel.xpath('//table[@class="secretos"]')
        print(response.url)
        #inspect_response(response, self)
        download_delay = 0.5

        

        for secreto in secretos:
            
            item = ItemLoader(Secreto(), secreto)

            # Obtenemos la ID
            numero = secreto.xpath('.//th[@class="numero"]/text()').get()
            numero = int(numero)

            # Obtenemos EDAD y SEXO
            datos = secreto.xpath('.//th[@class="datos"]/text()').get()
            # Edad
            edad = re.findall(r"\d+", datos)
            # Sexo
            sexo = datos.split("|")[-1].replace("Sexo:", "").strip()

            #Obtenemos FECHA
            fecha_str = secreto.xpath('.//th[@class="fecha"]/text()').get()
            fecha = datetime.strptime(fecha_str, "Fecha: %d.%m.%Y %H:%M")

            #Obtenemos el cuerpo del SECRETO
            cuerpo = secreto.xpath('.//td[@class="secreto"]/text()').getall()
            cuerpo = "".join(cuerpo)

            print(numero)
            print(edad)
            print(sexo)
            print(fecha)
            print(cuerpo)
            
            if numero in self.ids_seen:
                #inspect_response(response, self)
                #raise DropItem(f"Duplicate item found: {numero!r}")
                continue
            else:
                self.ids_seen.add(numero)
                
                item.add_value('id', numero)
                item.add_value('edad', edad)
                item.add_value('sexo', sexo)
                item.add_value('fecha', fecha)
                item.add_value('cuerpo', cuerpo)

            yield item.load_item()

# EJECUCION DESDE SCRIPT
 
# process = CrawlerProcess({
#     'FEED_FORMAT': 'csv',
#     'FEED_URI': 'tusecreto_debug.csv'
# })
# process.crawl(TuSecretoCrawler)
# process.start()


# PIPELINES

""" class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item
 """