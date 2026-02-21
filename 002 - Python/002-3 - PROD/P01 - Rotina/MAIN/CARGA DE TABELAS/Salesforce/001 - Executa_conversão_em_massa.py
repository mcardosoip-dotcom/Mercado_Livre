# ================================================
# Descrição :  Geração de arquivos Parquet a partir de CSVs mapeados
#              com validação de estrutura e tratamento de colunas.
#              Leitura ajustada para separador ponto e vírgula (;),
#              garantindo compatibilidade com carga no BigQuery.
#              Apenas os cabeçalhos são tratados; os dados são mantidos.
# Autor : Marcelo Cardoso
# ================================================

import os
import pandas as pd
import unicodedata
import re
import pyarrow as pa
import pyarrow.parquet as pq
from mapeamento_fontes import MAPEAMENTO_FONTES

PASTA_SAIDA = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-02 - SF"

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

# Carrega mapeamento de fontes do arquivo Python
mapeamento = MAPEAMENTO_FONTES

# Valida estrutura do mapeamento
for item in mapeamento:
    if not all(key in item for key in ["Endereco", "Arquivo", "Arquivo final"]):
        raise ValueError(
            f"❌ Estrutura de mapeamento inválida.\n"
            f"Esperado: {{'Endereco', 'Arquivo', 'Arquivo final'}}\n"
            f"Encontrado: {list(item.keys())}"
        )

for row in mapeamento:
    caminho_csv = os.path.join(row["Endereco"], row["Arquivo"] + ".csv")
    nome_saida_parquet = os.path.join(
        PASTA_SAIDA,
        limpar_nome_arquivo(row["Arquivo final"]) + ".parquet"
    )

    try:
        try:
            # 🔄 Tenta ler primeiro com 'latin1', já que esta é a codificação mais comum na sua execução.
            df_csv = pd.read_csv(caminho_csv, sep=';', encoding='latin1', dtype=str)
        except UnicodeDecodeError:
            print(f"Aviso: Erro ao ler com latin1. Tentando com utf-8-sig → {caminho_csv}")
            # Tenta com 'utf-8-sig' como fallback
            df_csv = pd.read_csv(caminho_csv, sep=';', encoding='utf-8-sig', dtype=str)

        if df_csv.shape[1] <= 1:
            print(f"❌ Estrutura inválida: apenas {df_csv.shape[1]} coluna(s). Verifique delimitador ou conteúdo: {caminho_csv}")
            continue

        colunas_tratadas = [normalizar_coluna(col) for col in df_csv.columns]
        if len(set(colunas_tratadas)) != len(colunas_tratadas):
            raise ValueError(f"❌ Colunas duplicadas após normalização: {colunas_tratadas}")
        df_csv.columns = colunas_tratadas

        # Apenas conversão segura para string (sem alterar valores originais)
        df_csv = df_csv.astype(str)

        # Conversão para Parquet
        table = pa.Table.from_pandas(df_csv, preserve_index=False, schema=None)
        pq.write_table(table, nome_saida_parquet, compression='snappy')

        print(f"{nome_saida_parquet} → ✅ Sucesso\n")

    except Exception as e:
        print(f"{nome_saida_parquet} → ❌ Erro: {e}\n")

    print()
