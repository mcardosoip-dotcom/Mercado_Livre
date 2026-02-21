import pandas as pd
import os

# Caminho do arquivo de origem
arquivo_origem = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_19_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_OPS.xlsx"

# Nome do novo arquivo consolidado
arquivo_saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_19_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_OPS_unico.xlsx"

# Nomes das abas a consolidar
abas = ["Tarefas (Agendamentos) - Enligh", "Tarefas (Agendamentos) - Interv"]

# Lista para armazenar os DataFrames
dfs = []

# Processar cada aba
for aba in abas:
    print(f"🔄 Lendo aba: {aba}")
    df = pd.read_excel(arquivo_origem, sheet_name=aba, skiprows=5)
    
    # Remove linhas totalmente em branco
    df = df.dropna(how='all')

    # Adiciona à lista
    dfs.append(df)

# Consolida os DataFrames
df_consolidado = pd.concat(dfs, ignore_index=True)

# Verifica se o arquivo já existe
if os.path.exists(arquivo_saida):
    print(f"⚠️ Arquivo existente será substituído: {arquivo_saida}")

# Salva o resultado
df_consolidado.to_excel(arquivo_saida, index=False, sheet_name="Tarefas Consolidadas")

print(f"✅ Arquivo salvo em: {arquivo_saida}")
