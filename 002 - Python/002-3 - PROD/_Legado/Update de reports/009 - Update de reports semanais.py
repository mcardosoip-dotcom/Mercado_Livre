# ================================================
# Descrição :  O processo faz a atualização de todos os acompanhamentos diários 
#              baseado na lista que está em anexo neste código
# Autor : Marcelo Cardoso
# ================================================

import time
import datetime
import os
import win32com.client as win32
import gc  # Para forçar a coleta de lixo
from datetime import datetime
from coda_processo_geral import inserir_dados
import shutil
import site

# Define o diretório e o caminho absoluto para o arquivo de log
log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
LOG_FILE = os.path.join(log_dir, "LOG_Update_de_reports_diarios.txt")

def limpar_cache_gen_py():
    gen_py_path = os.path.join(site.getusersitepackages(), 'win32com', 'gen_py')
    if os.path.exists(gen_py_path):
        try:
            shutil.rmtree(gen_py_path)
            print("Cache COM (gen_py) limpo com sucesso.")
        except Exception as e:
            print(f"Erro ao limpar gen_py: {e}")
    else:
        print("Pasta gen_py não encontrada. Nenhuma limpeza necessária.")

def abrir_workbook(excel_app, caminho_arquivo, tentativas=10, intervalo=15):
    for i in range(tentativas):
        try:
            workbook = excel_app.Workbooks.Open(caminho_arquivo)
            return workbook
        except Exception as e:
            if 'rejeitada' in str(e).lower():
                print(f"Tentativa {i+1} falhou. Aguardando {intervalo} segundos para tentar novamente...")
                time.sleep(intervalo)
            else:
                raise e
    raise Exception("Falha ao abrir o arquivo após múltiplas tentativas.")

def log_update(file_number, total_files, file_path, start_time, end_time):
    duration = (end_time - start_time).total_seconds() / 60
    log_entry = (
        f"Arquivo {file_number} de {total_files}\n"
        f"Arquivo: {file_path}\n"
        f"Start: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Duração: {duration:.2f} minutos\n"
        f"Status: Processamento Ok\n"
        "------------------------------------------\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def log_error(file_number, total_files, file_path, error_message, start_time):
    error_time = datetime.now()
    log_entry = (
        f"Arquivo {file_number} de {total_files}\n"
        f"Arquivo: {file_path}\n"
        f"Start: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Erro: {error_message}\n"
        f"Horário do Erro: {error_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "Status: Não processado\n"
        "------------------------------------------\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def wait_for_refresh(workbook, excel_app, max_wait=600):
    elapsed = 0
    while elapsed < max_wait:
        refresh_in_progress = False

        if excel_app.CalculationState != 0:
            refresh_in_progress = True

        for sheet in workbook.Worksheets:
            for qt in sheet.QueryTables:
                if qt.Refreshing:
                    refresh_in_progress = True
                    break
            if refresh_in_progress:
                break

        for connection in workbook.Connections:
            try:
                if connection.OLEDBConnection and connection.OLEDBConnection.Refreshing:
                    refresh_in_progress = True
                    break
            except Exception:
                pass

        if not refresh_in_progress:
            break

        time.sleep(1)
        elapsed += 1

    if elapsed >= max_wait:
        print("Atenção: O refresh pode não ter sido completamente concluído após o tempo máximo de espera.")
    else:
        print(f"Refresh concluído em {elapsed} segundos.")

def safe_quit(excel_app, retries=3, wait_interval=5):
    for i in range(retries):
        try:
            excel_app.Quit()
            print("Instância do Excel encerrada com sucesso.")
            return True
        except Exception as e:
            print(f"Tentativa {i+1} para encerrar o Excel falhou: {e}")
            time.sleep(wait_interval)
    print("Não foi possível encerrar a instância do Excel após múltiplas tentativas.")
    return False

def atualizar_e_salvar_excel(caminho_arquivo, file_number, total_files, max_wait=600):
    excel_app = None
    workbook = None
    start_time = datetime.now()
    status_do_arquivo = ""
    try:
        print(f"\nIniciando processamento do arquivo {file_number} de {total_files}:\n{caminho_arquivo}\nàs {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        excel_app = win32.Dispatch('Excel.Application')  # Corrigido: evita erro de gen_py
        excel_app.Visible = True
        excel_app.DisplayAlerts = False

        time.sleep(5)
        workbook = abrir_workbook(excel_app, caminho_arquivo, tentativas=5, intervalo=10)
        time.sleep(45)

        workbook.RefreshAll()
        wait_for_refresh(workbook, excel_app, max_wait)

        workbook.Save()
        workbook.Close(SaveChanges=True)

        end_time = datetime.now()
        status_do_arquivo = "Processamento Ok"
        print(f"Finalizado processamento do arquivo {file_number} de {total_files}:\n{caminho_arquivo}\nàs {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        log_update(file_number, total_files, caminho_arquivo, start_time, end_time)
        print(f"Arquivo '{caminho_arquivo}' atualizado, salvo e log registrado com sucesso!")
    except Exception as e:
        end_time = datetime.now()
        print(f"Ocorreu um erro no arquivo '{caminho_arquivo}': {e}")
        log_error(file_number, total_files, caminho_arquivo, str(e), start_time)
        status_do_arquivo = "Falha no processamento"
        global erro_encontrado
        erro_encontrado = True
    finally:
        if excel_app is not None:
            safe_quit(excel_app)
        try:
            if workbook is not None:
                del workbook
            if excel_app is not None:
                del excel_app
            gc.collect()
        except Exception as e:
            print("Erro ao liberar objetos COM:", e)

        inserir_dados(
            datetime.now().date().strftime("%Y-%m-%d"), 
            os.path.basename(caminho_arquivo),
            start_time.strftime("%H:%M:%S"), 
            end_time.strftime("%H:%M:%S"), 
            status_do_arquivo,
            "Semanal"
        )

erro_encontrado = False

if __name__ == '__main__':
    limpar_cache_gen_py()
    open(LOG_FILE, "w", encoding="utf-8").close()

    file_paths = [
        r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Processo_2_Update_NPS\Push de informações NPS.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Processo_1_Nostradamus\Push de informações Nostradamus.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\002 - Estudos e processos AD HOC\053 - Informações Gerais Cecilia Brunelli\2025\001 - Push Reclamos Laborales\Push Reclamos Laborales.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\002 - Estudos e processos AD HOC\053 - Informações Gerais Cecilia Brunelli\2025\002 - Push Tercerizados Corp\Push Tercerizados Corp.xlsx'
    ]

    total_files = len(file_paths)
    for i, file_path in enumerate(file_paths, start=1):
        atualizar_e_salvar_excel(file_path, i, total_files)
        os.system('taskkill /f /im excel.exe')