import os
import pandas as pd

# Caminho da pasta onde os arquivos consolidados anuais estão
pasta_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\Consumidor.gov"

# Anos a considerar
anos = list(range(2017, 2026))

# Lista para armazenar os DataFrames
lista_df = []

# Detectar colunas-padrão com base no primeiro arquivo encontrado
colunas_padrao = None

for ano in anos:
    caminho_arquivo = os.path.join(pasta_base, str(ano), f"Consolidado {ano}.csv")
    if os.path.isfile(caminho_arquivo):
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8', low_memory=False)
            df["ANO"] = ano

            # Detectar colunas padrão a partir do primeiro arquivo válido
            if colunas_padrao is None:
                colunas_padrao = df.columns.tolist()

            # Ajustar colunas do DataFrame atual
            colunas_atual = df.columns.tolist()
            colunas_faltantes = [col for col in colunas_padrao if col not in colunas_atual]
            colunas_excedentes = [col for col in colunas_atual if col not in colunas_padrao]

            # Adiciona colunas faltantes
            for col in colunas_faltantes:
                df[col] = None

            # Remove colunas excedentes
            df = df[[col for col in colunas_padrao if col in df.columns]]

            # Garante a ordem das colunas
            df = df[colunas_padrao]

            lista_df.append(df)
        except Exception as e:
            print(f"❌ Erro ao ler {caminho_arquivo}: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho_arquivo}")

# Consolidação final
if lista_df:
    df_geral = pd.concat(lista_df, ignore_index=True)
    caminho_saida = os.path.join(pasta_base, "Consolidado Geral.csv")
    df_geral.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
    print(f"✅ Arquivo final consolidado salvo em: {caminho_saida}")
else:
    print("⚠️ Nenhum arquivo consolidado anual encontrado.")
