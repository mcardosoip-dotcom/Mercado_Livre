"""
Step 6 – Processo CLM por FTP: envia os Parquets (gerados no step 5) para o bucket GCS.
Lê de 001-99 - Outras Fontes/CLM_DocuSign e faz upload para prod e dev.
Baseado em CLM_DocuSign/002 - Carga em Bucket.py
"""
import os
from google.cloud import storage
from google.api_core.retry import Retry

# Pasta de origem dos Parquets (saída do step 5)
PASTA_ARQUIVOS = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\CLM_DocuSign"

BUCKETS = {"prod": "pdme000426", "dev": "ddme000426"}
SUBPASTA_BUCKET = "Projeto banco de dados/Diversas"

PROJETO_ID = "ddme000426-gopr4nla6zo-furyid"
cliente = storage.Client(project=PROJETO_ID)
retry_policy = Retry(deadline=300)
upload_timeout = 300


def main():
    resumo_uploads = []
    if not os.path.isdir(PASTA_ARQUIVOS):
        print(f"Erro: Pasta nao encontrada: {PASTA_ARQUIVOS}")
        return 1

    for nome_arquivo in os.listdir(PASTA_ARQUIVOS):
        caminho_completo = os.path.join(PASTA_ARQUIVOS, nome_arquivo)
        if not os.path.isfile(caminho_completo) or not nome_arquivo.lower().endswith(".parquet"):
            continue

        resultado = {"arquivo": nome_arquivo, "status": {}}
        for ambiente, nome_bucket in BUCKETS.items():
            try:
                bucket = cliente.bucket(nome_bucket)
                blob_destination = f"{SUBPASTA_BUCKET}/{nome_arquivo}"
                blob = bucket.blob(blob_destination)
                print(f"  Upload {nome_arquivo} -> [{ambiente.upper()}]...")
                blob.upload_from_filename(
                    caminho_completo,
                    timeout=upload_timeout,
                    retry=retry_policy,
                )
                resultado["status"][ambiente] = "Sucesso"
            except Exception as e:
                resultado["status"][ambiente] = f"Erro: {e}"
        resumo_uploads.append(resultado)

    print("\nResumo do upload GCS:")
    print(f"Total de arquivos Parquet: {len(resumo_uploads)}\n")
    for r in resumo_uploads:
        print(f"  {r['arquivo']}")
        for ambiente, status in r["status"].items():
            print(f"    [{ambiente.upper()}] {status}")
    print("\nStep 6 concluido.")
    return 0


if __name__ == "__main__":
    exit(main())
