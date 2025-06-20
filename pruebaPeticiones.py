import requests

url = "http://127.0.0.1:8000/login/"
_data = {
        "username": "prueba1",
        "password": "123456"
    }

r = requests.post(url, data=_data)

res = r.json()
print(f"Peticion de login: {res}")

if "token" in res:
    token = f"Token {res['token']}"
    url = "http://127.0.0.1:8000/products/products/"
    headers = {
        "Authorization": token}
    r = requests.get(url, headers=headers)
    data = r.json()
    print(f"Peticion de listado: {data}")
