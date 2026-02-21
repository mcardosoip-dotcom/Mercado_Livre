import pandas as pd
import os

# Caminhos dos arquivos de entrada
arquivo_cap = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_17_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_CAP_unico.xlsx"
arquivo_ops = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_19_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_OPS_unico.xlsx"

# Caminho do arquivo de saída
arquivo_saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_30_Report_eLAW_Tarefas_Agendadas_Subsidios_Hispanos.xlsx"

# Leitura dos arquivos
print("📥 Lendo arquivo CAP...")
df_cap = pd.read_excel(arquivo_cap)

print("📥 Lendo arquivo OPS...")
df_ops = pd.read_excel(arquivo_ops)

# Padroniza as colunas de OPS com base na CAP
df_ops.columns = df_cap.columns[:len(df_ops.columns)]

# Consolidação das bases
df_consolidado = pd.concat([df_cap, df_ops], ignore_index=True)

# Verifica se o arquivo já existe
if os.path.exists(arquivo_saida):
    print(f"⚠️ Arquivo existente será substituído: {arquivo_saida}")

# Salva o resultado
df_consolidado.to_excel(arquivo_saida, index=False, sheet_name="Tarefas Consolidadas")

print(f"✅ Arquivo consolidado salvo em: {arquivo_saida}")
