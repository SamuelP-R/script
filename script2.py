import requests
import base64

URL_Login = "https://pdf.finkok.com/api/login/"
URL_Upload = "https://pdf.finkok.com/api/pdfs/upload/"

# Credenciales de envío
Data_Login = {
    "username": "pcervantes@quadrum.com.mx",
    "password": "2524!It!pl@!"
}

response = requests.post(URL_Login, json=Data_Login)

# Para obtener el token o si es el caso mensaje de error
if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    expiry = data.get('expiry')
    print(f'Token: {token}')
    print(f'Expiry: {expiry}')
else:
    print(f'Error: {response.status_code}, {response.text}')
    exit()

# Sesión ID
sessionid = '5lhm9n2amos9g4xom5oxe10hq0w115gl'

# Obtenemos los headers
headers = {
    'Authorization': f'Token {token}',
    'Cookie': f'sessionid={sessionid}'
}

# Abrir el archivo cfdi.xml
with open('/home/spineda/Documentos/Actividades Desarrollo/script/cfdi.xml', 'rb') as file:
    files = {
        'cfdi': ('cfdi.xml', file)
    }
    try:
        # Solicitud para generar el PDF
        upload_response = requests.post(URL_Upload, headers=headers, files=files)
        upload_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        exit()

# Validamos si se envió correctamente con el status 200
if upload_response.status_code == 200:
    print("Solicitud enviada exitosamente")
    print(upload_response.status_code)
    data = upload_response.json()
    documents = data.get('documents', [])
    if not documents:
        print("No se encontraron documentos en la respuesta.")
        exit()

    # Iteramos documents para obtener content y guardarlo en una variable
    for document in documents:
        content_base64 = document.get('content', '')
        if content_base64:
            print('Base 64 Obtenido Satisfactoriamente')

            # Imprimir el PDF
            user_input = input("Desea Generar el pdf? (si/no):")
            if user_input.lower() == "si":
                try:
                    decodificacion = base64.b64decode(content_base64)
                    # Guardar el PDF
                    with open('Factura_xml.pdf', 'wb') as f:
                        f.write(decodificacion)
                except base64.binascii.Error as e:
                    print(f"Error al decodificar el contenido Base64: {e}")
            else:
                print('Exit')
        else:
            print("El contenido base64 está vacío o no es válido.")
else:
    print(f'Error: {upload_response.status_code}, {upload_response.text}')