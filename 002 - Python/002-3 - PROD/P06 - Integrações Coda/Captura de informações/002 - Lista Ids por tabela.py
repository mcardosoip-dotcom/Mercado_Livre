import requests

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "2uRaxzXW8e"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
URL = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables"

params = {"limit": 100}
todas_tabelas = []

while True:
    response = requests.get(URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Erro {response.status_code}: {response.text}")
        break

    data = response.json()
    items = data.get("items", [])
    print(f"Tabelas retornadas nesta página: {len(items)}")
    todas_tabelas.extend(items)

    next_token = data.get("nextPageToken")
    if not next_token:
        break
    params["pageToken"] = next_token

# Listar tabelas
print(f"\nTotal de tabelas encontradas: {len(todas_tabelas)}\n")
for t in todas_tabelas:
    print(f"Nome da tabela: {t['name']} | ID: {t['id']}")
