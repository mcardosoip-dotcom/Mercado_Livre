# ================================================
# Descrição :  Este processo captura os arquivos Parquet 
#              e transfere eles para o Bucket Meli na pasta eLAW_Databases
#              com nomes tratados (sem acentos/caracteres especiais)
# Autor : Marcelo Cardoso
# ================================================

import os
import re
import unicodedata
from datetime import datetime
from google.cloud import storage
from google.api_core.retry import Retry

# Caminho real da pasta de onde vêm os arquivos
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-03 - Quebra de Sigilo"

# Mapeamento de buckets: prod e dev
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Projeto banco de dados/Quebra_Sigilo"

# Inicializa cliente do Storage
cliente = storage.Client()

# Define política de retry e timeout
retry_policy = Retry(deadline=300)
upload_timeout = 900  # segundos

# Função para limpar nomes de arquivos
def limpar_nome_arquivo(nome, nomes_existentes):
    nome_sem_ext = os.path.splitext(nome)[0]
    ext = os.path.splitext(nome)[1]

    nome_limpo = unicodedata.normalize('NFKD', nome_sem_ext)
    nome_limpo = ''.join(c for c in nome_limpo if not unicodedata.combining(c))
    nome_limpo = re.sub(r'\W', '_', nome_limpo)
    nome_limpo = re.sub(r'_+', '_', nome_limpo).strip('_')

    nome_final = nome_limpo
    contador = 2
    while f"{nome_final}{ext}" in nomes_existentes:
        nome_final = f"{nome_limpo}_{contador}"
        contador += 1

    return f"{nome_final}{ext}"

# Armazena resultados para exibição final
resumo_uploads = []
nomes_gerados = set()

# Itera sobre arquivos na pasta
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
    if not os.path.isfile(caminho_completo):
        continue

    # 🔒 Garante que só arquivos .parquet sejam processados
    if not nome_arquivo.lower().endswith(".parquet"):
        continue

    nome_ajustado = limpar_nome_arquivo(nome_arquivo, nomes_gerados)
    nomes_gerados.add(nome_ajustado)

    resultado = {"arquivo": nome_arquivo, "nome_tratado": nome_ajustado, "status": {}}

    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            blob = bucket.blob(f"{subpasta_bucket}/{nome_ajustado}")
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
print(f"Total de arquivos processados: {len(resumo_uploads)}\n")

for r in resumo_uploads:
    print(f"📁 Original: {r['arquivo']}")
    print(f"   Tratado : {r['nome_tratado']}")
    for ambiente, status in r["status"].items():
        print(f"   [{ambiente.upper()}] {status}")
    print()

print("✅ Processo concluído.\n")
