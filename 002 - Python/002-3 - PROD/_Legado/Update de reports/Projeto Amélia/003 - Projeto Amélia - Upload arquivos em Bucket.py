# ================================================
# Descrição :  Este processo faz a carga de UM ARQUIVO ESPECÍFICO no ambiente do Mercado Livre 
#              através de uma conexão Google com autenticação de usuário
# Autor : Marcelo Cardoso
# ================================================

import os
from datetime import datetime
from google.cloud import storage
from google.api_core.retry import Retry
import sys

# Adiciona o caminho do módulo coda_processo_geral.py
sys.path.append(r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports")
from coda_processo_geral import inserir_dados

# Caminho da pasta e nome do arquivo específico
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket"
arquivo_especifico = "CSV Amélia.csv"

# Mapeamento de buckets: prod e dev
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Entradas e desfechos"
frequencia = "Diário"

# Inicializa cliente do Storage
cliente = storage.Client()

# Define política de retry e timeout
retry_policy = Retry(deadline=300)
upload_timeout = 300

# Caminho completo do arquivo
caminho_completo = os.path.join(pasta_arquivos, arquivo_especifico)

# Verifica se o arquivo existe
if os.path.isfile(caminho_completo):
    data_atual = datetime.now().strftime("%Y-%m-%d")
    hora_inicio = datetime.now().strftime("%H:%M:%S")
    erro_encontrado = False
    nome_processo = f"Upload de arquivo - {arquivo_especifico}"

    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            blob = bucket.blob(f"{subpasta_bucket}/{arquivo_especifico}")
            blob.upload_from_filename(
                caminho_completo,
                timeout=upload_timeout,
                retry=retry_policy
            )
            print(f"✔ '{arquivo_especifico}' enviado para '{ambiente}' → {nome_bucket}/{subpasta_bucket}/{arquivo_especifico}")
        except Exception as e:
            erro_encontrado = True
            print(f"❌ Erro em '{ambiente}' ao enviar '{arquivo_especifico}': {e}")

    hora_fim = datetime.now().strftime("%H:%M:%S")
    status = "Falha no processamento" if erro_encontrado else "Processamento Ok"

    try:
        inserir_dados(
            data_atual,
            nome_processo,
            hora_inicio,
            hora_fim,
            status,
            frequencia
        )
    except Exception as e:
        print(f"⚠ Erro ao registrar log do processo '{arquivo_especifico}': {e}")
else:
    print(f"❌ Arquivo '{arquivo_especifico}' não encontrado no caminho especificado.")

print("✅ Processo finalizado.")
