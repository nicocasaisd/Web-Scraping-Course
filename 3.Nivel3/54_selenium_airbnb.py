from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Instanciamos el Web Driver usando opciones
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)

# Hacemos el request a la página principal
driver.get('https://www.airbnb.com.ar/')

sleep(10)

# Cerramos el boton del pop-up que nos aparece
boton_cerrar = driver.find_element(By.XPATH, '//button[@aria-label="Cerrar"]')
print("Cerrando pop-up...")
boton_cerrar.click()

sleep(5)

# Obtenemos los titulos de los anuncios

print("Comenzando...")
titulos_anuncios = driver.find_elements(By.XPATH, '//div[@itemprop="itemListElement"]//div[@data-testid="listing-card-title"]')

for titulo in titulos_anuncios:
    print(titulo.text)