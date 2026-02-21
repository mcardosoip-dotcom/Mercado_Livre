# ================================================
# BLOCO 2: UPLOAD PARA O BUCKET GCS
# Objetivo: Captura os arquivos Parquet da pasta TARGET_DIR e
#           transfere para o Bucket Meli na pasta eLAW_Databases.
# ================================================

import os
# import unicodedata # Não é mais necessário, já que a limpeza de nome foi removida
from google.cloud import storage
from google.api_core.retry import Retry
# Adicionando 'time' e 'datetime' por consistência com o bloco de configuração desejado
import time 
from datetime import datetime

# Caminho de origem dos arquivos Parquet (o destino do Bloco 1)
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\CLM_DocuSign"

# Mapeamento de buckets: prod e dev (mantido do seu código de referência)
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Projeto banco de dados/Diversas"

# ⭐ CORREÇÃO APLICADA AQUI: Passando o project ID explicitamente
projeto_id = "ddme000426-gopr4nla6zo-furyid"
cliente = storage.Client(project=projeto_id) 
# ⭐ FIM DA CORREÇÃO

# Define política de retry e timeout
retry_policy = Retry(deadline=300)
# Ajustando o upload_timeout para o valor do código de conexão (300 segundos)
upload_timeout = 300 

# Armazena resultados para exibição final
resumo_uploads = []

# Itera sobre arquivos na pasta (procurando pelos Parquets)
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
    
    # Processa apenas arquivos Parquet
    if not os.path.isfile(caminho_completo) or not nome_arquivo.lower().endswith('.parquet'):
        continue

    # Como o Bloco 1 já limpou e padronizou o nome,
    # o nome de destino no GCS é o próprio nome do arquivo.
    nome_ajustado = nome_arquivo 
    
    resultado = {"arquivo": nome_arquivo, "status": {}}

    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            # O blob é a subpasta + o nome do arquivo limpo (e.g., CLM_control_de_contratos.parquet)
            blob_destination = f"{subpasta_bucket}/{nome_ajustado}"
            blob = bucket.blob(blob_destination)
            
            print(f"  Fazendo upload de {nome_arquivo} para [{ambiente.upper()}]...")
            
            blob.upload_from_filename(
                caminho_completo,
                timeout=upload_timeout,
                retry=retry_policy
            )
            resultado["status"][ambiente] = "✔ Sucesso"
        except Exception as e:
            resultado["status"][ambiente] = f"❌ Erro: {e}"

    resumo_uploads.append(resultado)

# Output final
print("\n📊 Resumo do Upload GCS:\n")
print(f"Total de arquivos Parquet enviados: {len(resumo_uploads)}\n")

for r in resumo_uploads:
    print(f"📁 Arquivo: {r['arquivo']}")
    for ambiente, status in r["status"].items():
        print(f"   [{ambiente.upper()}] {status}")
    print()

print("✅ Processo de Upload concluído.\n")