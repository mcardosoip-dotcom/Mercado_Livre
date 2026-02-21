# ================================================
# Descrição : Lista arquivos e datas de carga no bucket DEV
#              e salva resultado em Excel com marcação de atraso
# Autor : Marcelo Cardoso
# ================================================

import os
from datetime import datetime
from google.cloud import storage
import pytz
import pandas as pd

# Configurações
bucket_dev = "ddme000426"
subpastas_bucket = [
    "Projeto banco de dados/Salesforce_Databases",
    "Projeto banco de dados/eLAW_Databases",
    "Mesa_de_entrada",
    "Projeto banco de dados/Quebra_Sigilo"
]

# Caminho de saída
caminho_saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\O_que_temos_no_Bucket.xlsx"

# Inicializa cliente e fuso horário
cliente = storage.Client()
fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora = datetime.now(fuso_brasilia)

# Lista para DataFrame
dados_output = []

for subpasta in subpastas_bucket:
    try:
        bucket = cliente.bucket(bucket_dev)
        blobs = bucket.list_blobs(prefix=subpasta)

        for blob in blobs:
            if blob.name.endswith("/"):
                continue

            data_mod = blob.updated.astimezone(fuso_brasilia)
            nome_arquivo = os.path.basename(blob.name)
            esta_atrasado = data_mod.date() < agora.date()

            dados_output.append({
                "Pasta": subpasta,
                "Arquivo": nome_arquivo,
                "Data de Modificação": data_mod.strftime('%d/%m/%Y %H:%M:%S'),
                "Atrasado": "Sim" if esta_atrasado else "Não"
            })

    except Exception as e:
        dados_output.append({
            "Pasta": subpasta,
            "Arquivo": "Erro ao acessar",
            "Data de Modificação": str(e),
            "Atrasado": "Erro"
        })

# Gera e salva Excel
df_resultado = pd.DataFrame(dados_output)
df_resultado.to_excel(caminho_saida, index=False)

print("\n✅ Relatório salvo em Excel com sucesso.\n")
