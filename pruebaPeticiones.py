import requests

url = "http://127.0.0.1:8000/login/"
_data = {
        "username": "prueba1",
        "password": "123456"
    }

r = requests.post(url, data=_data)

res = r.json()

print(res)