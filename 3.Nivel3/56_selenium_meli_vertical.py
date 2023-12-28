# Extraer el titulo y precio de los productos de MeLi

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#
from time import sleep

# Cargo el Driver de Chrome
opts = Options()
#opts.add_argument("--headless")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=opts)

# Obtengo la URL semilla
driver.get('https://listado.mercadolibre.com.ec/herramientas-vehiculos/')

# Cierro el pop-up de cookies para que no moleste
try:
    btn_cookies = driver.find_element(By.XPATH, '//button[@data-testid="action:understood-button"]')
    btn_cookies.click()
    print("Pop-up de cookies cerrado.")
except Exception as e:
    print(e)


print("Comenzando...")
sleep(1)

# Obtengo el nro de paginas
#nro_paginas = driver.find_element(By.XPATH, '//div[@class="ui-search-pagination"]//li[@class="andes-pagination__page-count"]')
#nro_paginas = nro_paginas.text.split(' ')[1]
nro_paginas = 3
print(nro_paginas)
pagina_actual = 1



while pagina_actual <= nro_paginas:

    # Obtengo titulo y precio de los productos
    items = driver.find_elements(By.XPATH, '//section[@class="ui-search-results"]//ol//li')

    lista_de_links = []
    # Imprimo en pantalla
    print("pagina:",pagina_actual," len:",len(items))

    for item in items:
        link = item.find_element(By.XPATH, './/a[contains(@class, "ui-search-item__group__element")]')
        lista_de_links.append(link.get_attribute("href"))


        #titulo = item.find_element(By.XPATH, './/h2[@class="ui-search-item__title"]')
        #precio = item.find_element(By.XPATH, './/div[@class="ui-search-price__second-line"]')
        #precio = "".join(precio.text).replace('\n', '')
        #print(titulo.text, "," , precio)

    #print(lista_de_links)

    for link in lista_de_links[:5]:

        try:
            driver.get(link)
            sleep(0.5)
            titulo = driver.find_element(By.XPATH, '//h1').text
            precio = driver.find_element(By.XPATH, '//div[@id="price"]').text
            precio = "".join(precio).replace('\n',"")

            print(titulo, precio)
            driver.back()
        except:
            print("Error")
            driver.back()

    # Obtengo el boton
    #boton = driver.find_element(By.XPATH, '//div[@class="ui-search-pagination"]//li[@class="andes-pagination__button andes-pagination__button--next"]')
    try:
        boton = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        boton.click()
    except:
        break

    pagina_actual += 1
    #sleep(3)


driver.close()