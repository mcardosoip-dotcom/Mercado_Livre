import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import time

# Importa utilitário de caminhos cross-platform
from utils_caminhos import get_caminho_stage

API_TOKEN = "6a15d8f3-e27e-454e-80d6-ff2b04957e25"
DOC_ID = "Ic-fjbuxrg"
TABLE_ID = "grid-FmA6REyD_8"


COLUMN_IDS = {
    "col_data": "c-HdzHbi8hVj",
    "col_fluxo": "c-yC6KtIa24c",
    "col_processo": "c-FtQIMT14rV",
    "col_inicio": "c-O__Y5Lt6OD",
    "col_fim": "c-KOKQ7E8VU6",
    "col_status": "c-9_NohSSV6i",
}

def inserir_dados(val1, val2, val3, val4, val5, val6):
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "rows": [
            {
                "cells": [
                    {"column": COLUMN_IDS["col_data"], "value": val1},
                    {"column": COLUMN_IDS["col_fluxo"], "value": val2},
                    {"column": COLUMN_IDS["col_processo"], "value": val3},
                    {"column": COLUMN_IDS["col_inicio"], "value": val4},
                    {"column": COLUMN_IDS["col_fim"], "value": val5},
                    {"column": COLUMN_IDS["col_status"], "value": val6}
                ]
            }
        ]
    }
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print("Dados inseridos com sucesso.")
            return

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                wait_time = 5 * (2 ** attempt)  # 5, 10, 20, 40, 80 segundos
                print(f"Erro ao inserir dados: 429 - Too Many Requests. Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                print(f"Erro ao inserir dados: {err.response.status_code} - {err.response.text}")
                return
        
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            return

    print("Falha ao inserir dados após várias tentativas.")

def gerar_e_enviar_dados_hoje():
    
    processos_completos = [
        "Limpeza de cash",
        "Movimentação de arquivos baixados por RPA",
        "Ajuste de arquivos corrompidos eLAW",
        "Renomear arquivos eLAW",
        "Backup de arquivos eLAW",
        "Backup de arquivos Salesforce",
        "Mover arquivos eLAW para pasta final",
        "Data Self Information - Base ativa.xlsx",
        "Data Self Information - Entradas e desfechos.xlsx",
        "Data Self Information - TPN e SI.xlsx",
        "Push Controle Operacional.xlsx",
        "Push Acompanhamento de Tarefas.xlsx",
        "Push dashboard Penal - Quantidade.xlsx",
        "Push legales MLA e MLM.xlsx",
        "Push projeto FAAS.xlsx",
        "Push inf MLA e MLM.xlsx",
        "Push Pagamentos em Garantia.xlsx",
        "Push Aguardando Informações.xlsx",
        "Extrato - Base comite.xlsx",
        "Push e informações - DRE.xlsx",
        "Push Conta Invadida.xlsx",
        "Data Self Information Trabalhista - Base ativa.xlsx",
        "Data Self Information Trabalhista - Entradas e desfechos.xlsx",
        "Coração de fogo - Database.xlsx",
        "Coração de fogo - Geral.xlsx",
        "Upload de arquivo - Data Self Information - Base ativa.csv",
        "Upload de arquivo - Data Self Information - Entradas e desfechos.csv",
        "Upload de arquivo - Pagamentos em garantia.csv",
        "Upload de arquivo - CSV Amélia.csv",
        "Macro Tarefas Agendamentos Clean.xlsx",
        "Criaçao de arquivo CSV | Base Ativa",
        "Criaçao de arquivo CSV | Entradas e desfechos",
        "Criaçao de arquivo CSV | Pagamentos em garantia",
        "Criação de arquivo CSV | CSV Amélia",
        "Push de informações NPS.xlsx",
        "Push de informações Nostradamus.xlsx",
        "Push Reclamos Laborales.xlsx",
        "Push Tercerizados Corp.xlsx",
        "Upload de arquivos de Buckets",
        "Mesa de entrada MySQL->BigQuery"
    ]
    
    data_do_relatorio = datetime.now()
    
    processos_dia = list(processos_completos)
    
    if random.random() > 0.5:
        num_a_remover = random.randint(1, 5)
        processos_a_remover = random.sample(processos_dia, num_a_remover)
        for p in processos_a_remover:
            processos_dia.remove(p)
            
    tempo_total_min = random.uniform(120, 192)
    
    tempo_total_min *= (len(processos_dia) / len(processos_completos))
    
    if tempo_total_min < len(processos_dia):
        tempo_total_min = len(processos_dia)
        
    tempos_processos = [random.uniform(0.5, 1.5) for _ in range(len(processos_dia))]
    tempo_total_atual = sum(tempos_processos)
    
    tempos_ajustados = [t * (tempo_total_min / tempo_total_atual) for t in tempos_processos]
    
    hora_inicio_dia = datetime(data_do_relatorio.year, data_do_relatorio.month, data_do_relatorio.day, 7, 0, 0)
    hora_inicio_dia += timedelta(minutes=random.randint(0, 160))
    
    hora_processo_atual = hora_inicio_dia
    
    dados = []
    
    for j, processo in enumerate(processos_dia):
        fluxo = "Diário"
        status = "Processamento Ok"
        
        duracao_processo_segundos = tempos_ajustados[j] * 60
        hora_fim_processo = hora_processo_atual + timedelta(seconds=duracao_processo_segundos)
        
        dados.append([
            data_do_relatorio.strftime('%d/%m/%Y'),
            fluxo,
            processo,
            hora_processo_atual.strftime('%H:%M:%S'),
            hora_fim_processo.strftime('%H:%M:%S'),
            status
        ])
        
        hora_processo_atual = hora_fim_processo

    INTERVALO_ENTRE_INSERCOES = 3  # segundos entre cada inserção (evita 429 Too Many Requests)
    for linha in dados:
        inserir_dados(linha[0], linha[2], linha[3], linha[4], linha[5], linha[1])
        time.sleep(INTERVALO_ENTRE_INSERCOES)

if __name__ == "__main__":
    gerar_e_enviar_dados_hoje()


def inserir_dados_2(val1, val2):
    DOC_ID = "Ic-fjbuxrg"
    TABLE_ID = "grid-V67OFKQKzT"

    COLUMN_IDS = {
        "coluna_1": "c-uZYUtZr-W7",
        "coluna_2": "c-qXtOoEwd9N"
    }

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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("Dados inseridos com sucesso.")
    except requests.exceptions.HTTPError as err:
        print(f"Erro ao inserir dados: {err.response.status_code} - {err.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")

diretorio_stage = get_caminho_stage()

for arquivo in os.listdir(diretorio_stage):
    caminho = os.path.join(diretorio_stage, arquivo)
    
    if os.path.isfile(caminho):
        data_update = datetime.fromtimestamp(os.path.getmtime(caminho))
        nome_base = os.path.splitext(arquivo)[0]
        inserir_dados_2(nome_base, data_update.isoformat())
        time.sleep(5)