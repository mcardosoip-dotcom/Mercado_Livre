"""
================================================================================
06 - CARTA CIRCULAR 3454 - ENDEREÇO (Validação via API)
================================================================================
Descrição: Valida e completa endereços usando APIs de CEP
Objetivo: Preencher endereços faltantes e salvar em tabela validada
Conexão: SBOX_LEGALES (BigQuery e Storage)
Melhoria: Cache em PROJETO_ACRE_ADDRESSES para evitar consultas repetidas
================================================================================
"""

import os
from datetime import date
from google.cloud import storage, bigquery
import pandas as pd
import numpy as np
import requests as req

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

# ============================================================================
# OBTER DADOS E CACHE DE ENDEREÇOS
# ============================================================================
print('Obtendo dados de titulares...')
table_name = "meli-bi-data.SBOX_LEGALES.TBL_QS_TITULARES_FINCH"
command = """SELECT 
    TRIM(IDENTIFICACAO) as IDENTIFICACAO,
    NUMERO_BANCO,
    NUMERO_AGENCIA,
    NUMERO_CONTA,
    TIPO_CONTA,
    TIPO_TITULAR,
    PESSOA_INVESTIGADA,
    TIPO_PESSOA_TITULAR,
    CPF_CNPJ_TITULAR,
    UPPER(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(NOME_TITULAR,
        '[á,Á,à,À,ã,Ã,â,Â]','A'),'[É,é,ê,Ê]','E'),'[Í,í,Î,î]','I'), 
        '[Ó,ó,Õ,ö,Õ,õ]','O'),'[Ú,ú,û,Ü,ü]','U'), '[Ç,ç]','C'),
        '[^0-9a-zA-Z]+',' ')) AS NOME_TITULAR,
    NOME_DOC_IDENTIFICACAO,
    NUMERO_DOC_IDENTIFICACAO,
    B.street_name as ENDERECO_LOGRADOURO,
    B.city as ENDERECO_CIDADE,
    B.state as ENDERECO_UF,
    B.country as ENDERECO_PAIS,
    ENDERECO_CEP,
    TELEFONE_PESSOA,
    VALOR_RENDA,
    DATA_ATUALIZACAO_RENDA,
    DATA_INICIO_RELACIONAMENTO_CONTA,
    DATA_FIM_RELACIONAMENTO_CONTA,
    DATAHORA_IMPORTACAO
FROM `{}` A
LEFT JOIN `meli-bi-data.SBOX_LEGALES.PROJETO_ACRE_ADDRESSES` B 
    ON A.ENDERECO_CEP = B.zip_code
WHERE DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) 
    FROM SBOX_LEGALES.STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH
);""".format(table_name)

query_job = bigquery_client.query(command)
df = query_job.to_dataframe()

# Carregar cache de endereços
print('Carregando cache de endereços...')
table_name_cache = "meli-bi-data.SBOX_LEGALES.PROJETO_ACRE_ADDRESSES"
command_cache = """SELECT * FROM `{}`;""".format(table_name_cache)
query_job_cache = bigquery_client.query(command_cache)
df_address = query_job_cache.to_dataframe()

