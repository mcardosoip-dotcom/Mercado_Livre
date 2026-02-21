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
    """Limpa o cache de COM do win32com para evitar erros."""
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
    """Abre uma pasta de trabalho do Excel com múltiplas tentativas."""
    for i in range(tentativas):
        try:
            workbook = excel_app.Workbooks.Open(caminho_arquivo)
            return workbook
        except Exception as e:
            if 'rejeitada' in str(e).lower():
                print(f"Tentativa {i+1} falhou. O Excel está ocupado. Aguardando {intervalo} segundos...")
                time.sleep(intervalo)
            else:
                raise e
    raise Exception("Falha ao abrir o arquivo após múltiplas tentativas.")

def log_update(file_number, total_files, file_path, start_time, end_time):
    """Registra o sucesso do processamento no arquivo de log."""
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
    """Registra um erro no processamento no arquivo de log."""
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
    """Aguarda a conclusão da atualização de todas as conexões de dados."""
    print("Aguardando a atualização dos dados...")
    elapsed = 0
    while elapsed < max_wait:
        refresh_in_progress = False

        # Verifica o estado de cálculo do Excel
        if excel_app.CalculationState != 0: # xlDone is 0
            refresh_in_progress = True

        # Verifica as QueryTables
        if not refresh_in_progress:
            for sheet in workbook.Worksheets:
                for qt in sheet.QueryTables:
                    if qt.Refreshing:
                        refresh_in_progress = True
                        break
                if refresh_in_progress:
                    break
        
        # Verifica as conexões OLEDB
        if not refresh_in_progress:
            for connection in workbook.Connections:
                try:
                    if connection.OLEDBConnection and connection.OLEDBConnection.Refreshing:
                        refresh_in_progress = True
                        break
                except Exception:
                    # Algumas conexões podem não ter a propriedade OLEDBConnection
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
    """Tenta fechar a instância do Excel de forma segura."""
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

