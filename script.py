import requests
import base64

URL_Login = "https://pdf.finkok.com/api/login/"
URL_Upload ="https://pdf.finkok.com/api/pdfs/upload/"


#Credenciales de envio
Data_Login = {
    "username": "pcervantes@quadrum.com.mx",
    "password": "2524!It!pl@!"
}

response = requests.post(URL_Login, json=Data_Login)

#para obtener el token o si es el caso mensaje de error
if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    expiry = data.get('expiry')
    print(f'Token: {token}')
    print(f'Expiry: {expiry}')
else:
    print(f'Error: {response.status_code}, {response.text}')

#sesion id 
sessionid = '5lhm9n2amos9g4xom5oxe10hq0w115gl'

#obtenemos los headers
headers = {
    'Authorization':f'Token {token}',
    'Cookie': f'sessionid={sessionid}'
}

files ={
    'cfdi': ('cfdi.xml', open('/home/spineda/Documentos/Actividades Desarrollo/script/cfdi.xml','rb'))
}

#solicitud para generar el pdf
upload_response = requests.post(URL_Upload, headers=headers, files=files)

#validamos si se envio correctamente con el status 200
if upload_response.status_code == 200:
    print("Solucitid enviada exitosamente")
    print(upload_response.status_code)
    data = upload_response.json()
    documents = data.get('documents', [])
    # iteramos documents para ontener content y guardarlo en una variable
    for document in documents:
        content_base64 = document.get('content', '')
        print('Base 64 Obtenido Satisfactoriamente')

        #Imprimir el PDF
        user_input = input("Desea Generar el pdf? (si/no):")
        if user_input.lower() == "si":
            decodificacion = base64.b64decode(content_base64)

            #Guardar el pdf
            with open('Factura_xml.pdf', 'wb') as f:
                f.write(decodificacion)
                
        else:
            print('Exit')

else:
    print(f'Error: {upload_response.status_code}, {upload_response.text}')



