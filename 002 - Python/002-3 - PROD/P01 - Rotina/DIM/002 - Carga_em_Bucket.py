# ================================================
# Descrição :  Este processo captura os arquivos CSVs 
#              e transfere eles para o Bucket Meli na pasta eLAW_Databases
# Autor : Marcelo Cardoso
# ================================================

import os
from datetime import datetime
from google.cloud import storage
from google.api_core.retry import Retry

# ---------- CONFIGURAÇÃO DE ACESSO GCP ----------
# Opção 1: Deixe None para usar variável de ambiente GOOGLE_APPLICATION_CREDENTIALS
#          ou login do gcloud (gcloud auth application-default login)
# Opção 2: Caminho para o arquivo JSON da service account (ex.: "C:/credenciais/minha-sa.json")
CAMINHO_CREDENCIAIS_JSON = None  # ou r"C:\caminho\para\sua-service-account.json"

# Caminho real da pasta de onde vêm os arquivos
pasta_arquivos = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões"

# Mapeamento de buckets: prod e dev
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Projeto banco de dados/Dimensoes"

# ---------- Inicializa cliente do Storage ----------
try:
    if CAMINHO_CREDENCIAIS_JSON and os.path.isfile(CAMINHO_CREDENCIAIS_JSON):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CAMINHO_CREDENCIAIS_JSON
        print(f"Usando credenciais: {CAMINHO_CREDENCIAIS_JSON}")
    elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(f"Usando credenciais (env): {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
    else:
        print("Usando Application Default Credentials (gcloud auth application-default login)")
    cliente = storage.Client()
except Exception as e:
    print("\n❌ Erro ao conectar ao Google Cloud Storage:")
    print(f"   {e}")
    print("\n📌 Verifique:")
    print("   1. GOOGLE_APPLICATION_CREDENTIALS aponta para um JSON de service account, OU")
    print("   2. Execute: gcloud auth application-default login")
    print("   3. Veja CONFIG_GCP_BUCKET.md na pasta DIM para o passo a passo.\n")
    raise

# Testa acesso a um bucket (falha rápido se não tiver permissão)
try:
    primeiro_bucket = list(buckets.values())[0]
    cliente.get_bucket(primeiro_bucket)
except Exception as e:
    print(f"\n❌ Sem permissão no bucket '{primeiro_bucket}' ou bucket inexistente:")
    print(f"   {e}")
    print("\n📌 Confirme no console GCP que sua conta/service account tem papel")
    print("   'Storage Object Creator' ou 'Storage Admin' no bucket.\n")
    raise

# Define política de retry e timeout
retry_policy = Retry(deadline=300)
upload_timeout = 900  # segundos

# Armazena resultados para exibição final
resumo_uploads = []

# Itera sobre arquivos na pasta
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho_completo = os.path.join(pasta_arquivos, nome_arquivo)
    if not os.path.isfile(caminho_completo):
        continue

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
print(f"Total de arquivos processados: {len(resumo_uploads)}\n")

for r in resumo_uploads:
    print(f"📁 {r['arquivo']}")
    for ambiente, status in r["status"].items():
        print(f"   [{ambiente.upper()}] {status}")
    print()

print("✅ Processo concluído.\n")
