"""
================================================================================
EXPORTAR WHOWNER.BT_MP_ACC_MOVEMENTS PARA LOG TEXTO
================================================================================
Descrição: Consulta a tabela BT_MP_ACC_MOVEMENTS no BigQuery (WHOWNER),
           traz todas as colunas e grava em um arquivo .txt com uma linha
           de cabeçalho e uma linha por registro (separador: tab).
Uso: Execute no ambiente com acesso ao BigQuery (meli-bi-data).
     Opcional: LIMIT para teste; deixe None para tabela completa.
================================================================================
"""

import os
from pathlib import Path

# query_job.to_dataframe() e df.to_csv() usam pandas (já dependência do projeto)

# Tentar usar conexão do orquestrador; senão criar cliente BigQuery direto
try:
    bigquery_client = connections["SBOX_LEGALES"].bigquery_client
except NameError:
    from google.cloud import bigquery
    bigquery_client = bigquery.Client(project="meli-bi-data")

PROJECT = "meli-bi-data"
DATASET = "WHOWNER"
TABLE = "BT_MP_ACC_MOVEMENTS"
FULL_TABLE = f"`{PROJECT}.{DATASET}.{TABLE}`"

# Limite de linhas (None = tabela completa; use ex.: 1000 para teste)
LIMIT = None  # altere para 1000 ou outro número para teste

# Pasta de saída do log (ajuste se quiser outro diretório)
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR  # ou ex.: SCRIPT_DIR / "LOGs_export"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "BT_MP_ACC_MOVEMENTS_log.txt"

def main():
    sql = f"SELECT * FROM {FULL_TABLE}"
    if LIMIT is not None:
        sql += f" LIMIT {int(LIMIT)}"
    print(f"Executando: {sql[:80]}...")
    query_job = bigquery_client.query(sql)
    df = query_job.to_dataframe()
    # Uma linha de cabeçalho + uma linha por registro (tab como separador)
    df.to_csv(OUTPUT_FILE, sep="\t", index=False, header=True, encoding="utf-8", na_rep="")
    print(f"Linhas escritas: {len(df)} (+ 1 cabeçalho)")
    print(f"Arquivo salvo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
