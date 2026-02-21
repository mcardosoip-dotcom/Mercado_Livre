import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import time
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------- CONFIG ----------------
db_name = "mesa_entrada"
ip = "10.82.128.122"
user = "lhub_readonly"
password = os.getenv("DB_PASSWORD", "Ls3a3_4wq")

PASTA_TEMPORARIA = "/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics/002 - Python/002-3 - PROD/P01 - Rotina/MAIN/CARGA DE TABELAS/Mesa de entrada/Buffer"
os.makedirs(PASTA_TEMPORARIA, exist_ok=True)

TAREFAS = [
    ("SELECT *, DAYOFWEEK(fecha) AS dia_semana FROM vista_entradas", "Mesa_entrada_vista_entradas.parquet"),
    ("SELECT * FROM dw_hist_casos_x_estado", "Mesa_entrada_dw_hist_casos_x_estado.parquet"),
    ("SELECT * FROM entradas", "Mesa_entrada_tab_entradas.parquet"),
    ("SELECT * FROM vista_cantidad_casos_usuarios", "Mesa_entrada_vista_cantidad_casos_usuarios.parquet"),
    ("SELECT * FROM vista_usuarios", "Mesa_entrada_vista_usuarios.parquet"),
    ("SELECT * FROM mesa_entrada.v_metricas_qa", "Mesa_entrada_v_metricas_qa.parquet"),
    ("SELECT * FROM mesa_entrada.estados", "Mesa_entrada_estados.parquet"),
    ("SELECT * FROM mesa_entrada.tipo_documentos", "Mesa_entrada_tipo_documentos.parquet"),
    ("SELECT * FROM mesa_entrada.metricas_big_query", "Mesa_entrada_metricas_big_query.parquet"),
    ("SELECT * FROM mesa_entrada.origenes", "Mesa_entrada_origenes.parquet"),
    ("SELECT * FROM mesa_entrada.entradas_estados", "Mesa_entrada_entradas_estados.parquet")
]

def extrair_salvar_parquet(tarefas, pasta_destino, user, password, ip, db_name):
    logger.info("Iniciando conexão com o banco")
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{ip}:3306/{db_name}")

    log_execucao = []
    status_final = "Ok"

    try:
        with engine.connect() as conn:
            logger.info("Conexão estabelecida")

            for idx, (sql, nome_arquivo) in enumerate(tarefas, start=1):
                logger.info(f"Início tarefa {idx}/{len(tarefas)} | {nome_arquivo}")
                inicio_total = time.time()

                caminho_parquet = os.path.join(pasta_destino, nome_arquivo)

                logger.info("Executando query")
                inicio_query = time.time()
                df = pd.read_sql(text(sql), conn)
                tempo_query = round(time.time() - inicio_query, 2)

                logger.info(f"Query finalizada | linhas={len(df)} | tempo={tempo_query}s")

                logger.info("Iniciando escrita parquet")
                inicio_write = time.time()
                df.to_parquet(caminho_parquet, engine="pyarrow", index=False)
                tempo_write = round(time.time() - inicio_write, 2)

                tempo_total = round(time.time() - inicio_total, 2)

                logger.info(
                    f"Tarefa concluída | arquivo={nome_arquivo} | "
                    f"query={tempo_query}s | escrita={tempo_write}s | total={tempo_total}s"
                )

                log_execucao.append({
                    "arquivo": nome_arquivo,
                    "linhas": len(df),
                    "colunas": list(df.columns),
                    "tempo_query": tempo_query,
                    "tempo_escrita": tempo_write,
                    "tempo_total": tempo_total,
                    "caminho_local": caminho_parquet
                })

    except Exception:
        logger.exception("Erro inesperado durante a extração")
        status_final = "Falha na Extração"

    finally:
        engine.dispose()
        logger.info("Conexão encerrada")

    return log_execucao, status_final

if __name__ == "__main__":
    logger.info("Processo iniciado")

    logs, status = extrair_salvar_parquet(
        TAREFAS, PASTA_TEMPORARIA, user, password, ip, db_name
    )

    logger.info(f"Processo finalizado | status={status}")

    if status == "Ok":
        for log in logs:
            logger.info(f"Arquivo gerado: {log['caminho_local']}")
