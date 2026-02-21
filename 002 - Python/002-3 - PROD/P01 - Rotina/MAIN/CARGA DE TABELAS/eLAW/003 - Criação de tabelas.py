import os
import pandas as pd
import re
import unicodedata

# Caminho onde estão os arquivos Parquet
CAMINHO_PARQUETS = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW"

# Caminho onde o arquivo .txt será salvo
CAMINHO_SAIDA = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\eLAW\comandos_create_tables.txt"

# Prefixo do schema no BigQuery
PREFIXO_TABELA = "<ENV>.STG"

# Lista para armazenar os comandos SQL
comandos_sql = []

def tratar_coluna(texto):
    """Remove acentos e caracteres especiais, retorna em snake_case minúsculo."""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'\W', '_', texto)
    texto = re.sub(r'_+', '_', texto)
    return texto.strip('_').lower()

def tratar_tabela(texto):
    """Remove acentos e caracteres especiais, retorna em snake_case MAIÚSCULO."""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'\W', '_', texto)
    texto = re.sub(r'_+', '_', texto)
    return texto.strip('_').upper()

# Geração dos comandos com base nos arquivos Parquet
for nome_arquivo in os.listdir(CAMINHO_PARQUETS):
    if nome_arquivo.lower().endswith(".parquet"):
        caminho_arquivo = os.path.join(CAMINHO_PARQUETS, nome_arquivo)

        try:
            df = pd.read_parquet(caminho_arquivo, engine='pyarrow')
        except Exception as e:
            print(f"⚠️ Erro ao processar {nome_arquivo}: {e}")
            continue

        colunas_tratadas = []
        colunas_usadas = {}

        for col in df.columns:
            col_tratada = tratar_coluna(col)
            if col_tratada in colunas_usadas:
                colunas_usadas[col_tratada] += 1
                novo_nome = f"{col_tratada}_{colunas_usadas[col_tratada]}"
            else:
                colunas_usadas[col_tratada] = 1
                novo_nome = col_tratada
            colunas_tratadas.append(novo_nome)

        nome_base = os.path.splitext(nome_arquivo)[0]
        nome_tabela_tratada = tratar_tabela(nome_base)
        tabela_destino = f"{PREFIXO_TABELA}.{nome_tabela_tratada}"

        colunas_formatadas = ",\n  ".join([f"`{col}` STRING" for col in colunas_tratadas])
        comando = f"""CREATE OR REPLACE TABLE `{tabela_destino}` (
  {colunas_formatadas}
);\n"""
        comandos_sql.append(comando)

# Escreve os comandos no arquivo final
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    for comando in comandos_sql:
        f.write(comando + "\n")

print(f"✅ Comandos SQL salvos com sucesso em:\n{CAMINHO_SAIDA}")
