import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Cargo el driver de Chrome
driver = webdriver.Chrome('./chromedriver-linux64/chromedriver')
print("Driver Cargado. \n")

# Obtengo la pagina objetivo
driver.get('https://www.olx.in/cars_c84')
print("Empezanding...\n")
sleep(4)
print("Sleep finalizado\n")

# Clickeamos en el boton 'Cargar más' 3 veces

for i in range(3):
    try:
        # encuentro el boton
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]') # Obtenemos el elemento del DOM
        # le doy click
        boton.click()
        # espero 
        sleep(random.uniform(8, 10))
    except:
        # Si ocurre un error, rompo el bucle
        break

# Todos los anuncios (DOM) en una lista
autos = driver.find_elements(By.XPATH, './/li[@data-aut-id="itemBox"]')

print("Total de autos: ", len(autos))

# La recorro e imprimo los resultados
for auto in autos:
    precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
    #descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemDetails"]')
    titulo = auto.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text

    print(titulo, precio)