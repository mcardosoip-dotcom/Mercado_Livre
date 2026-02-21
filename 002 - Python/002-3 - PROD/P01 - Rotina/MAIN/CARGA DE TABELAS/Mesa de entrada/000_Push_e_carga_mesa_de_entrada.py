import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from google.cloud import storage
from google.api_core.retry import Retry
import time
import pyarrow

data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

db_name = "mesa_entrada"
ip = "10.82.128.122"
user = "lhub_readonly"
password = os.getenv("DB_PASSWORD", "Ls3a3_4wq")
engine = create_engine(f"mysql+pymysql://{user}:{password}@{ip}:3306/{db_name}")

buckets = {"prod": "pdme000426", "dev": "ddme000426"}
subpasta_bucket = "Mesa_de_entrada"
cliente = storage.Client()
retry_policy = Retry(deadline=300)
upload_timeout = 300

pasta_temporaria = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Mesa de entrada\Buffer"
os.makedirs(pasta_temporaria, exist_ok=True)

caminho_log = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Mesa de entrada\LOG_execucao_mesa_entrada.txt"
os.makedirs(os.path.dirname(caminho_log), exist_ok=True)

tarefas = [
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

log_execucao = []
status_final = "Processamento Ok"

for sql, nome_arquivo in tarefas:
    print(f"\n⏳ Executando: {nome_arquivo}")
    inicio = time.time()

    try:
        with engine.connect() as conn:
            caminho_parquet = os.path.join(pasta_temporaria, nome_arquivo)
            df = pd.read_sql(text(sql), conn)

        duracao = round(time.time() - inicio, 2)
        num_linhas = len(df)
        colunas = list(df.columns)

        df.to_parquet(caminho_parquet, engine='pyarrow', index=False)
        print(f"✅ Arquivo Parquet gerado ({num_linhas} linhas, {duracao}s)")

        for ambiente, nome_bucket in buckets.items():
            try:
                bucket = cliente.bucket(nome_bucket)
                blob = bucket.blob(f"{subpasta_bucket}/{nome_arquivo}")
                blob.upload_from_filename(caminho_parquet, timeout=upload_timeout, retry=retry_policy)
                print(f"✔ Upload → {ambiente}: {nome_bucket}/{subpasta_bucket}/{nome_arquivo}")
            except Exception as e:
                print(f"❌ Erro no upload ({ambiente}): {e}")
                status_final = "Falha no processamento"

        log_execucao.append({
            "arquivo": nome_arquivo,
            "ok": True,
            "linhas": num_linhas,
            "colunas": colunas,
            "tempo_segundos": duracao
        })

    except Exception as erro:
        duracao = round(time.time() - inicio, 2)
        print(f"⚠️ Erro (conexão/consulta) em {nome_arquivo}: {erro}")
        print(f"   Continuando com as demais tarefas...")
        status_final = "Falha no processamento"
        log_execucao.append({
            "arquivo": nome_arquivo,
            "ok": False,
            "erro": str(erro),
            "tempo_segundos": duracao
        })

with open(caminho_log, "w", encoding="utf-8") as f:
    f.write(f"Log de Execução - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    for item in log_execucao:
        f.write(f"📌 Arquivo: {item['arquivo']}\n")
        if item.get("ok"):
            f.write(f"⏱ Tempo: {item['tempo_segundos']}s\n")
            f.write(f"📦 Linhas: {item['linhas']}\n")
            f.write(f"📑 Colunas ({len(item['colunas'])}): {', '.join(item['colunas'])}\n")
        else:
            f.write(f"❌ Erro: {item.get('erro', 'N/A')}\n")
            f.write(f"⏱ Tempo até falha: {item['tempo_segundos']}s\n")
        f.write("-" * 60 + "\n")

print(f"\n📝 Log salvo em: {caminho_log}")
print("✅ Processo finalizado." if status_final == "Processamento Ok" else "⚠️ Processo finalizado com erros.")
