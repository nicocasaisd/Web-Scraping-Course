#import random
#from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# Importamos lo necesario para hacer la espera por Eventos
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Cargo el driver de Chrome
driver = webdriver.Chrome()
print("Driver Cargado. \n")

# Obtengo la pagina objetivo
driver.get('https://www.olx.in')
print("Empezanding...\n")

print("Sleep finalizado\n")

# Clickeamos en el boton 'Cargar más' 3 veces

for i in range(2):
    try:
        # Espera por Evento
        # encuentro el boton
        wait = WebDriverWait(driver, 10)
        boton = wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]')))
        # le doy click
        boton.click()
        print("Click nro", i)
        # Espero que carge la informacion dinámica de las tarjetas
        nro_anuncios = 20 + ( (i+1)*20 ) # 20 anuncios iniciales y 20 más por cada click
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.presence_of_element_located( (By.XPATH, '//li[@data-aut-id="itemBox"][' + str(nro_anuncios) + ']')))
    except:
        # Si ocurre un error, rompo el bucle
        break

# Todos los anuncios (DOM) en una lista
anuncios = driver.find_elements(By.XPATH, './/li[@data-aut-id="itemBox"]')

print("Total de anuncios: ", len(anuncios))

# La recorro e imprimo los resultados
for anuncio in anuncios:
    precio = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
    #descripcion = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemDetails"]')
    titulo = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text

    print(titulo,",", precio)