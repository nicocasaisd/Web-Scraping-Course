# Login a Twitter y descarga de Tuits
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargo el WebDriver
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=opts)

# Obtengo la URL semilla
driver.get('https://www.google.com/maps/place/Amaz%C3%B3nico/@40.423706,-3.6872655,17z/data=!4m8!3m7!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423715!4d-3.6850997!9m1!1b1!16s%2Fg%2F11df4t5hhs?entry=ttu')

# Hardcodeo el usuario y password
