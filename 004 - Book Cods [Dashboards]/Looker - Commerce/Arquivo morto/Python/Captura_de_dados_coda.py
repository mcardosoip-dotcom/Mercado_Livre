import requests
import pandas as pd
import os
import time

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
API_TOKEN = "f40c5115-17de-416d-8718-c715952eda63"
DOC_ID = "6_rrQy4CBF"
TABLE_ID = "table-UeVccqB1G1"
ARQUIVO_CSV = r'G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - Commerce\Python\Database_commerce_2025_FULL.csv'

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# =========================
# COLUNAS DESEJADAS NO CSV FINAL
# =========================
colunas_desejadas = [
    "Responsavel",
    "Solicitante",
    "Data_de_solicitacao",
    "Hora_de_solicitacao",
    "Ariba_CLM",
    "Nome_contraparte",
    "Objeto",
    "Descricao",
    "Valor_global",
    "Expectativa_GMV",
    "Cost_Avoidance",
    "Cost_Saving",
    "Data_Entrega",
    "Hora_Entrega",
    "Area",
    "Status_Macro",
    "Status_Micro"
]

# Mapeamento: Nome no Coda → Nome no CSV
mapa_colunas = {
    "Responsável": "Responsavel",
    "Solicitante": "Solicitante",
    "Data da solicitação": "Data_de_solicitacao",
    "Num. CLM": "Ariba_CLM",
    "Nome contraparte": "Nome_contraparte",
    "Objeto": "Objeto",
    "Descrição": "Descricao",
    "Valor Global (total)": "Valor_global",
    "Expectativa GMV": "Expectativa_GMV",
    "Cost Avoidance": "Cost_Avoidance",
    "Cost Saving": "Cost_Saving",
    "Data de entrega": "Data_Entrega",
    "Área": "Area",
    "Status Macro": "Status_Macro",
    "Sub Status": "Status_Micro"
}

# =========================
# ETAPA 0 – Aguardar sincronização do Coda
# =========================
print("⌛ Aguardando 20 segundos para sincronização com o Coda...")
time.sleep(20)

# =========================
# ETAPA 1 – Buscar colunas da tabela
# =========================
url_cols = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/columns"
response_cols = requests.get(url_cols, headers=headers)
columns_map = {}

if response_cols.status_code == 200:
    for col in response_cols.json().get("items", []):
        columns_map[col["id"]] = col["name"]
else:
    print("❌ Erro ao buscar colunas:", response_cols.text)
    exit()

# =========================
# ETAPA 2 – Buscar linhas (com paginação)
# =========================
url_rows = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
params = {}
all_rows = []

while True:
    response_rows = requests.get(url_rows, headers=headers, params=params)
    if response_rows.status_code != 200:
        print("❌ Erro ao buscar linhas:", response_rows.text)
        exit()

    data = response_rows.json()
    all_rows.extend(data.get("items", []))

    if "nextPageToken" in data:
        params["pageToken"] = data["nextPageToken"]
    else:
        break

print(f"✅ Total de linhas extraídas do Coda: {len(all_rows)}")

# =========================
# ETAPA 3 – Criar DataFrame formatado
# =========================
dados_formatados = []
for row in all_rows:
    linha = {"idRow": row["id"]}
    for col_id, valor in row["values"].items():
        nome_coda = columns_map.get(col_id, col_id)
        nome_final = mapa_colunas.get(nome_coda)

        if nome_final:
            # Trata datas com hora embutida
            if nome_final in ["Data_de_solicitacao", "Data_Entrega"] and isinstance(valor, str):
                try:
                    datetime_obj = pd.to_datetime(valor, errors="coerce")
                    linha[nome_final] = datetime_obj.date()
                    hora_col = "Hora_de_solicitacao" if nome_final == "Data_de_solicitacao" else "Hora_Entrega"
                    linha[hora_col] = datetime_obj.strftime("%H:%M") if not pd.isnull(datetime_obj) else ""
                except:
                    linha[nome_final] = ""
                    linha[hora_col] = ""
            else:
                linha[nome_final] = valor
    dados_formatados.append(linha)

df_coda = pd.DataFrame(dados_formatados)

# =========================
# ETAPA 4 – Garantir colunas e ordenação
# =========================
for col in colunas_desejadas:
    if col not in df_coda.columns:
        df_coda[col] = ""

df_coda = df_coda.sort_values(by=["Responsavel", "Data_de_solicitacao"])

# =========================
# ETAPA 5 – Comparar com versão anterior (opcional)
# =========================
if os.path.exists(ARQUIVO_CSV):
    df_antigo = pd.read_csv(ARQUIVO_CSV, encoding="utf-8-sig")
    df_atualizado = pd.concat([df_antigo, df_coda]).drop_duplicates(subset="idRow", keep="last")
    df_atualizado = df_atualizado.sort_values(by=["Responsavel", "Data_de_solicitacao"])
    print(f"🔁 Comparação feita. Total final: {len(df_atualizado)} linhas.")
else:
    df_atualizado = df_coda.copy()
    print(f"📄 Nenhum arquivo anterior encontrado. Salvando tudo.")

# =========================
# ETAPA 6 – Salvar CSV final
# =========================
df_atualizado[colunas_desejadas].to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")
print(f"✅ CSV final salvo com sucesso em: {ARQUIVO_CSV}")
