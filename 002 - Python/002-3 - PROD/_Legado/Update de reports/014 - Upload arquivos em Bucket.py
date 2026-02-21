# ================================================
# Descrição :  Este processo faz a carga dos arquivos no ambiente do Mercado Livre 
#              através de uma conexão Google com autenticação de usuário
# Autor : Marcelo Cardoso
# ================================================

import os
from datetime import datetime
from google.cloud import storage
from google.api_core.retry import Retry
from coda_processo_geral import inserir_dados

# Caminho real da pasta de onde vêm os arquivos
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket"

# Mapeamento de buckets: prod e dev
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Entradas e desfechos"
frequencia = "Diário"

# Inicializa cliente do Storage
cliente = storage.Client()

# Define política de retry e timeout
retry_policy = Retry(deadline=300)  # até 5 minutos de tentativas
upload_timeout = 300  # segundos

# Itera sobre arquivos na pasta
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
    if not os.path.isfile(caminho_completo):
        continue

    data_atual = datetime.now().strftime("%Y-%m-%d")
    hora_inicio = datetime.now().strftime("%H:%M:%S")
    erro_encontrado = False
    nome_processo = f"Upload de arquivo - {nome_arquivo}"

    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            blob = bucket.blob(f"{subpasta_bucket}/{nome_arquivo}")
            blob.upload_from_filename(
                caminho_completo,
                timeout=upload_timeout,
                retry=retry_policy
            )
            print(f"✔ '{nome_arquivo}' enviado para '{ambiente}' → {nome_bucket}/{subpasta_bucket}/{nome_arquivo}")
        except Exception as e:
            erro_encontrado = True
            print(f"❌ Erro em '{ambiente}' ao enviar '{nome_arquivo}': {e}")

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
        print(f"⚠ Erro ao registrar log do processo '{nome_arquivo}': {e}")

print("✅ Upload finalizado em ambos os ambientes.")
