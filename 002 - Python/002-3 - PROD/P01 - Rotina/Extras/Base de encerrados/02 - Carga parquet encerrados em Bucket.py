# ================================================
# Descrição :  Envia o parquet consolidado (Base encerrados eLAW)
#              para o Bucket na pasta Base_de_encerrados (eLAW_Databases).
#              Executar após o script 01 - Consolidar encerrados eLAW.py
# Autor : Marcelo Cardoso
# ================================================

import os
from google.cloud import storage
from google.api_core.retry import Retry

# Parquet gerado pelo script de consolidação
pasta_parquet = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Extras\Histórico Contencioso\Consolidado"
nome_arquivo_parquet = "Base_Consolidada_Encerrados_eLAW.parquet"
caminho_parquet = os.path.join(pasta_parquet, nome_arquivo_parquet)

# Bucket: mesmo padrão do eLAW (prod e dev)
buckets = {"prod": "pdme000426", "dev": "ddme000426"}
# Destino no bucket: subpasta Base de encerrados (nome limpo para path)
subpasta_bucket = "Projeto banco de dados/eLAW_Databases/Base_de_encerrados"

projeto_id = "ddme000426-gopr4nla6zo-furyid"
cliente = storage.Client(project=projeto_id)
retry_policy = Retry(deadline=300)
upload_timeout = 300

if __name__ == "__main__":
    if not os.path.isfile(caminho_parquet):
        print(f"Arquivo não encontrado: {caminho_parquet}")
        print("Execute antes o script: 01 - Consolidar encerrados eLAW.py")
        raise SystemExit(1)

    print(f"Enviando parquet para o bucket (pasta Base de encerrados): {nome_arquivo_parquet}\n")

    resumo = []
    for ambiente, nome_bucket in buckets.items():
        try:
            bucket = cliente.bucket(nome_bucket)
            blob = bucket.blob(f"{subpasta_bucket}/{nome_arquivo_parquet}")
            blob.upload_from_filename(
                caminho_parquet,
                timeout=upload_timeout,
                retry=retry_policy,
            )
            resumo.append((ambiente, "Sucesso"))
        except Exception as e:
            resumo.append((ambiente, f"Erro: {e}"))

    for ambiente, status in resumo:
        print(f"  [{ambiente.upper()}] {status}")
    print("\nProcesso de carga no bucket concluído.")
