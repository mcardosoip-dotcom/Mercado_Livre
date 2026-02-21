# ================================================
# Descrição : Tratamento de arquivos corrompidos que são baixados do eLAW
# Autor : Marcelo Cardoso (revisado)
# ================================================

import os
import traceback
import time
import gc
import pythoncom
import win32com.client
from pywintypes import com_error
from datetime import datetime
from coda_processo_geral import inserir_dados

# === Diretório de logs ===
log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
os.makedirs(log_dir, exist_ok=True)
LOG_FILE = os.path.join(log_dir, "LOG_Ajustar_arquivos_corrompidos_eLAW.txt")

def registrar_log(mensagem):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {mensagem}\n")

def safe_quit(excel_app, retries=3, wait_interval=5):
    for i in range(retries):
        try:
            excel_app.Quit()
            registrar_log("Instância do Excel encerrada com sucesso.")
            return True
        except Exception as e:
            registrar_log(f"Tentativa {i+1} para encerrar o Excel falhou: {e}")
            time.sleep(wait_interval)
    registrar_log("Não foi possível encerrar a instância do Excel após múltiplas tentativas.")
    return False

def reparar_e_converter(arquivo_origem, arquivo_destino, max_tentativas=2):
    pythoncom.CoInitialize()
    excel = None
    workbook = None

    try:
        try:
            excel = win32com.client.DispatchEx("Excel.Application")
        except com_error as ce:
            registrar_log(f"Erro ao iniciar Excel (COM error): {ce}")
            return False
        except Exception as e:
            registrar_log(f"Erro genérico ao iniciar Excel: {e}")
            return False

        excel.Visible = False  # Não exibir a janela do Excel
        excel.DisplayAlerts = False  # Suprimir caixas de diálogo interativas

        for tentativa in range(1, max_tentativas + 1):
            try:
                registrar_log(f"Tentativa {tentativa}: Abrindo {os.path.basename(arquivo_origem)}")
                workbook = excel.Workbooks.Open(arquivo_origem, CorruptLoad=1)
                break
            except com_error as ce:
                registrar_log(f"Erro COM na tentativa {tentativa}: {ce}")
                time.sleep(2)
            except Exception as e:
                registrar_log(f"Erro genérico na tentativa {tentativa}: {e}")
                time.sleep(2)

        if not workbook:
            registrar_log(f"Falha ao abrir {os.path.basename(arquivo_origem)} após {max_tentativas} tentativas.")
            return False

        if os.path.exists(arquivo_destino):
            os.remove(arquivo_destino)
            registrar_log(f"Arquivo de destino existente removido: {os.path.basename(arquivo_destino)}")

        workbook.SaveAs(arquivo_destino, FileFormat=51)
        workbook.Close(False)

        registrar_log(f"Arquivo reparado com sucesso: {os.path.basename(arquivo_origem)}")
        print(f"Arquivo reparado com sucesso: {os.path.basename(arquivo_origem)}")
        return True

    except Exception as e:
        registrar_log(f"Falha inesperada ao reparar {os.path.basename(arquivo_origem)}: {e}")
        traceback.print_exc()
        return False

    finally:
        try:
            if workbook:
                workbook.Close(False)
        except:
            pass
        try:
            if excel:
                safe_quit(excel)
        except:
            pass
        try:
            del workbook
            del excel
            gc.collect()
        except Exception as e:
            registrar_log(f"Erro ao liberar objetos COM: {e}")
        os.system('taskkill /f /im excel.exe')
        pythoncom.CoUninitialize()

def main():
    data_atual = datetime.now().date().strftime("%Y-%m-%d")
    hora_inicio = datetime.now().strftime("%H:%M:%S")
    status_do_processo = "Processamento Ok"

    pasta_origem = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW"
    pasta_destino = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Arquivos tratados eLAW\Temp"

    os.makedirs(pasta_destino, exist_ok=True)
    open(LOG_FILE, "w", encoding="utf-8").close()

    arquivos = [arquivo for arquivo in os.listdir(pasta_origem) if arquivo.lower().endswith(".xlsx")]
    if not arquivos:
        registrar_log("Nenhum arquivo .xlsx encontrado na pasta de origem.")
        print("Nenhum arquivo .xlsx encontrado na pasta de origem.")
        return

    total_arquivos = len(arquivos)
    for idx, arquivo in enumerate(arquivos, start=1):
        progresso = f"{idx} de {total_arquivos}"
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)

        # Pula arquivos já tratados
        if os.path.exists(caminho_destino):
            registrar_log(f"[{progresso}] Arquivo já tratado anteriormente: {arquivo}. Pulando.")
            print(f"[{progresso}] Arquivo já tratado anteriormente: {arquivo}. Pulando.")
            continue

        registrar_log(f"[{progresso}] Iniciando processamento do arquivo: {arquivo}")
        print(f"\n[{progresso}] Iniciando processamento do arquivo: {arquivo}")

        sucesso = reparar_e_converter(caminho_origem, caminho_destino)

        if not sucesso:
            registrar_log(f"[{progresso}] Erro ao tratar o arquivo, mas será considerado como OK no processo geral.")
            print(f"[{progresso}] Erro ao tratar o arquivo, mas será considerado como OK no processo geral.")

        registrar_log("-" * 80)
        print("-" * 80)

    registrar_log("Processamento concluído.")
    print("Processamento concluído.")

    hora_fim = datetime.now().strftime("%H:%M:%S")
    inserir_dados(data_atual, "Ajuste de arquivos corrompidos eLAW", hora_inicio, hora_fim, status_do_processo, "Diário")

if __name__ == "__main__":
    main()
