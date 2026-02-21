# ================================================
# Descrição :  Consolidação de todas as bases de contencioso, criando uma base única 
#              e atualizada que considera todo o histórico do Brasil e demais países
# Autor : Marcelo Cardoso
# ================================================

import os
import pandas as pd

# Caminho da pasta
pasta = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões"

# Lista de arquivos a consolidar
arquivos = [
    "Database_7_Report_eLAW_Contencioso_Brasil_Completo.xlsx",
    "Database_8_Report_eLAW_Contencioso_Brasil_Parcial.xlsx",
    "Database_4_Report_eLAW_Contencioso_Brasil_Parcial_Outgoing.xlsx",
    "Database_10_Report_eLAW_Contencioso_Hispanos_Completa.xlsx"
]

# Lista para armazenar os DataFrames válidos
lista_df = []

for arquivo in arquivos:
    caminho = os.path.join(pasta, arquivo)
    if os.path.exists(caminho):
        try:
            df = pd.read_excel(caminho, skiprows=5)
            if not df.empty:
                lista_df.append(df)
            else:
                print(f"⚠️ Arquivo vazio: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {arquivo}")

# Consolidação
if lista_df:
    df_consolidado = pd.concat(lista_df, ignore_index=True)

    # Remoção de duplicidades com base no campo (Processo) ID
    if "(Processo) ID" in df_consolidado.columns:
        df_consolidado = df_consolidado.drop_duplicates(subset=["(Processo) ID"])

    # Salvar arquivo final
    caminho_saida = os.path.join(pasta, "Database_40_Report_eLAW_Contencioso_Full.xlsx")
    df_consolidado.to_excel(caminho_saida, index=False)
    print(f"✅ Consolidação concluída com {len(df_consolidado)} registros: {caminho_saida}")
else:
    print("❌ Nenhum DataFrame válido foi consolidado.")
