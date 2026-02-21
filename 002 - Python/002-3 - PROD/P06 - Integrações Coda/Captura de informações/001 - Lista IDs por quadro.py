import requests

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

url = "https://coda.io/apis/v1/docs"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    documentos = response.json().get("items", [])
    if not documentos:
        print("Nenhum documento encontrado com este token.")
    else:
        for doc in documentos:
            print(f"Nome: {doc['name']} | DOC_ID: {doc['id']} | URL: https://coda.io/d/_d{doc['id']}")
else:
    print(f"Erro ao buscar documentos: {response.status_code}")
    print(response.text)
