# Extracción de comentarios de una playlist de youtube
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

# Creo la función para realizar scrolling (NO LA USO)

def obtener_script_scrolling(iteration):
    scrollingScript = """
        window.scrollTo(0,20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

# Instancio el web driver
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)

# Obtengo la url semilla
driver.get('https://www.youtube.com/playlist?list=PLuaGRMrO-j-8NndtkHMA7Y_7798tdJWKH')
sleep(2)

# Obtengo los links a los videos
videos = driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-playlist-video-renderer')
urls_videos = []
for video in videos:
    url = video.find_element(By.XPATH, './/h3/a[@id="video-title"]').get_attribute("href")
    urls_videos.append(url)
    
print(urls_videos)

# Voy a cada url de la lista
for url in urls_videos:
    driver.get(url)
    sleep(3)
    titulo = driver.find_element(By.XPATH, '//div[@id="title"]/h1').text
    print(titulo)
    # Primer scroll para obtener el total de comentarios
    driver.execute_script("""window.scrollTo(0, 8000)""")
    sleep(3)
    # Obtengo el total de comentarios
    total_comentarios = driver.find_element(By.XPATH, '//h2[@id="count"]//span[1]').text
    total_comentarios = int(total_comentarios)
    print(f"Total de comentarios: {total_comentarios}")

    COMENTARIOS_POR_SCROLL = 20
    iteraciones = total_comentarios//COMENTARIOS_POR_SCROLL + 1
    
    # Scrolling
    for i in range(iteraciones):
        driver.execute_script(obtener_script_scrolling(i))
        sleep(3)

    # Obtengo los comentarios
    comentarios = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')
    for comentario in comentarios:
        print(comentario.text)

