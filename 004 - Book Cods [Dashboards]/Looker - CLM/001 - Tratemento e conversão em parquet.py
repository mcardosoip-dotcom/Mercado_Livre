import pandas as pd
import unicodedata
import re
import os

def clean_column_names(df):
    """
    Limpa os nomes das colunas de um DataFrame:
    - Remove acentos.
    - Substitui espaços por underscores e outros caracteres especiais por nada.
    - Converte para minúsculas.
    """
    new_columns = []
    for col in df.columns:
        # Remover acentos e converter para minúsculas
        col_cleaned = unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('utf-8').lower()
        
        # Substituir espaços e caracteres não alfanuméricos por underscores
        col_cleaned = re.sub(r'[^a-z0-9_]+', '_', col_cleaned)
        
        # Remover underscores extras no início ou fim e múltiplos underscores
        col_cleaned = re.sub(r'^_+|_+$', '', col_cleaned)
        col_cleaned = re.sub(r'_{2,}', '_', col_cleaned)
        
        new_columns.append(col_cleaned)
    df.columns = new_columns
    return df

def process_and_convert(input_filename, output_directory, prefix):
    """
    Processa um arquivo CSV, limpa os nomes das colunas e o salva como Parquet.
    """
    input_csv_path = os.path.join(output_directory, f'{input_filename}.csv')
    
    # Gerar o nome do arquivo de saída Parquet
    base_output_name = unicodedata.normalize('NFKD', input_filename).encode('ascii', 'ignore').decode('utf-8').lower()
    base_output_name = re.sub(r'\s+', '_', base_output_name)
    output_parquet_filename = f'{prefix}_{base_output_name}.parquet'
    output_parquet_path = os.path.join(output_directory, output_parquet_filename)

    try:
        # Ler o arquivo CSV
        print(f"Lendo o arquivo CSV: {input_csv_path}")
        df = pd.read_csv(input_csv_path)

        # Limpar os nomes das colunas
        df = clean_column_names(df)
        print("Cabeçalhos ajustados para remover espaços, acentos e caracteres especiais.")

        # Salvar o DataFrame como Parquet
        print(f"Salvando o arquivo Parquet em: {output_parquet_path}")
        df.to_parquet(output_parquet_path, index=False)

        print(f"\nArquivo '{input_filename}.csv' convertido para '{output_parquet_filename}' com sucesso!")
        print(f"O arquivo Parquet foi salvo em: {output_parquet_path}")
    
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado no caminho especificado: {input_csv_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo '{input_filename}.csv': {e}")

# --- Configurações ---
# Diretório onde estão os arquivos de entrada e onde os arquivos de saída serão salvos
base_directory = r'G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - CLM\Databases'

# Lista com os nomes base dos arquivos (sem a extensão .csv)
files_to_convert = [
    'Métricas de contratos',
    'Control de contratos',
    'Métricas de flujos activos'
]

# Prefixo para os nomes dos arquivos Parquet de saída
output_prefix = 'carga_docusign'

# --- Execução do script ---
for filename in files_to_convert:
    print(f"\n--- Iniciando o processamento do arquivo: {filename} ---")
    process_and_convert(filename, base_directory, output_prefix)
    print("--- Processamento concluído. ---")