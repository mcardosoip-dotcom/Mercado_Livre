import base64
import json
import os
from datetime import date
from google.oauth2 import service_account
from google.cloud import storage, bigquery
import pandas as pd
import numpy as np
import requests as req

area = os.environ.get("area")
processing_date_string = date.today().strftime('%Y-%m-%d')
execution_date = os.environ.get("DF_TIME_TO").replace("-", "").replace(":", "").replace(" ", "")
project = 'meli-bi-data'

storage_client = connections["BigQuery_Default_DME"].storage_client
bigquery_client = connections["BigQuery_Default_DME"].bigquery_client

bucket_name = "ddme000426"
root_folder = f"LEGALES/{area}/QUEBRA_SIGILO_TUNING/"
destination_execution_file = root_folder + execution_date + "/"
account_file = destination_execution_file + "TITULARES.txt"
circular_letter_3454_directory = destination_execution_file + "carta_circular_3454/"
financial_statement_directory = destination_execution_file + "extrato_financeiro/"

table_name = "ddme000426-gopr4nla6zo-furyid.STG.TBL_QS_TITULARES_TUNING"
source_import_table = "ddme000426-gopr4nla6zo-furyid.STG.STG_QS_PLANILHA_PRESENTA_CAD_VF_TUNING"
address_lookup_table = "ddme000426-gopr4nla6zo-furyid.SBOX_LEGALES.PROJETO_ACRE_ADDRESSES_TUNING" # Assumindo que essa também terá sufixo _TUNING

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
              UPPER(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(NOME_TITULAR,'[á,Á,à,À,ã,Ã,â,Â]','A'),'[É,é,ê,Ê]','E'),'[Í,í,Î,î]','I'), '[Ó,ó,Õ,ö,Õ,õ]','O'),'[Ú,ú,û,Ü,ü]','U'), '[Ç,ç]','C'),'[^0-9a-zA-Z]+',' ')) AS NOME_TITULAR,
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
    LEFT JOIN `{}` B ON A.ENDERECO_CEP = B.zip_code
    WHERE DATAHORA_IMPORTACAO = (
    SELECT MAX(DATAHORA_IMPORTACAO) FROM `{}`
);""".format(table_name, address_lookup_table, source_import_table)
query_job = bigquery_client.query(command)
df = query_job.to_dataframe()

table_name = address_lookup_table # Usando a variável definida acima
command = """SELECT * FROM `{}`;""".format(table_name)
query_job = bigquery_client.query(command)
df_address = query_job.to_dataframe()

for row in df.itertuples(index=True, name='Pandas'):
    cep = row.ENDERECO_CEP.replace(".", "").replace("-", "").replace("None", "").strip() if row.ENDERECO_CEP is not None else ''
    address = ''
    logradouro = ''
    cidade = ''
    uf = ''
    pais = ''
 
    if row.ENDERECO_LOGRADOURO is not None and row.ENDERECO_LOGRADOURO != '':
        continue
 
    if len(cep) == 0:
        cep = '.'
    elif len(row.ENDERECO_CEP) >= 8:
        cep = cep[0: 8]
        df_address_filtered = df_address.loc[df_address['zip_code'] == cep]
        if df_address_filtered.empty:
            cep_encontrado = True
            try:
                resposta = req.get(f'https://cep.awesomeapi.com.br/json/{cep}')
                if resposta.status_code == 200:
                    address = resposta.json()
                    logradouro = address['address']
                    cidade = address['city']
                    uf = address['state']
                    pais = 'BRA'
                else:
                    raise Exception()
            except Exception:
                try:
                    resposta = req.get(f'http://correiosapi.apphb.com/cep/{cep}')
                    if resposta.status_code == 200:
                        address = resposta.json()
                        if address['status'] in [400, 404]:
                            raise Exception()
                        logradouro = address['tipodelogradouro'] + " " + address['logradouro']
                        cidade = address['cidade']
                        uf = address['estado']
                        pais = 'BRA'
                    else:
                        raise Exception()
                except Exception:
                    try:
                        resposta = req.get(f'https://ws.apicep.com/cep/{cep}.json')
                        if resposta.status_code == 200:
                            address = resposta.json()
                            if address['status'] in [400, 404]:
                                raise Exception()
                            logradouro = address['address']
                            cidade = address['city']
                            uf = address['state']
                            pais = 'BRA'
                        else:
                            raise Exception()
                    except Exception:
                        try:
                            resposta = req.get(f'https://viacep.com.br/ws/{cep}/json/')
                            if resposta.status_code == 200:
                                address = resposta.json()
                                logradouro = address['logradouro']
                                cidade = address['localidade']
                                uf = address['uf']
                                pais = 'BRA'
                            else:
                                raise Exception()
                        except Exception:
                            cep_encontrado = False
            
            if cep_encontrado:
                table_name = address_lookup_table # Usando a variável definida acima
                command = "INSERT INTO `{}` (zip_code, street_name, city, state, country, last_update_date) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(table_name, cep, logradouro, cidade, uf, pais, processing_date_string)
                bigquery_client.query(command)

                new_data = pd.DataFrame([{
                    'zip_code': cep, 
                    'street_name': logradouro, 
                    'city': cidade, 
                    'state': uf, 
                    'country': pais, 
                    'last_update_date': processing_date_string
                }])
                df_address = pd.concat([df_address, new_data], ignore_index=True)
        else:
            cep = df_address_filtered.zip_code.values[0]
            logradouro = df_address_filtered.street_name.values[0]
            cidade = df_address_filtered.city.values[0]
            uf = df_address_filtered.state.values[0]
            pais = df_address_filtered.country.values[0]

    print(f"cep: {cep} - logradouro:{logradouro} - cidade:{cidade} - uf:{uf} - pais:{pais}")

    df.at[row.Index, 'ENDERECO_CEP'] = '.' if not cep else cep
    df.at[row.Index, 'ENDERECO_LOGRADOURO'] = '.' if not logradouro else logradouro[:79]
    df.at[row.Index, 'ENDERECO_CIDADE'] = '.' if not cidade else cidade
    df.at[row.Index, 'ENDERECO_UF'] = '.' if not uf else uf
    df.at[row.Index, 'ENDERECO_PAIS'] = '.' if not pais else pais

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

table_name = "ddme000426-gopr4nla6zo-furyid.SBOX_LEGALES.TBL_QS_TITULARES_COM_ENDERECOS_VALIDADOS_TUNING" # Assumindo sufixo _TUNING
bigquery_client.query(f"DELETE FROM `{table_name}` WHERE 1=1")

job = bigquery_client.load_table_from_dataframe(
    df, table_name, job_config=job_config
)

job.result()