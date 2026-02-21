"""
================================================================================
10 - EXTRATO FINANCEIRO CSV
================================================================================
Descrição: Gera arquivos CSV de extrato financeiro e rendimento
Objetivo: Exportar extratos em formato CSV para cada investigado
Conexão: SBOX_LEGALES (BigQuery e Storage)
Saída: PROTOCOLOS_CCS_So_ExtratoMercantil_{ID}_{DOC}_{CUS}.csv
       PROTOCOLOS_CCS_So_ExtratoMercantil_{ID}_{DOC}_{CUS}_rendimento.csv
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
print('Iniciando o processo de extrato financeiro CSV...')

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
financial_statement_directory = destination_execution_file + "extrato_financeiro/"

# ============================================================================
# OBTER DADOS
# ============================================================================
print('Obtendo dados da base...')
table_name = "meli-bi-data.SBOX_LEGALES.CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH"
command = """SELECT 
    TRIM(IDENTIFICACAO) as IDENTIFICACAO, 
    TIPO_MOVIMENTO,
    DOC_INVESTIGADO,
    CUS_CUST_ID,
    CASE 
        WHEN MOV_CREATED_DT IS NULL Then ''
        ELSE CAST(MOV_CREATED_DT as STRING) 
    END as MOV_CREATED_DT,
    ID_PAGAMENTO,
    MOV_TYPE_ID, 
    MOV_DETAIL, 
    MOV_STATUS_ID,
    CASE
        WHEN TIPO_MOVIMENTO = '' AND MOV_AMOUNT = '0,00' THEN ''
        ELSE CAST(MOV_AMOUNT as STRING)
    END as MOV_AMOUNT, 
    CASE
        WHEN TIPO_MOVIMENTO = '' AND MOV_BALANCED_AMOUNT = '0,00' THEN ''
        ELSE CAST(MOV_BALANCED_AMOUNT as STRING)
    END as MOV_BALANCED_AMOUNT
FROM `{}` 
WHERE DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) 
    FROM SBOX_LEGALES.STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH
);""".format(table_name)

query_job = bigquery_client.query(command)
df = query_job.to_dataframe()
print(f'Total de registros: {len(df)}')

# ============================================================================
# TRATAR DADOS
# ============================================================================
print('Tratando a base...')
bucket = storage_client.bucket(bucket_name)
data = df.astype(str).replace('nan', '').replace('None', '')

print('Removendo acentos e convertendo para maiúsculas...')
cols = data.select_dtypes(include=[object]).columns
data[cols] = data[cols].apply(
    lambda x: x.astype(str)
                 .str.normalize('NFKD')
                 .str.encode('ascii', errors='ignore')
                 .str.decode('utf-8')
                 .str.upper()
).fillna('')

print('Validando registros vazios...')
data = data.replace(r'^\s*$', np.nan, regex=True)
if len(data) > 0:
    data = data.replace(np.nan, '')

# ============================================================================
# GERAR ARQUIVOS CSV POR INVESTIGADO
# ============================================================================
print('Gerando arquivos CSV...')
# Obter ids únicos com base em IDENTIFICACAO, DOC_INVESTIGADO e CUS_CUST_ID
ids = data.drop_duplicates(subset=['IDENTIFICACAO', 'DOC_INVESTIGADO', 'CUS_CUST_ID']).to_numpy()
print(f"Total de ids: {len(ids)}")

for id in ids:
    print(f'Executando o processo: {id[0]}')
    filtro = "%s == '%s' & %s == '%s' & %s == '%s'" % (
        'IDENTIFICACAO', id[0], 
        'DOC_INVESTIGADO', id[2], 
        'CUS_CUST_ID', id[3]
    )
    filtered_data = data.query(filtro)
    
    if not filtered_data.empty:
        # Nomes dos arquivos
        filename = f"PROTOCOLOS_CCS_So_ExtratoMercantil_{id[0]}_{id[2]}_{id[3]}.csv"
        file_rendimento = filename.replace(".csv", "_rendimento.csv")
        id_directory = financial_statement_directory + filename
        
        filtered_data["TIPO_MOVIMENTO"] = filtered_data["TIPO_MOVIMENTO"].str.strip()
        
        # Filtrar extrato
        filtro_extrato = "%s == '%s'" % ('TIPO_MOVIMENTO', 'EXTRATO')
        filtered_extract = filtered_data.query(filtro_extrato)

        # Filtrar rendimento
        filtro_rendimento = "%s != '%s' and %s != '%s'" % (
            'TIPO_MOVIMENTO', 'EXTRATO', 
            'TIPO_MOVIMENTO', ''
        )
        filtered_income = filtered_data.query(filtro_rendimento)
        
        print('Criando arquivos CSV...')
        
        # Salvar extrato em CSV
        if not filtered_extract.empty:
            filtered_extract_clean = filtered_extract.drop(
                columns=['IDENTIFICACAO', 'TIPO_MOVIMENTO', 'DOC_INVESTIGADO']
            )
            filtered_extract_clean.to_csv(filename, index=False, sep=',')
            
            # Upload do arquivo de extrato
            blob = bucket.blob(id_directory)
            blob.upload_from_filename(filename)
            os.remove(filename)  # Limpar arquivo temporário
        
        # Salvar rendimento em outro CSV
        if not filtered_income.empty:
            filtered_income_clean = filtered_income.drop(
                columns=['IDENTIFICACAO', 'TIPO_MOVIMENTO', 'DOC_INVESTIGADO']
            )
            filtered_income_clean.to_csv(file_rendimento, index=False, sep=',')
            
            # Upload do arquivo de rendimento
            blob_income = bucket.blob(id_directory.replace(".csv", "_rendimento.csv"))
            blob_income.upload_from_filename(file_rendimento)
            os.remove(file_rendimento)  # Limpar arquivo temporário

print('Processo de extrato financeiro CSV concluído.')
