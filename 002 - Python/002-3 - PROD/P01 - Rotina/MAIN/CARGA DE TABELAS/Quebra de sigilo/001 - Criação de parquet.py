import os
import pandas as pd
import unicodedata
import re
from datetime import datetime
from dateutil import parser
from pathlib import Path

# Lista base de nomes de colunas de data (sem acento ou espaço)
COLUNAS_DE_DATA_BASE = [
    'Data Envio Sisbacen',
    'Data Recebimento Inst.',
    'CCS-Inicio do período solicitado',
    'CCS-Fim do período solicitado',
    'CCS-Prazo limite de resposta'
]

# Funções auxiliares
def remover_acentos(texto):
    if not isinstance(texto, str):
        return texto
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def limpar_coluna(col):
    col = remover_acentos(col)
    col = re.sub(r'\W+', '_', col)
    col = re.sub(r'__+', '_', col)
    return col.strip('_').lower()

def tentar_converter_data(valor):
    try:
        if not valor or pd.isna(valor):
            return None
        valor_str = str(valor).strip()
        if valor_str in ["--", "00/00/0000", "nan", "NaT"]:
            return None
        valor_str = valor_str[:19]
        if re.match(r'^\d{4}-\d{2}-\d{2}', valor_str):
            try:
                return datetime.strptime(valor_str, "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y')
            except:
                return datetime.strptime(valor_str, "%Y-%m-%d").strftime('%d/%m/%Y')
        dt = parser.parse(valor_str, dayfirst=True)
        return dt.strftime('%d/%m/%Y')
    except Exception:
        return None

# Caminhos
caminho_entrada = Path(r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\Quebra de sigilo")
caminho_saida = Path(r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-03 - Quebra de Sigilo")

excel_file = caminho_entrada / "Quebra_de_sigilo_controle.xlsx"
output_path = caminho_saida / "Quebra_de_sigilo_controle.parquet"

# Verificação de existência
assert excel_file.exists(), f"❌ Arquivo não encontrado: {excel_file}"

# Abas a carregar
abas = ["Base_22_23", "Base_24", "Base_25"]

# Leitura e unificação das abas
df_consolidado = pd.concat([pd.read_excel(excel_file, sheet_name=aba) for aba in abas], ignore_index=True)

# Padronização dos nomes das colunas
df_consolidado.columns = [limpar_coluna(col) for col in df_consolidado.columns]

# Tratamento de colunas de data
for col in df_consolidado.columns:
    if any(col == base.lower().replace(" ", "_").replace(".", "").replace("-", "_") for base in COLUNAS_DE_DATA_BASE):
        df_consolidado[col] = df_consolidado[col].apply(tentar_converter_data)

# Conversão de todos os campos para string
df_consolidado = df_consolidado.astype(str)

# Exportação para Parquet
df_consolidado.to_parquet(output_path, index=False)

print(f"✅ Arquivo Parquet salvo com sucesso em: {output_path}")
