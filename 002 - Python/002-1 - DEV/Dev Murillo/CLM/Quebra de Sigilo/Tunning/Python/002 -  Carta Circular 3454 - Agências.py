import base64
import json
import os
from datetime import date
from google.oauth2 import service_account
from google.cloud import storage, bigquery
import pandas as pd
import numpy as np

area = os.environ.get("area")
processing_date_string = date.today().strftime('%Y-%m-%d')
execution_date = os.environ.get("DF_TIME_TO").replace("-", "").replace(":", "").replace(" ", "")
project='meli-bi-data'

storage_client = connections["BigQuery_Default_DME"].storage_client
bigquery_client = connections["BigQuery_Default_DME"].bigquery_client

bucket_name = "ddme000426"
root_folder = f"LEGALES/{area}/QUEBRA_SIGILO_TUNING/"
destination_execution_file = root_folder + execution_date + "/"
account_file = destination_execution_file + "AGENCIAS.txt"
circular_letter_3454_directory = destination_execution_file + "carta_circular_3454/"
financial_statement_directory = destination_execution_file + "extrato_financeiro/"

table_name = "ddme000426-gopr4nla6zo-furyid.STG.TBL_QS_AGENCIAS_TUNING"
source_import_table = "ddme000426-gopr4nla6zo-furyid.STG.STG_QS_PLANILHA_PRESENTA_CAD_VF_TUNING" 

command = """SELECT
              TRIM(IDENTIFICACAO) as IDENTIFICACAO,
              NUMERO_BANCO,
              NUMERO_AGENCIA,
              NOME_AGENCIA,
              ENDERECO_LOGRADOURO,
              ENDERECO_CIDADE,
              ENDERECO_UF,
              ENDERECO_PAIS,
              ENDERECO_CEP,
              TELEFONE_AGENCIA,
              DATA_ABERTURA_AGENCIA,
              DATA_FECHAMENTO_AGENCIA
              FROM `{}` WHERE DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) FROM `{}`
);""".format(table_name, source_import_table)
query_job = bigquery_client.query(command)
df = query_job.to_dataframe()

bucket = storage_client.bucket(bucket_name)
#blob = bucket.blob(account_file)
#blob.upload_from_string(df.to_csv(index=0, mode='w'), 'text/plain')

ids = df['IDENTIFICACAO'].unique()
for id_val in ids:
    print(f'Executando o processo: {id_val}')
    id_sanitized = str(id_val).replace('/', '-').replace('\\', '-')
    filtered_data = df.loc[df['IDENTIFICACAO'] == id_val]

    filtered_data = filtered_data.astype(str).replace('nan', '').replace('None', '')

    cols = filtered_data.select_dtypes(include=[object]).columns
    filtered_data[cols] = filtered_data[cols].apply(lambda x: x.astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper()).fillna('')
    
    filtered_data = filtered_data.replace(r'^\s*$', np.nan, regex=True)
    if(len(filtered_data) > 0):
        filtered_data = filtered_data.drop(columns=['IDENTIFICACAO'])
        filtered_data = filtered_data.replace(np.nan, '')

    id_directory = circular_letter_3454_directory + id_sanitized
    id_filename = id_directory + '/' + id_sanitized + "_AGENCIAS.txt"
    blob = bucket.blob(id_filename)
    blob.upload_from_string(filtered_data.to_csv(sep='\t', header=False, index=0, mode='w'), 'text/plain')