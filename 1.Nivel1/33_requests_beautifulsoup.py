# StackOverflow

# Extraemos el título y la descripcion de las preguntas de la pagina principal

import requests
from bs4 import BeautifulSoup


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

url = "https://stackoverflow.com/questions/"


respuesta = requests.get(url, headers= headers)

soup = BeautifulSoup(respuesta.text, features="lxml")

contenedor_de_preguntas = soup.find(id="questions")
lista_de_preguntas = contenedor_de_preguntas.find_all('div',class_="js-post-summary")

for pregunta in lista_de_preguntas:
    texto_pregunta = pregunta.find('h3').text
    descripcion_pregunta = pregunta.find(class_="s-post-summary--content-excerpt").text
    descripcion_pregunta = descripcion_pregunta.strip()
    #print(texto_pregunta)
    #print(descripcion_pregunta)
    print()

# Obtengo el elemento 'h3' y me muevo hacia su elemento hermano

print("*************************************************")

for pregunta in lista_de_preguntas:
    elemento_texto_pregunta = pregunta.find('h3')
    descripcion_pregunta = elemento_texto_pregunta.find_next_sibling('div').text.strip()

    print(descripcion_pregunta)
    
