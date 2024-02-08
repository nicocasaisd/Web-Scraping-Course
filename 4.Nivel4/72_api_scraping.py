import requests
import pandas as pd

headers = {
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

cursos_totales = []

for i in range(1,2):
    print(f"***********Iteracion {i}")
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=' + str(i)

    response = requests.get(url_api, headers=headers)

    data = response.json()

    cursos = data['courses']

    for curso in cursos:
        cursos_totales.append(
            {
                "titulo":curso['title'],
                "num_reviews":curso['num_reviews'],
                "rating":curso['rating']
            }
        )


df = pd.DataFrame(cursos_totales)

print(df)

df.to_csv('cursos_udemy.csv')