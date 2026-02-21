"""
================================================================================
02 - CARTA CIRCULAR 3454 - CONTAS
================================================================================
Descrição: Gera arquivos de contas para Carta Circular 3454
Objetivo: Exportar dados de contas em formato TXT (separado por tabulação)
Conexão: SBOX_LEGALES (BigQuery e Storage)
Saída: CONTAS.txt (geral) e {IDENTIFICACAO}_CONTAS.txt (por investigado)
================================================================================
"""

import os
from datetime import date
from google.cloud import storage, bigquery
import pandas as pd
import numpy as np

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
account_file = destination_execution_file + "CONTAS.txt"
circular_letter_3454_directory = destination_execution_file + "carta_circular_3454/"

# ============================================================================
# OBTER DADOS
# ============================================================================
print('Obtendo dados de contas...')
table_name = "meli-bi-data.SBOX_LEGALES.TBL_QS_CONTAS_FINCH"
command = """SELECT 
    TRIM(IDENTIFICACAO) as IDENTIFICACAO, 
    NUMERO_BANCO, 
    NUMERO_AGENCIA, 
    NUMERO_CONTA, 
    TIPO_CONTA, 
    DATA_ABERTURA_CONTA, 
    DATA_ENCERRAMENTO_CONTA, 
    MOVIMENTACAO_CONTA 
FROM `{}` 
WHERE DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) 
    FROM SBOX_LEGALES.STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH
);""".format(table_name)

query_job = bigquery_client.query(command)
df = query_job.to_dataframe()
print(f'Total de registros: {len(df)}')

# ============================================================================
# SALVAR ARQUIVO GERAL
# ============================================================================
print('Salvando arquivo geral CONTAS.txt...')
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(account_file)
blob.upload_from_string(df.to_csv(index=0, mode='w'), 'text/plain')

# ============================================================================
# GERAR ARQUIVOS POR INVESTIGADO
# ============================================================================
print('Gerando arquivos por investigado...')
ids = df['IDENTIFICACAO'].unique()

for id in ids:
    print(f'Processando: {id}')
    id_sanitized = id.replace('/', '-').replace('\\', '-')
    filtered_data = df.loc[df['IDENTIFICACAO'] == id].copy()

    # Tratamento de dados
    filtered_data = filtered_data.astype(str).replace('nan', '').replace('None', '')

    # Remover acentos e converter para maiúsculas
    cols = filtered_data.select_dtypes(include=[object]).columns
    filtered_data[cols] = filtered_data[cols].apply(
        lambda x: x.astype(str)
                     .str.normalize('NFKD')
                     .str.encode('ascii', errors='ignore')
                     .str.decode('utf-8')
                     .str.upper()
    ).fillna('')
    
    # Validar registros vazios
    filtered_data = filtered_data.replace(r'^\s*$', np.nan, regex=True)
    if len(filtered_data) > 0:
        filtered_data = filtered_data.drop(columns=['IDENTIFICACAO'])
        filtered_data = filtered_data.replace(np.nan, '')

        # Gerar arquivo por ID
        id_directory = circular_letter_3454_directory + id_sanitized + "/"
        id_filename = id_directory + id_sanitized + "_CONTAS.txt"
        blob = bucket.blob(id_filename)
        blob.upload_from_string(
            filtered_data.to_csv(sep='\t', header=False, index=0, mode='w'), 
            'text/plain'
        )

print('Processo de geração de contas concluído.')
