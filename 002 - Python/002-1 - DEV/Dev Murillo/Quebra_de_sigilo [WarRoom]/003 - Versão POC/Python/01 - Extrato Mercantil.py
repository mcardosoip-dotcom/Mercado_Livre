"""
================================================================================
01 - EXTRATO MERCHANTIL
================================================================================
Descrição: Prepara dados de extrato mercantil para não correspondentes e 
           movimentações financeiras
Objetivo: Popular tabelas finais para geração de extratos em CSV
Conexão: SBOX_LEGALES (BigQuery e Storage)
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

# Conexões mantidas da estrutura original
storage_client = connections["SBOX_LEGALES"].storage_client
bigquery_client = connections["SBOX_LEGALES"].bigquery_client

bucket_name = "meli-bi-data-tmp"
root_folder = f"LEGALES/{area}/QUEBRA_SIGILO_FINCH/"
destination_execution_file = root_folder + execution_date + "/"

# ============================================================================
# PROCESSAMENTO: NÃO CORRESPONDENTE
# ============================================================================
print('Processando não correspondentes para extrato...')

# MERGE para não correspondentes
merge_command = """
MERGE SBOX_LEGALES.CAD_TBL_QS_EXTRATO_NAO_CORRESPONDENTE_FINCH A
USING SBOX_LEGALES.STG_QS_NAO_CORRESPONDENTE_CAD_VF_FINCH B
ON A.DATAHORA_IMPORTACAO = B.DATAHORA_IMPORTACAO
WHEN MATCHED THEN DELETE;

INSERT INTO SBOX_LEGALES.CAD_TBL_QS_EXTRATO_NAO_CORRESPONDENTE_FINCH
SELECT  
    '<area>' AS VERTICAL,
    CAST(IDENTIFICACAO AS STRING) AS IDENTIFICACAO,
    CAST(DOC_NUMBER AS STRING) AS DOC_NUMBER,
    SISTEMA,
    CAST(DATAHORA_IMPORTACAO AS DATE) AS DATA_IMPORTACAO,
    DATAHORA_IMPORTACAO AS DATAHORA_IMPORTACAO
FROM SBOX_LEGALES.STG_QS_NAO_CORRESPONDENTE_CAD_VF_FINCH
WHERE EXTRATO = 'Sim';
""".replace('<area>', area)

bigquery_client.query(merge_command).result()
print('Não correspondentes processados.')

# ============================================================================
# PROCESSAMENTO: MOVIMENTAÇÕES
# ============================================================================
print('Processando movimentações para extrato...')

merge_command_mov = """
MERGE SBOX_LEGALES.CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH A
USING SBOX_LEGALES.STG_QS_TITULAR_CAD_VF_FINCH B
ON A.DATAHORA_IMPORTACAO = B.DATAHORA_IMPORTACAO
WHEN MATCHED THEN DELETE;

INSERT INTO SBOX_LEGALES.CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH
SELECT DISTINCT
    '<area>' AS VERTICAL,
    CAST(TIT.IDENTIFICACAO AS STRING) AS IDENTIFICACAO,
    CASE 
         WHEN MOV.CUS_CUST_ID IS NOT NULL THEN 'EXTRATO    ' 
         ELSE NULL
    END AS TIPO_MOVIMENTO,
    CAST(TIT.DOC_NUMBER AS STRING) AS DOC_INVESTIGADO,
    COALESCE(CAST(TIT.CONTA_SPB AS STRING), CAST(TIT.CUS_CUST_ID AS STRING)) AS ID_INVESTIGADO,
    MOV.DATA_LANCAMENTO,
    CAST(MOV.ID_PAGAMENTO AS STRING) AS ID_PAGAMENTO,
    MOV.MOV_TYPE_ID,
    MOV.MOV_DETAIL,
    CASE 
         WHEN MOV.CUS_CUST_ID IS NOT NULL THEN 'available'
         ELSE NULL
    END AS MOV_STATUS_ID,
    CASE 
         WHEN NATUREZA_LANCAMENTO = 'D' THEN
              (CASE 
                    WHEN LENGTH(VALOR_LANCAMENTO) IS NULL THEN NULL
                    WHEN LENGTH(VALOR_LANCAMENTO) = 1 THEN CONCAT('-0,0', VALOR_LANCAMENTO)
                    WHEN LENGTH(VALOR_LANCAMENTO) = 2 THEN CONCAT('-0,', VALOR_LANCAMENTO)
                    ELSE CONCAT('-', LEFT(VALOR_LANCAMENTO, LENGTH(VALOR_LANCAMENTO)-2), ',', RIGHT(VALOR_LANCAMENTO, 2))
               END)
         WHEN NATUREZA_LANCAMENTO = 'C' THEN
              (CASE 
                    WHEN LENGTH(VALOR_LANCAMENTO) IS NULL THEN NULL
                    WHEN LENGTH(VALOR_LANCAMENTO) = 1 THEN CONCAT('0,0', VALOR_LANCAMENTO)
                    WHEN LENGTH(VALOR_LANCAMENTO) = 2 THEN CONCAT('0,', VALOR_LANCAMENTO)
                    ELSE CONCAT(LEFT(VALOR_LANCAMENTO, LENGTH(VALOR_LANCAMENTO)-2), ',', RIGHT(VALOR_LANCAMENTO, 2))
               END)
    END AS VALOR_LANCAMENTO,
    '0' AS MOV_BALANCED_AMOUNT,
    DATAHORA_IMPORTACAO AS DATAHORA_IMPORTACAO
FROM SBOX_LEGALES.STG_QS_TITULAR_CAD_VF_FINCH TIT  
LEFT JOIN SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH MOV  
    ON CAST(TIT.CUS_CUST_ID AS STRING) = CAST(MOV.CUS_CUST_ID AS STRING)
WHERE TIT.EXTRATO = 'Sim';
""".replace('<area>', area)

bigquery_client.query(merge_command_mov).result()
print('Movimentações processadas.')

print('Processo de extrato mercantil concluído.')
