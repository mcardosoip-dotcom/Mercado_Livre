# ================================================
# Descrição :  Essa integração insere em uma tabela CODA informações sobre a base 
#              e sua data de atualização, para manter o controle de quando as bases 
#              foram atualizadas
# Autor : Marcelo Cardoso
# ================================================

import requests
import json

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "Ic-fjbuxrg"
TABLE_ID = "grid-V67OFKQKzT"

COLUMN_IDS = {
    "coluna_1": "c-uZYUtZr-W7",
    "coluna_2": "c-qXtOoEwd9N"

}

def inserir_dados_2(val1, val2):
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "rows": [
            {
                "cells": [
                    {"column": COLUMN_IDS["coluna_1"], "value": val1},
                    {"column": COLUMN_IDS["coluna_2"], "value": val2}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 202:
        print("Dados inseridos com sucesso.")
    else:
        print(f"Erro ao inserir dados: {response.status_code} - {response.text}")
