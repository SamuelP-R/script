import requests

URL = "https://pdf.finkok.com/api/login/"

Data = {
    "username": "spineda@finkok.com.mx",
    "password": "Residente_Spr#25"
}

response = requests.post(URL, json=Data)

if response.status_code == 201:
    data = response.json()

    print('Token obtenido con exito')
    print('Respuesta', data)
else:
    print('Error en lasolicitud, detalles:', response.text)