import os
import pandas as pd
import warnings

# Suprime avisos irrelevantes do openpyxl
warnings.filterwarnings("ignore", message="Workbook contains no default style")

# Pasta base onde estão os diretórios por ano
pasta_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Grupo_Database_2_Reclame_Aqui"

# Anos a processar
anos = range(2019, 2026)

for ano in anos:
    pasta_ano = os.path.join(pasta_base, str(ano))
    arquivo_saida = os.path.join(pasta_base, f"Consolidado_{ano}.xlsx")
    lista_df = []

    if not os.path.isdir(pasta_ano):
        print(f"⚠️ Pasta não encontrada para o ano {ano}: {pasta_ano}")
        continue

    arquivos_xlsx = [f for f in os.listdir(pasta_ano) if f.lower().endswith(".xlsx")]
    if not arquivos_xlsx:
        print(f"⚠️ Nenhum arquivo .xlsx encontrado para o ano {ano}")
        continue

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(pasta_ano, arquivo)
        try:
            df = pd.read_excel(caminho_arquivo, skiprows=3, engine="openpyxl")
            if not df.empty and not df.isna().all(axis=1).all():
                lista_df.append(df)
            else:
                print(f"⚠️ Arquivo vazio ou inválido ignorado: {arquivo}")
        except Exception as e:
            print(f"❌ Erro ao ler {arquivo} ({ano}): {e}")

    if lista_df:
        try:
            df_consolidado = pd.concat(lista_df, ignore_index=True)
            df_consolidado.to_excel(arquivo_saida, index=False, engine="openpyxl")
            print(f"✅ Consolidado salvo: {arquivo_saida}")
        except Exception as e:
            print(f"❌ Erro ao salvar consolidado {ano}: {e}")
    else:
        print(f"⚠️ Nenhum DataFrame válido para consolidar no ano {ano}")
