# Scrolling para carga dinámica de la web y manejo de múltiples tabs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

# Cargo el WebDriver
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=opts)

# Obtengo la URL semilla
driver.get('https://www.google.com/maps/place/Amaz%C3%B3nico/@40.423706,-3.6872655,17z/data=!4m8!3m7!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423715!4d-3.6850997!9m1!1b1!16s%2Fg%2F11df4t5hhs?entry=ttu')

# Espero que cargue la web inicial
sleep(random.uniform(7,9))

print("Comenzando el scrolling..")

# Hago el scrolling hasta el final
SCROLLS = 0
while (SCROLLS != 1):
    driver.execute_script("""
        recuadro = document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf ')[0]
        recuadro.scroll(0, recuadro.scrollHeight)
        """)
    sleep(random.uniform(5,6))
    SCROLLS += 1


# Obtengo todas las reviews de la página
reviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not (@aria-label)]')

for review in reviews:

    user_link = review.find_element(By.XPATH, './/button[@data-href and @aria-label]')

    try:
        user_link.click()   # Voy al perfil de usuario
        print("Click en perfil de usuario");sleep(1)
        driver.switch_to.window(driver.window_handles[1]) # Cambio a la nueva pestaña
        print("Cambio a nueva pestaña");sleep(1)
        try:
            driver.find_element(By.XPATH, '//button[@data-tab-index="0"]').click() # Clickeo en el tab reseñas
        except:
            pass
        print("Click en el tab reseñas");sleep(1)

        # Scrolleamos el recuadro de User Reviews
        for i in range(3):
            user_reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located( (By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]') )
            )
            driver.execute_script("""
                userReviews = document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf ')[0]
                userReviews.scroll(0, userReviews.scrollHeight)
            """)
            sleep(random.uniform(5,6))
        
        # Obtenemos los User Reviews
        user_reviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not (@aria-label)]')

        for user_review in user_reviews:
            titulo = user_review.find_element(By.XPATH, './/div[@class="d4r55 YJxk2d"]').text
            span_puntaje = user_review.find_element(By.XPATH, './/span[@class="kvMYJc"]')
            puntaje = span_puntaje.get_attribute('aria-label')

            print(titulo, " - " ,puntaje)
    
    # Cierro la pestaña de perfil de usuario
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(1)




    except Exception as e:
        print(e)
        driver.close()
        sleep(1)
    
    #break



#driver.close()