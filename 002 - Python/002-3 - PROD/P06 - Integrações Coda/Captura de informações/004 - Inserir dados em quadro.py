import requests
import json

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "Ic-fjbuxrg"
TABLE_ID = "grid-FmA6REyD_8"

url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

dados = {
    "rows": [
        {
            "cells": [
                {"column": "c-HdzHbi8hVj", "value": "Exemplo A"},
                {"column": "c-yC6KtIa24c", "value": "Exemplo B"},
                {"column": "c-FtQIMT14rV", "value": "Exemplo C"},
                {"column": "c-jHVPh7Jh4D", "value": "Exemplo D"}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(dados))

if response.status_code == 202:
    print("Linha inserida com sucesso.")
else:
    print(f"Erro ao inserir linha: {response.status_code}")
    print(response.text)
