# ================================================
# Descrição :  Essa integração faz parte da atualização dos status na plataforma CODA, 
#              sendo chamada em todas as fases anteriores, o que gera um histórico completo
# Autor : Marcelo Cardoso
# ================================================

import requests
import json

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "Ic-fjbuxrg"
TABLE_ID = "grid-FmA6REyD_8"

COLUMN_IDS = {
    "coluna_1": "c-HdzHbi8hVj",
    "coluna_2": "c-yC6KtIa24c",
    "coluna_3": "c-FtQIMT14rV",
    "coluna_4": "c-O__Y5Lt6OD",
    "coluna_5": "c-KOKQ7E8VU6",
    "coluna_6": "c-9_NohSSV6i",

}

def inserir_dados(val1, val2, val3,val4,val5,val6):
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
                    {"column": COLUMN_IDS["coluna_2"], "value": val2},
                    {"column": COLUMN_IDS["coluna_3"], "value": val3},
                    {"column": COLUMN_IDS["coluna_4"], "value": val4},
                    {"column": COLUMN_IDS["coluna_5"], "value": val5},
                    {"column": COLUMN_IDS["coluna_6"], "value": val6}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 202:
        print("Dados inseridos com sucesso.")
    else:
        print(f"Erro ao inserir dados: {response.status_code} - {response.text}")
