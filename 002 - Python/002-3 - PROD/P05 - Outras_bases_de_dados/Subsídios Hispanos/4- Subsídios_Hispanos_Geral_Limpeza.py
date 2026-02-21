import os
import shutil

# Caminhos dos arquivos a serem movidos
arquivos_para_mover = [
    r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_17_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_CAP_unico.xlsx",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Database_19_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_OPS_unico.xlsx"
]

# Pasta de destino
destino = r"G:\Drives compartilhados\Legales_Analytics\001 - Databases_e_dimensões\Arquivo morto\Pastas Temp"

# Loop para mover arquivos
for caminho in arquivos_para_mover:
    if os.path.exists(caminho):
        novo_caminho = os.path.join(destino, os.path.basename(caminho))
        shutil.move(caminho, novo_caminho)
        print(f"📁 Arquivo movido para o arquivo morto: {os.path.basename(caminho)}")
    else:
        print(f"⚠️ Arquivo não encontrado: {os.path.basename(caminho)}")
