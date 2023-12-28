
# Extraemos información sobre los idiomas disponibles en la página de 
#  inicio de Wikipedia.org

import requests
from lxml import html

# Definimos la seed
URL = "https://www.wikipedia.org/"

# Definimos los encabezados

# User Agent define que tipo de cliente está haciendo la request. Por defecto es "ROBOT"

encabezados = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# Realizamos el requerimiento web

respuesta = requests.get(URL, headers=encabezados)

parser = html.fromstring(respuesta.text)

# Obtenemos el dato usando get_element_by_id()
print("\t\t *** Un solo elemento.\n")
español = parser.get_element_by_id("js-link-box-es")
print(español.text_content())

# Obtenemos el dato usando XPATH

ingles = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(ingles)

# Obtenemos todos los idiomas de la página
print("\t\t *** Múltiples elementos.\n")

idiomas_v1 = parser.xpath("//a[starts-with(@id, 'js-link-box')]/strong/text()")
print(idiomas_v1)

idiomas_v2 = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
for idioma in idiomas_v2:
    print(idioma)

idiomas_v3 = parser.find_class('central-featured-lang')
for idioma in idiomas_v3:
    print(idioma.text_content().strip())
