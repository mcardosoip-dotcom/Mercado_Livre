import os
import pandas as pd
import re
import unicodedata

# Caminho onde estão os arquivos Parquet
CAMINHO_PARQUET = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões"

# Caminho onde o arquivo .txt será salvo
CAMINHO_SAIDA = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\DIM\comandos_create_tables.txt"

# Prefixo do schema no BigQuery
PREFIXO_TABELA = "<ENV>.STG"

# Lista para armazenar os comandos SQL
comandos_sql = []

def remover_acentos_e_caracteres(texto):
    """Remove acentos e caracteres especiais, retorna em snake_case minúsculo"""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'\W', '_', texto)
    texto = re.sub(r'_+', '_', texto)
    return texto.strip('_').lower()

def tratar_nome_tabela(texto):
    """Remove acentos e caracteres especiais, retorna em snake_case MAIÚSCULO"""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'\W', '_', texto)
    texto = re.sub(r'_+', '_', texto)
    return texto.strip('_').upper()

# Geração dos comandos com base nos arquivos Parquet
for nome_arquivo in os.listdir(CAMINHO_PARQUET):
    if nome_arquivo.lower().endswith(".parquet"):
        caminho_arquivo = os.path.join(CAMINHO_PARQUET, nome_arquivo)

        try:
            df = pd.read_parquet(caminho_arquivo, engine='pyarrow')
        except Exception as e:
            print(f"⚠️ Erro ao processar {nome_arquivo}: {e}")
            continue

        colunas_tratadas = []
        colunas_vistas = {}

        for col in df.columns:
            limpa = remover_acentos_e_caracteres(col)
            if limpa in colunas_vistas:
                colunas_vistas[limpa] += 1
                novo_nome = f"{limpa}_{colunas_vistas[limpa]}"
            else:
                colunas_vistas[limpa] = 1
                novo_nome = limpa
            colunas_tratadas.append(novo_nome)

        nome_base = os.path.splitext(nome_arquivo)[0]
        nome_tabela_tratada = tratar_nome_tabela(nome_base)
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
