import requests

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "2uRaxzXW8e"       # Substitua pelo ID do seu documento
TABLE_ID = "grid-67NNi0uPuz"    # Substitua pelo ID da tabela (pode obter com GET /tables)

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/columns"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    colunas = response.json().get("items", [])
    for col in colunas:
        print(f"Nome da Coluna: {col['name']} | ID: {col['id']}")
else:
    print(f"Erro ao buscar colunas: {response.status_code}")
    print(response.text)