# ============================================================================
# VALIDAR ENDEREÇOS VIA API
# ============================================================================
print('Validando endereços via API...')
for row in df.itertuples(index=True, name='Pandas'):
    cep = row.ENDERECO_CEP.replace(".", "").replace("-", "").replace("None", "").strip() if row.ENDERECO_CEP != None else ''
    address = ''
    logradouro = ''
    cidade = ''
    uf = ''
    pais = ''
  
    # Se já tem endereço, pular
    if row.ENDERECO_LOGRADOURO != None and row.ENDERECO_LOGRADOURO != '':
        continue
  
    if len(cep) == 0:
        cep = '.'
    elif len(str(row.ENDERECO_CEP)) >= 8:
        cep = cep[0:8]
        df_address_filtered = df_address.loc[df_address['zip_code'] == cep]
        
        if df_address_filtered.empty:
            cep_encontrado = False
            # Tentar múltiplas APIs em cascata
            apis = [
                ('https://cep.awesomeapi.com.br/json/{}', lambda r: {
                    'logradouro': r.json().get('address', ''),
                    'cidade': r.json().get('city', ''),
                    'uf': r.json().get('state', ''),
                    'pais': 'BRA'
                }),
                ('http://correiosapi.apphb.com/cep/{}', lambda r: {
                    'logradouro': f"{r.json().get('tipodelogradouro', '')} {r.json().get('logradouro', '')}",
                    'cidade': r.json().get('cidade', ''),
                    'uf': r.json().get('estado', ''),
                    'pais': 'BRA'
                }),
                ('https://ws.apicep.com/cep/{}.json', lambda r: {
                    'logradouro': r.json().get('address', ''),
                    'cidade': r.json().get('city', ''),
                    'uf': r.json().get('state', ''),
                    'pais': 'BRA'
                }),
                ('https://viacep.com.br/ws/{}/json/', lambda r: {
                    'logradouro': r.json().get('logradouro', ''),
                    'cidade': r.json().get('localidade', ''),
                    'uf': r.json().get('uf', ''),
                    'pais': 'BRA'
                })
            ]
            
            for api_url, parser in apis:
                try:
                    resposta = req.get(api_url.format(cep), timeout=5)
                    if resposta.status_code == 200:
                        data = resposta.json()
                        if data.get('status') not in [400, 404] and 'erro' not in str(data).lower():
                            parsed = parser(resposta)
                            logradouro = parsed['logradouro']
                            cidade = parsed['cidade']
                            uf = parsed['uf']
                            pais = parsed['pais']
                            cep_encontrado = True
                            break
                except Exception:
                    continue
              
            # Salvar no cache se encontrado
            if cep_encontrado:
                insert_command = """
                INSERT INTO `meli-bi-data.SBOX_LEGALES.PROJETO_ACRE_ADDRESSES` 
                (zip_code, street_name, city, state, country, last_update_date) 
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                """.format(cep, logradouro, cidade, uf, pais, processing_date_string)
                try:
                    bigquery_client.query(insert_command).result()
                    # Atualizar cache local
                    new_data = pd.DataFrame([{
                        'zip_code': cep, 
                        'street_name': logradouro, 
                        'city': cidade, 
                        'state': uf, 
                        'country': pais, 
                        'last_update_date': processing_date_string
                    }])
                    df_address = pd.concat([df_address, new_data], ignore_index=True)
                except Exception as e:
                    print(f'Erro ao salvar CEP {cep}: {e}')
        else:
            # Usar dados do cache
            cep = df_address_filtered.zip_code.values[0]
            logradouro = df_address_filtered.street_name.values[0]
            cidade = df_address_filtered.city.values[0]
            uf = df_address_filtered.state.values[0]
            pais = df_address_filtered.country.values[0]

    # Atualizar DataFrame
    df.at[row.Index, 'ENDERECO_CEP'] = '.' if not cep or cep == '.' else cep
    df.at[row.Index, 'ENDERECO_LOGRADOURO'] = '.' if not logradouro else str(logradouro)[:79]
    df.at[row.Index, 'ENDERECO_CIDADE'] = '.' if not cidade else cidade
    df.at[row.Index, 'ENDERECO_UF'] = '.' if not uf else uf
    df.at[row.Index, 'ENDERECO_PAIS'] = '.' if not pais else pais

# ============================================================================
# SALVAR TABELA COM ENDEREÇOS VALIDADOS
# ============================================================================
print('Salvando tabela com endereços validados...')
job_config = bigquery.LoadJobConfig(schema=[
    bigquery.SchemaField('IDENTIFICACAO','STRING'),
    bigquery.SchemaField('NUMERO_BANCO', 'STRING'),
    bigquery.SchemaField('NUMERO_AGENCIA', 'STRING'),
    bigquery.SchemaField('NUMERO_CONTA', 'STRING'),
    bigquery.SchemaField('TIPO_CONTA', 'STRING'),
    bigquery.SchemaField('TIPO_TITULAR', 'STRING'),
    bigquery.SchemaField('PESSOA_INVESTIGADA', 'STRING'),
    bigquery.SchemaField('TIPO_PESSOA_TITULAR', 'STRING'),
    bigquery.SchemaField('CPF_CNPJ_TITULAR', 'STRING'),
    bigquery.SchemaField('NOME_TITULAR', 'STRING'),
    bigquery.SchemaField('NOME_DOC_IDENTIFICACAO', 'STRING'),
    bigquery.SchemaField('NUMERO_DOC_IDENTIFICACAO', 'STRING'),
    bigquery.SchemaField('ENDERECO_LOGRADOURO', 'STRING'),
    bigquery.SchemaField('ENDERECO_CIDADE', 'STRING'),
    bigquery.SchemaField('ENDERECO_UF', 'STRING'),
    bigquery.SchemaField('ENDERECO_PAIS', 'STRING'),
    bigquery.SchemaField('ENDERECO_CEP', 'STRING'),
    bigquery.SchemaField('TELEFONE_PESSOA', 'STRING'),
    bigquery.SchemaField('VALOR_RENDA', 'STRING'),
    bigquery.SchemaField('DATA_ATUALIZACAO_RENDA', 'STRING'),
    bigquery.SchemaField('DATA_INICIO_RELACIONAMENTO_CONTA', 'STRING'),
    bigquery.SchemaField('DATA_FIM_RELACIONAMENTO_CONTA', 'STRING'),
    bigquery.SchemaField('DATAHORA_IMPORTACAO', 'DATETIME')
])

table_name_final = "meli-bi-data.SBOX_LEGALES.TBL_QS_TITULARES_COM_ENDERECOS_VALIDADOS_FINCH"
bigquery_client.query(f"DELETE FROM `{table_name_final}` WHERE 1=1").result()

job = bigquery_client.load_table_from_dataframe(df, table_name_final, job_config=job_config)
job.result()

print('Processo de validação de endereços concluído.')
