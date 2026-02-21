import pandas as pd
import numpy as np
import os

# Caminho original do arquivo
arquivo = r'G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P00 - Book de Querys\P00-2 - Dashboards\CODA - Commerce\Consolidada_Commerce.xlsx'

# Leitura do arquivo
df = pd.read_excel(arquivo)

# === Limpeza das colunas de data (coluna A e coluna O) ===
coluna_a = df.columns[0]  # Primeira coluna (coluna A)
coluna_o = 'O'            # Nome literal da coluna O

colunas_data = [coluna_a, coluna_o]
for col in colunas_data:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

# === Limpeza das colunas de valores (E, F, G, H) ===
colunas_valores = ['E', 'F', 'G', 'H']
for col in colunas_valores:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Caminho para salvar o arquivo ajustado
pasta, nome_arquivo = os.path.split(arquivo)
nome_base, ext = os.path.splitext(nome_arquivo)
novo_nome = f'{nome_base}_ajustado{ext}'
caminho_saida = os.path.join(pasta, novo_nome)

# Salva o arquivo ajustado
df.to_excel(caminho_saida, index=False)

print(f"Arquivo ajustado salvo em: {caminho_saida}")
