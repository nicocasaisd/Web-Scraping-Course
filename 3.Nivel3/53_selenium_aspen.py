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
driver.get('https://fmaspen.com/')
print("Empezanding...\n")
sleep(4)
print("Sleep finalizado\n")

# Scrolleamos hasta el final de la pagina
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(4)
print("Sleep de scrolling finalizado\n")

# Clickeamos en el boton de reproduccion

# encuentro el boton
boton = driver.find_element(By.XPATH, '//button[@aria-label="Toggle play"]') # Obtenemos el elemento del DOM
print("Boton encontrado.")
print(boton)
# le doy click
boton.click()
# espero 
sleep(random.uniform(8, 10))



# imprimo los resultados

autor = driver.find_element(By.XPATH, '//span[@class="np__soundbadge_info_small np__song_title"]').text
#descripcion = driver.find_element_by_xpath('.//span[@data-aut-id="itemDetails"]')
titulo = driver.find_element(By.XPATH, '//span[@class="np__info_principal np__artist_name"]').text

print(autor, titulo)