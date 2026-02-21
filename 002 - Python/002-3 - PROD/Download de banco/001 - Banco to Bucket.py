import os
import pandas as pd
import io
from google.api_core.retry import Retry
from datetime import date

# === Parâmetros fixos ===
project = "<ENV>"  # Certifique-se de preencher este valor
bucket_name = "<Bucket>" # Certifique-se de preencher este valor
tabelas = [
    "STG.LK_PBD_LA_BASE_BASE_ATIVA",
    "STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS"
]

# === Conexões via contexto MELI ===
# As conexões 'connections' são específicas do ambiente onde este script é executado (provavelmente MELI).
# Garanta que elas estejam configuradas corretamente no seu ambiente.
storage_client = connections["BigQuery_Default_DME"].storage_client
bigquery_client = connections["BigQuery_Default_DME"].bigquery_client

# ---
# === Loop pelas tabelas ===
for tabela in tabelas:
    nome_tabela = tabela.split('.')[-1]
    dataset_table = f"{project}.{tabela}"
    file_name_base = nome_tabela
    parquet_path = f"Projeto banco de dados/Exports_csvs/{file_name_base}.parquet"
    csv_path = f"Projeto banco de dados/Exports_csvs/{file_name_base}.csv"

    print(f"🔄 Iniciando extração da tabela: {dataset_table}")
    query = f"SELECT * FROM `{dataset_table}`"
    df = bigquery_client.query(query).to_dataframe()
    print(f"✅ {len(df)} linhas extraídas.")

    # ---
    # === Upload Parquet ===
    print(f"☁ Upload (Parquet) para gs://{bucket_name}/{parquet_path}")
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    blob_parquet = storage_client.bucket(bucket_name).blob(parquet_path)
    blob_parquet.upload_from_file(parquet_buffer, content_type='application/octet-stream')

    # ---
    # === Upload CSV ===
    # AQUI ESTÁ A MUDANÇA: adicionado sep='|' para usar o pipe como separador
    print(f"☁ Upload (CSV) para gs://{bucket_name}/{csv_path}")
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep='|') # <-- MUDANÇA AQUI
    csv_buffer.seek(0)
    blob_csv = storage_client.bucket(bucket_name).blob(csv_path)
    blob_csv.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    print(f"✅ Tabela {nome_tabela} exportada com sucesso.\n")