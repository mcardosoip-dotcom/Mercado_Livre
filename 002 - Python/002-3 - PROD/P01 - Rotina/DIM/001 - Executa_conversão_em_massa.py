# ================================================
# Descrição : Converte planilhas Excel mapeadas em arquivos Parquet,
#             aplicando padronizações nos nomes de colunas,
#             sem alterar os dados das células.
# Autor     : Marcelo Cardoso
# ================================================

import sys
import os
import pandas as pd
import unicodedata
import re
from mapeamento_fontes import MAPEAMENTO_FONTES

PASTA_SAIDA = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões"

def remover_acentos(texto):
    if not isinstance(texto, str):
        return texto
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def normalizar_coluna(col):
    col = remover_acentos(str(col)).lower().strip()
    col = re.sub(r'[^\w\s]', '_', col)
    col = re.sub(r'\s+', '_', col)
    col = re.sub(r'_+', '_', col)
    return col.strip('_')

def limpar_nome_arquivo(nome):
    nome = remover_acentos(nome)
    nome = re.sub(r'[^\w\s-]', '_', nome)
    nome = re.sub(r'\s+', '_', nome)
    nome = re.sub(r'_+', '_', nome)
    return nome.strip('_')

def converter_excel_para_parquet(caminho_excel, nome_aba, nome_saida_parquet):
    df = pd.read_excel(caminho_excel, sheet_name=nome_aba, dtype=str)
    df.columns = [normalizar_coluna(col) for col in df.columns]

    df = df.dropna(how='all')
    df = df[~df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)]

    df.to_parquet(nome_saida_parquet, index=False, compression='snappy')

# Carrega mapeamento de fontes do arquivo Python
mapeamento = MAPEAMENTO_FONTES

# Valida estrutura do mapeamento
for item in mapeamento:
    if not all(key in item for key in ["Endereco", "Arquivo", "Aba", "Arquivo final"]):
        raise ValueError(
            f"❌ Estrutura de mapeamento inválida.\n"
            f"Esperado: {{'Endereco', 'Arquivo', 'Aba', 'Arquivo final'}}\n"
            f"Encontrado: {list(item.keys())}"
        )

for row in mapeamento:
    caminho_excel = os.path.join(row["Endereco"], row["Arquivo"] + ".xlsx")
    nome_aba = row["Aba"]
    nome_arquivo_tratado = limpar_nome_arquivo(row["Arquivo final"])
    nome_saida = os.path.join(PASTA_SAIDA, nome_arquivo_tratado + ".parquet")

    try:
        converter_excel_para_parquet(
            caminho_excel=caminho_excel,
            nome_aba=nome_aba,
            nome_saida_parquet=nome_saida
        )
        print(f"{nome_saida} → ✅ Sucesso\n")
    except Exception as e:
        print(f"{nome_saida} → ❌ Erro: {e}\n")