# >>> ALTERAÇÃO <<<
# A função agora recebe a instância do Excel como um parâmetro, em vez de criá-la.
def atualizar_e_salvar_excel(excel_app, caminho_arquivo, file_number, total_files, max_wait=600):
    workbook = None
    start_time = datetime.now()
    # Garante que end_time sempre terá um valor
    end_time = start_time 
    status_do_arquivo = ""
    try:
        print(f"\nIniciando processamento do arquivo {file_number} de {total_files}:\n{caminho_arquivo}\nàs {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # >>> ALTERAÇÃO <<<
        # As linhas que criavam uma nova instância do Excel foram removidas daqui.
        # A instância 'excel_app' agora é recebida como argumento.
        
        time.sleep(5) # Pequena pausa para garantir que o Excel está pronto
        workbook = abrir_workbook(excel_app, caminho_arquivo, tentativas=5, intervalo=10)
        time.sleep(45) # Mantido do código original, pode ser necessário para carregamento de dados

        print("Atualizando todas as conexões...")
        workbook.RefreshAll()
        wait_for_refresh(workbook, excel_app, max_wait)

        print("Salvando o arquivo...")
        workbook.Save()
        print("Fechando o arquivo...")
        workbook.Close(SaveChanges=True)

        end_time = datetime.now()
        status_do_arquivo = "Processamento Ok"
        print(f"Finalizado processamento do arquivo {file_number} de {total_files}:\n{caminho_arquivo}\nàs {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        log_update(file_number, total_files, caminho_arquivo, start_time, end_time)
        print(f"Arquivo '{os.path.basename(caminho_arquivo)}' atualizado, salvo e log registrado com sucesso!")
    
    except Exception as e:
        end_time = datetime.now()
        print(f"Ocorreu um erro no arquivo '{caminho_arquivo}': {e}")
        log_error(file_number, total_files, caminho_arquivo, str(e), start_time)
        status_do_arquivo = "Falha no processamento"
        global erro_encontrado
        erro_encontrado = True
        # Se o workbook foi aberto, tenta fechá-lo sem salvar para não travar
        if workbook:
            try:
                workbook.Close(SaveChanges=False)
            except Exception as close_e:
                print(f"Erro ao tentar fechar o workbook após falha: {close_e}")

    finally:
        # >>> ALTERAÇÃO <<<
        # A seção que fechava o Excel ('safe_quit') foi removida daqui.
        # Apenas os objetos do workbook são liberados.
        try:
            if workbook is not None:
                del workbook
            # A coleta de lixo é chamada no final do script principal
        except Exception as e:
            print("Erro ao liberar objeto COM do Workbook:", e)

        # Insere os dados do processamento no banco de dados
        inserir_dados(
            datetime.now().date().strftime("%Y-%m-%d"), 
            os.path.basename(caminho_arquivo),
            start_time.strftime("%H:%M:%S"), 
            end_time.strftime("%H:%M:%S"), 
            status_do_arquivo,
            "Diário"
        )

erro_encontrado = False

if __name__ == '__main__':
    limpar_cache_gen_py()
    # Limpa o arquivo de log no início da execução
    open(LOG_FILE, "w", encoding="utf-8").close()

    file_paths = [
        # r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Macro Tarefas Agendamentos Clean.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\006 - Dashboard Entradas Brasil e CORP\Versão 2\Data Self Information - Base ativa.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\006 - Dashboard Entradas Brasil e CORP\Versão 2\Data Self Information - Entradas e desfechos.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\006 - Dashboard Entradas Brasil e CORP\Versão 2\Data Self Information - TPN e SI.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\028 - Controle operacional Legal OPS\002 - Versão 3\Push Controle Operacional.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\005 - Dashboard Acomp de Tarefas\Push Acompanhamento de Tarefas.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\033 - Dashboard Penal\002 - Versão 2\Push dashboard Penal - Quantidade.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Processo_2_Input_BigQuery [FAAS]\003 - Bases Legales MLA x MLM\Push legales MLA e MLM.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Processo_2_Input_BigQuery [FAAS]\001 - Bases Legales\Push projeto FAAS.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Processo_3_Cust_IDS_MLA_MLM\Push inf MLA e MLM.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\046 - Pagamentos e garantia\Push Pagamentos em Garantia.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\048 - Dashboard Aguardando informações\Push Aguardando Informações.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\050 - Bases Comite\Extrato - Base comite.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\003 - Big Base DRE\002 - Modelo Tableau\Push e informações - DRE.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\065 - Dashboard Conta Invadida\Push Conta Invadida.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\036 - Dashboard Trabalhista\Novo modelo 2024\Data Self Information Trabalhista - Base ativa.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\036 - Dashboard Trabalhista\Novo modelo 2024\Data Self Information Trabalhista - Entradas e desfechos.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\005 - Legal Spend and Overheads\003 - Coração de fogo\Coração de fogo - Database.xlsx',
        r'G:\Drives compartilhados\Legales_Analytics_Legado\005 - Legal Spend and Overheads\003 - Coração de fogo\Coração de fogo - Geral.xlsx'
    ]

    total_files = len(file_paths)
    excel_app = None # Inicia a variável como nula

    # >>> ALTERAÇÃO <<<
    # O bloco try/finally garante que o Excel seja fechado mesmo se ocorrer um erro.
    try:
        print("Iniciando instância única do Excel para todo o processo...")
        excel_app = win32.Dispatch('Excel.Application')
        excel_app.Visible = True
        excel_app.DisplayAlerts = False
        print("Instância do Excel iniciada e visível.")

        for i, file_path in enumerate(file_paths, start=1):
            # Passa a instância única do Excel para a função de atualização
            atualizar_e_salvar_excel(excel_app, file_path, i, total_files)
        
        # >>> ALTERAÇÃO <<<
        # O comando para matar o processo do Excel foi removido do loop.
    
    except Exception as e:
        print(f"Ocorreu um erro fatal no script: {e}")
        # Define a flag de erro global em caso de falha na inicialização do Excel
        erro_encontrado = True
    
    finally:
        # >>> ALTERAÇÃO <<<
        # Este bloco agora é executado no final de todo o script.
        if excel_app is not None:
            print("\nTodos os arquivos foram processados. Encerrando o Excel...")
            safe_quit(excel_app)
            try:
                del excel_app
            except Exception as e:
                print(f"Erro ao liberar o objeto principal do Excel: {e}")
        
        # Força a coleta de lixo para limpar a memória
        gc.collect()

        # >>> ALTERAÇÃO <<<
        # O comando taskkill é executado uma única vez no final, como uma garantia
        # de que nenhum processo do Excel ficou para trás.
        print("Executando limpeza final para garantir que todos os processos do Excel foram encerrados.")
        os.system('taskkill /f /im excel.exe > nul 2>&1') # Oculta a saída do comando

    print("\nProcesso de atualização diária finalizado.")
    if erro_encontrado:
        print("Atenção: Um ou mais arquivos apresentaram erro durante o processamento. Verifique o log.")

