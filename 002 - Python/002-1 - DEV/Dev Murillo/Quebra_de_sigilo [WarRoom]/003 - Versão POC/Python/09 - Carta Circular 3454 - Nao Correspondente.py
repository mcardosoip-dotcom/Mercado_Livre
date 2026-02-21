"""
================================================================================
09 - CARTA CIRCULAR 3454 - NÃO CORRESPONDENTE
================================================================================
Descrição: Gera arquivo de não correspondentes para Carta Circular 3454
Objetivo: Exportar investigados que não possuem conta no sistema
Conexão: SBOX_LEGALES (BigQuery e Storage)
Saída: NAO_CORRESPONDENTE.txt
================================================================================
"""

import os
from datetime import date
from google.cloud import storage, bigquery
import pandas as pd

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
area = os.environ.get("area")
processing_date_string = date.today().strftime('%Y-%m-%d')
execution_date = os.environ.get("DF_TIME_TO").replace("-", "").replace(":", "").replace(" ", "")
project = 'meli-bi-data'

# Conexões mantidas
storage_client = connections["SBOX_LEGALES"].storage_client
bigquery_client = connections["SBOX_LEGALES"].bigquery_client

bucket_name = "meli-bi-data-tmp"
root_folder = f"LEGALES/{area}/QUEBRA_SIGILO_FINCH/"
destination_execution_file = root_folder + execution_date + "/"
account_file = destination_execution_file + "NAO_CORRESPONDENTE.txt"

# ============================================================================
# OBTER DADOS
# ============================================================================
print('Obtendo dados de não correspondentes...')
table_name = "meli-bi-data.SBOX_LEGALES.TBL_QS_NAO_CORRESPONDENTE_FINCH"
command = """SELECT *
FROM `{}` T 
WHERE T.DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) 
    FROM SBOX_LEGALES.STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH
);""".format(table_name)

query_job = bigquery_client.query(command)
df = query_job.to_dataframe()
print(f'Total de registros: {len(df)}')

# ============================================================================
# SALVAR ARQUIVO
# ============================================================================
print('Salvando arquivo NAO_CORRESPONDENTE.txt...')
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(account_file)
blob.upload_from_string(df.to_csv(index=0, mode='w'), 'text/plain')

print('Processo de geração de não correspondentes concluído.')
