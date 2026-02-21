import os
import win32com.client


# === CONFIGURAÇÃO ===
pasta_origem = r"C:\Users\mcard\Desktop\eLAW Bases"
destino = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões"
nome_arquivo_destino = "Database_2_Report_eLAW_Amelia.xlsx"

# === LOCALIZA O ARQUIVO QUE CONTÉM 'Amelia' ===
arquivo_alvo = None
for nome_arquivo in os.listdir(pasta_origem):
    if "Amelia" in nome_arquivo and nome_arquivo.endswith(".xlsx"):
        arquivo_alvo = os.path.join(pasta_origem, nome_arquivo)
        break

if not arquivo_alvo:
    raise FileNotFoundError("Nenhum arquivo contendo 'Amelia' encontrado na pasta.")

# === ABRE NO EXCEL EM MODO DE REPARO E SALVA ===
excel = win32com.client.Dispatch("Excel.Application")
excel.DisplayAlerts = False
excel.Visible = False

# Modo de reparo ativado via Open method
try:
    workbook = excel.Workbooks.Open(arquivo_alvo, CorruptLoad=1)  # CorruptLoad=1 → modo de reparo
    caminho_destino = os.path.join(destino, nome_arquivo_destino)
    workbook.SaveAs(caminho_destino)
    workbook.Close(False)
    print(f"Arquivo reparado salvo com sucesso em: {caminho_destino}")
except Exception as e:
    print(f"Erro ao abrir ou salvar o arquivo: {e}")
finally:
    excel.Quit()
