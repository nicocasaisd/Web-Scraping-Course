import requests

headers = {
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true'

response = requests.get(url_api, headers=headers)

data = response.json()

