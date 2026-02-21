import pandas as pd
import os

# Caminho do arquivo original
arquivo_origem = r"G:\Drives compartilhados\Legales_Analytics\006 - Reports e Acompanhamentos\028 - Controle operacional Legal OPS\002 - Versão 3\Push Controle Operacional.xlsx"
arquivo_destino = arquivo_origem.replace(".xlsx", " Clean.xlsx")

# Colunas a remover por aba
colunas_por_aba = {
    "Cadastro - Tarefas": [
        "Processo - Indicar ajuste (Nome do campo, erro, detalhamento)",
        "Processo - Informar ajustes",
        "Processo - Informar ajustes_4",
        "Processo - Indicar ajuste (Nome do campo, erro, detalhamento)_5",
        "Processo - Motivo do Ajuste",
        "Processo - Pedido de ajuste foi correto?",
        "Processo - Motivo do Ajuste_6"
    ],
    "Ofícios": [
        "Issue: Number",
        "Issue: Tipo de registro"
    ]
}

# Leitura das abas
todas_abas = pd.read_excel(arquivo_origem, sheet_name=None, engine='openpyxl')

# Escrita do novo arquivo limpo
with pd.ExcelWriter(arquivo_destino, engine='xlsxwriter') as writer:
    for nome_aba, df in todas_abas.items():
        df = df.dropna(how='all').dropna(axis=1, how='all')  # limpa vazios

        # Remove colunas específicas se a aba estiver na lista
        if nome_aba in colunas_por_aba:
            colunas_remover = colunas_por_aba[nome_aba]
            df = df.drop(columns=[col for col in colunas_remover if col in df.columns], errors='ignore')

        df.to_excel(writer, sheet_name=nome_aba, index=False)

print(f"✅ Arquivo limpo salvo em: {arquivo_destino}")
