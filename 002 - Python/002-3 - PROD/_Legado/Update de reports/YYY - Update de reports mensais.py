import time
import datetime
import os
import win32com.client as win32
import gc  # Para forçar a coleta de lixo
from datetime import datetime
from coda_processo_geral import inserir_dados

# Define o diretório e o caminho absoluto para o arquivo de log
log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
LOG_FILE = os.path.join(log_dir, "LOG_Update_de_reports_diarios.txt")

def abrir_workbook(excel_app, caminho_arquivo, tentativas=10, intervalo=15):
    """
    Tenta abrir o workbook, com um mecanismo de retry caso a chamada seja rejeitada.
    """
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
    """
    Registra no arquivo de log os detalhes do processamento concluído com sucesso,
    exibindo a duração do processamento em minutos.
    """
    duration = (end_time - start_time).total_seconds() / 60  # duração em minutos
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
    """
    Registra no arquivo de log os detalhes do processamento que gerou erro.
    """
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
    """
    Aguarda até que o refresh de todas as fontes de dados seja concluído ou até atingir
    o tempo máximo de espera (default: 600 segundos).
    """
    elapsed = 0
    while elapsed < max_wait:
        refresh_in_progress = False

        # Verifica se os cálculos do Excel foram concluídos
        if excel_app.CalculationState != 0:
            refresh_in_progress = True

        # Verifica se há QueryTables em atualização em cada planilha
        for sheet in workbook.Worksheets:
            for qt in sheet.QueryTables:
                if qt.Refreshing:
                    refresh_in_progress = True
                    break
            if refresh_in_progress:
                break

        # Verifica conexões OLEDB, se existirem
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
    """
    Tenta encerrar a instância do Excel utilizando retries se a chamada for rejeitada.
    """
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
    """
    Processa e salva o arquivo Excel:
      - Cria uma instância isolada do Excel (visível ao usuário),
      - Abre o arquivo, inicia o refresh das fontes de dados e aguarda a conclusão,
      - Salva e fecha o arquivo,
      - Registra os logs (sucesso ou erro) e garante o encerramento da instância.
      - Chama a função inserir_dados com o nome do arquivo em processamento.
    """
    excel_app = None
    workbook = None
    start_time = datetime.now()
    status_do_arquivo = ""
    try:
        print(f"\nIniciando processamento do arquivo {file_number} de {total_files}:\n{caminho_arquivo}\nàs {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Cria a instância do Excel e torna-a visível
        excel_app = win32.gencache.EnsureDispatch('Excel.Application')
        excel_app.Visible = True          # Exibe o Excel para o usuário
        excel_app.DisplayAlerts = False    # Oculta alertas
        
        # Tempo para que o Excel seja devidamente iniciado
        time.sleep(5)
        
        # Abre o workbook com retry
        workbook = abrir_workbook(excel_app, caminho_arquivo, tentativas=5, intervalo=10)
        # Aguarda um delay para garantir que o workbook esteja totalmente carregado
        time.sleep(45)
        
        # Inicia o refresh dos dados
        workbook.RefreshAll()
        wait_for_refresh(workbook, excel_app, max_wait)
        
        # Salva e fecha o workbook
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
        # Encerra a instância do Excel utilizando safe_quit para tentar encerrar eventuais atividades presas
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
        
        # Chama inserir_dados para registrar os dados deste processamento individual
        # Aqui usamos o nome base do arquivo (sem caminho completo)
        inserir_dados(
            datetime.now().date().strftime("%Y-%m-%d"), 
            os.path.basename(caminho_arquivo),
            start_time.strftime("%H:%M:%S"), 
            end_time.strftime("%H:%M:%S"), 
            status_do_arquivo,
            "Mensais"
            
        )
       

# Variável para controlar se algum erro foi encontrado durante o processamento
erro_encontrado = False

if __name__ == '__main__':
    # Limpa o arquivo de log antes da execução
    open(LOG_FILE, "w", encoding="utf-8").close()
    
    # Lista de arquivos (acompanhamentos) a serem processados
    file_paths = [
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\023 - Comparativo de escritórios\Nova versão 2024\Versão Calculada\Push de informações Calculada.xlsb'
    ]
    
    total_files = len(file_paths)
    for i, file_path in enumerate(file_paths, start=1):
        atualizar_e_salvar_excel(file_path, i, total_files)
        # Para garantir que quaisquer instâncias pendentes sejam encerradas, usamos taskkill
        os.system('taskkill /f /im excel.exe')
