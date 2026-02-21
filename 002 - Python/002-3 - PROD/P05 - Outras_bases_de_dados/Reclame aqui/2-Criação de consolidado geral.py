import os
import pandas as pd
import time

# Início da contagem de tempo
inicio = time.time()

# Caminho da pasta onde estão os arquivos Consolidados
pasta_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Grupo_Database_2_Reclame_Aqui"

# Anos que foram processados
anos = list(range(2019, 2026))

# Lista para armazenar os DataFrames
lista_df_geral = []

for ano in anos:
    caminho_arquivo = os.path.join(pasta_base, f"Consolidado_{ano}.xlsx")
    if os.path.exists(caminho_arquivo):
        try:
            # Leitura usando engine otimizado e sem colunas extras
            df = pd.read_excel(caminho_arquivo, engine="openpyxl")
            if not df.empty:
                df["ANO"] = ano  # Adiciona coluna com o ano
                lista_df_geral.append(df)
            else:
                print(f"⚠️ Arquivo vazio: {caminho_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao ler {caminho_arquivo}: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho_arquivo}")

# Consolidar e salvar
if lista_df_geral:
    df_geral = pd.concat(lista_df_geral, ignore_index=True)
    arquivo_saida_geral = os.path.join(pasta_base, "Consolidado_Geral.xlsx")
    df_geral.to_excel(arquivo_saida_geral, index=False, engine="openpyxl")
    print(f"✅ Arquivo geral consolidado salvo em: {arquivo_saida_geral}")
else:
    print("⚠️ Nenhum arquivo anual válido encontrado para consolidar.")

# Tempo total
fim = time.time()
