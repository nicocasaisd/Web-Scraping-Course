# Login a Twitter y descarga de Tuits
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#
from time import sleep

# Cargo el WebDriver
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=opts)


# Obtengo datos de login del archivo .env (usando python-dotenv)
try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file \n")

except Exception as e:
    print(f"Error loading .env file {e}")
    sys.exit(1)

user = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")


# Obtengo la URL semilla
driver.get('https://twitter.com/i/flow/login')

sleep(2)

# Login
input_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]'))
)
input_user.send_keys(user)
input_user.send_keys(Keys.RETURN)
sleep(2)
input_password = driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
input_password.send_keys(password)
input_password.send_keys(Keys.RETURN)
print("Login exitoso.")
sleep(3)

# Obtengo los Tuits del timeline
# El proceso es ineficiente e incompleto pero así está enseñado en el curso
print("Obteniendo los tweets...  \n")

tweets = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located( (By.XPATH, '//article[@data-testid="tweet"]//div[@dir="auto"]'))
)
#tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]//div[@dir="auto"]')
for tweet in tweets:
    print(tweet.text)

sleep(15)
