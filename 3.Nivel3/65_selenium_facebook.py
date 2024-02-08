# Extracción de datos de una pagina de Facebook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Funciones

def soft_scroll(driver, start):
    step = 10
    end = start + 2000
    for i in range(start, end, step):
        driver.execute_script(f"window.scrollTo(0, {i})")
    
    return end

# Instancio el web driver
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
#opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)

# Obtengo la url semilla
driver.get('https://www.facebook.com/elcorteingles')
sleep(2)

# Cierro el pop-up de login
btn_cerrar = driver.find_element(By.XPATH, '//div[@aria-label="Cerrar"]')
btn_cerrar.click()

# Iteraciones de scrolling 
print("Iniciando soft scrolling")
#soft_scroll(driver, 0)
start = 0

for i in range(5):
    start = soft_scroll(driver, start)
    print(i, start)

    # Obtenemos los articulos
    articulos = driver.find_elements(By.XPATH, '//div[@aria-describedby and @role="article"]')
    print(f"Cant articulos: {len(articulos)}")

    sleep(3)

# Imprimimos en pantalla el resultado
for articulo in articulos:
    mensaje = articulo.find_element(By.XPATH, '(.//div[@data-ad-preview="message"])[1]').text
    reacciones = articulo.find_element(By.XPATH, './/span[@class="x1e558r4"]').text
    
    print(mensaje,'Reacciones:' ,reacciones)


sleep(5)

