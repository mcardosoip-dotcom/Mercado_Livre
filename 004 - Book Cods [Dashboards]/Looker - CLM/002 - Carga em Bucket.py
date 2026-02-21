# ================================================
# Descrição : Este processo captura os arquivos Parquet
#             e transfere eles para o Bucket Meli na pasta Salesforce_Databases
# Autor : Marcelo Cardoso
# ================================================

import os
from datetime import datetime
from google.cloud import storage
from google.api_core.retry import Retry

# Caminho real da pasta de onde vêm os arquivos
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - CLM\Databases"

# Mapeamento de buckets: prod e dev
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Projeto banco de dados/Diversas"

# Inicializa cliente do Storage
cliente = storage.Client()

# Define política de retry e timeout
retry_policy = Retry(deadline=300)
upload_timeout = 900  # segundos

# Armazena resultados para exibição final
resumo_uploads = []

# Itera sobre arquivos na pasta
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
    
    # Adiciona a verificação para garantir que apenas arquivos Parquet sejam processados
    if not os.path.isfile(caminho_completo) or not nome_arquivo.lower().endswith('.parquet'):
        continue # Pula para o próximo arquivo se não for um arquivo ou não for .parquet

    resultado = {"arquivo": nome_arquivo, "status": {}}

    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            blob = bucket.blob(f"{subpasta_bucket}/{nome_arquivo}")
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
print("\n📊 Resumo do Upload:\n")
print(f"Total de arquivos Parquet processados: {len(resumo_uploads)}\n")

for r in resumo_uploads:
    print(f"📁 {r['arquivo']}")
    for ambiente, status in r["status"].items():
        print(f"   [{ambiente.upper()}] {status}")
    print()

print("✅ Processo concluído.\n")