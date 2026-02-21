import os
from google.cloud import storage
from google.api_core.retry import Retry
import time
from datetime import datetime

# --- CONFIGURAÇÕES NECESSÁRIAS PARA O UPLOAD ---

# NOVO CAMINHO PARA MAC/GOOGLE DRIVE
pasta_temporaria = "/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics/002 - Python/002-3 - PROD/P01 - Rotina/MAIN/CARGA DE TABELAS/Mesa de entrada/Buffer"
os.makedirs(pasta_temporaria, exist_ok=True) 

# Configurações do Google Cloud Storage
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Mesa_de_entrada"

# ⭐ CORREÇÃO APLICADA AQUI: Passando o project ID explicitamente
projeto_id = "ddme000426-gopr4nla6zo-furyid"
cliente = storage.Client(project=projeto_id) 
# ⭐ FIM DA CORREÇÃO

retry_policy = Retry(deadline=300)
upload_timeout = 300
status_final = "Processamento Ok" # Variável para rastrear o status

# Lista de arquivos que devem ser carregados
arquivos_para_upload = [
    "Mesa_entrada_vista_entradas.parquet",
    "Mesa_entrada_dw_hist_casos_x_estado.parquet",
    "Mesa_entrada_tab_entradas.parquet",
    "Mesa_entrada_vista_cantidad_casos_usuarios.parquet",
    "Mesa_entrada_vista_usuarios.parquet",
    "Mesa_entrada_v_metricas_qa.parquet",
    "Mesa_entrada_estados.parquet",
    "Mesa_entrada_tipo_documentos.parquet",
    "Mesa_entrada_metricas_big_query.parquet",
    "Mesa_entrada_origenes.parquet",
    "Mesa_entrada_entradas_estados.parquet"
]


# --- FUNÇÃO DE CARGA (UPLOAD) PARA O BUCKET ---
def jogar_no_bucket(arquivos_gerados, buckets, subpasta_bucket, cliente, pasta_temporaria, upload_timeout, retry_policy):
    """
    Realiza o upload dos arquivos Parquet da pasta temporária para os buckets de PROD e DEV no GCS.
    """
    global status_final
    print("\n" + "="*50)
    print(f"Iniciando Upload de {len(arquivos_gerados)} arquivos para o Google Cloud Storage...")
    print("="*50)

    for nome_arquivo in arquivos_gerados:
        caminho_parquet = os.path.join(pasta_temporaria, nome_arquivo)

        if not os.path.exists(caminho_parquet):
            print(f"❌ Erro: Arquivo local não encontrado para o upload: {caminho_parquet}")
            status_final = "Falha no processamento"
            continue
        
        print(f"\n→ Tentando upload do arquivo: {nome_arquivo}")

        for ambiente, nome_bucket in buckets.items():
            try:
                bucket = cliente.bucket(nome_bucket)
                blob = bucket.blob(f"{subpasta_bucket}/{nome_arquivo}")

                blob.upload_from_filename(
                    caminho_parquet, 
                    timeout=upload_timeout, 
                    retry=retry_policy
                )
                print(f"  ✔ Upload [AMBIENTE: {ambiente}] → gs://{nome_bucket}/{subpasta_bucket}/{nome_arquivo}")

            except Exception as e:
                print(f"  ❌ Falha no upload [AMBIENTE: {ambiente}]: {e}")
                status_final = "Falha no processamento"


# --- EXECUÇÃO PRINCIPAL DO UPLOAD ---
if __name__ == "__main__":
    if arquivos_para_upload:
        jogar_no_bucket(
            arquivos_para_upload, 
            buckets, 
            subpasta_bucket, 
            cliente, 
            pasta_temporaria,
            upload_timeout,
            retry_policy
        )
    else:
        print("⚠️ Nenhuma base de dados foi especificada para fazer o upload.")

    print("\n" + "="*50)
    print(f"Status Final do Processo de Upload: {status_final}")
    print("="*50)