"""
================================================================================
11 - GERAÇÃO DE ZIP
================================================================================
Descrição: Consolida todos os arquivos gerados em ZIP por investigado
Objetivo: Criar arquivo ZIP final contendo todos os documentos
Conexão: SBOX_LEGALES (Storage)
Saída: {IDENTIFICACAO}.zip (por investigado)
================================================================================
"""

import os
import zipfile
from datetime import date
from google.cloud import storage
from io import BytesIO

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
print('Iniciando o processo de geração de ZIP...')

area = os.environ.get("area")
processing_date_string = date.today().strftime('%Y-%m-%d')
execution_date = os.environ.get("DF_TIME_TO").replace("-", "").replace(":", "").replace(" ", "")
project = 'meli-bi-data'

# Conexões mantidas
storage_client = connections["SBOX_LEGALES"].storage_client

bucket_name = "meli-bi-data-tmp"
root_folder = f"LEGALES/{area}/QUEBRA_SIGILO_FINCH/"
destination_execution_file = root_folder + execution_date + "/"
circular_letter_3454_directory = destination_execution_file + "carta_circular_3454/"
financial_statement_directory = destination_execution_file + "extrato_financeiro/"

# ============================================================================
# OBTER LISTA DE INVESTIGADOS
# ============================================================================
print('Obtendo lista de investigados...')
bucket = storage_client.bucket(bucket_name)

# Listar todos os diretórios de investigados
blobs = bucket.list_blobs(prefix=circular_letter_3454_directory)
identificacoes = set()

for blob in blobs:
    # Extrair identificação do caminho
    path_parts = blob.name.replace(circular_letter_3454_directory, '').split('/')
    if len(path_parts) > 1:
        identificacoes.add(path_parts[0])

print(f'Total de investigados: {len(identificacoes)}')

# ============================================================================
# GERAR ZIP POR INVESTIGADO
# ============================================================================
for identificacao in identificacoes:
    print(f'Gerando ZIP para: {identificacao}')
    id_sanitized = identificacao.replace('/', '-').replace('\\', '-')
    
    # Criar ZIP em memória
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Arquivos da Carta Circular 3454
        carta_path = f"{circular_letter_3454_directory}{id_sanitized}/"
        carta_files = [
            f"{id_sanitized}_CONTAS.txt",
            f"{id_sanitized}_AGENCIAS.txt",
            f"{id_sanitized}_EXTRATO.txt",
            f"{id_sanitized}_ORIGEM_DESTINO.txt",
            f"{id_sanitized}_TITULARES.txt",
            f"{id_sanitized}_INVESTIGADO.txt"
        ]
        
        for file_name in carta_files:
            blob_path = carta_path + file_name
            blob = bucket.blob(blob_path)
            if blob.exists():
                file_content = blob.download_as_bytes()
                zip_file.writestr(file_name, file_content)
                print(f'  Adicionado: {file_name}')
        
        # Arquivos de extrato financeiro
        # Buscar arquivos CSV do investigado
        extrato_prefix = financial_statement_directory
        for blob in bucket.list_blobs(prefix=extrato_prefix):
            if identificacao in blob.name and blob.name.endswith('.csv'):
                file_name = os.path.basename(blob.name)
                file_content = blob.download_as_bytes()
                zip_file.writestr(file_name, file_content)
                print(f'  Adicionado: {file_name}')
    
    # Upload do ZIP
    zip_buffer.seek(0)
    zip_filename = f"{destination_execution_file}{id_sanitized}.zip"
    blob_zip = bucket.blob(zip_filename)
    blob_zip.upload_from_file(zip_buffer, content_type='application/zip')
    print(f'  ZIP criado: {zip_filename}')

print('Processo de geração de ZIP concluído.')
