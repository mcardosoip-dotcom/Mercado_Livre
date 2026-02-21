# ================================================
# Descrição :  O processo de renomeação de arquivos considerando o padrão
# Autor : Marcelo Cardoso
# ================================================

import os
import time
import shutil
from datetime import datetime
from coda_processo_geral import inserir_dados

# Define data e hora de início do processo
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Caminhos das pastas
folder_path = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Arquivos tratados eLAW\Temp"
dest_folder = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Arquivos tratados eLAW"
historico_root = os.path.join(folder_path, "Histórico")  # Pasta "Histórico" dentro de Temp

# Caminho para o arquivo de log
log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "LOG_Renomear_arquivos_eLAW.txt")

# Separador para melhor visualização no log
divider = "=" * 80

def registrar_log(mensagem):
    """Grava a mensagem de log com timestamp e separadores no arquivo de log."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    entry = f"\n{divider}\n[{timestamp}] {mensagem}\n{divider}\n"
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(entry)

# Criar/limpar o arquivo de log antes de iniciar o processo
with open(log_file, "w", encoding="utf-8") as f:
    header = f"{divider}\nLog de renomeação iniciado em {time.strftime('%Y-%m-%d %H:%M:%S')}\n{divider}\n"
    f.write(header)

# Renomear os arquivos na pasta Temp (remove o prefixo "Temp_" de arquivos .xlsx)
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx") and filename.startswith("Temp_"):
        new_name = filename.replace("Temp_", "", 1)
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        try:
            os.rename(old_file, new_file)
            message = f"Arquivo renomeado: {filename} -> {new_name}"
            print(message)
            registrar_log(message)
        except Exception as e:
            message = f"Falha ao renomear {filename}: {e}"
            print(message)
            registrar_log(message)

# Garantir que a pasta de destino exista
os.makedirs(dest_folder, exist_ok=True)

# Copiar os arquivos (já renomeados) da pasta Temp para a pasta de destino
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Verifica se é um arquivo (não uma pasta)
    if os.path.isfile(file_path):
        dest_file = os.path.join(dest_folder, filename)
        try:
            shutil.copy2(file_path, dest_file)
            message = f"Arquivo copiado para destino: {filename}"
            print(message)
            registrar_log(message)
        except Exception as e:
            message = f"Falha ao copiar {filename}: {e}"
            print(message)
            registrar_log(message)

# Criação da pasta de histórico com data e hora (modelo YYYY-MM-DD_HH-MM-SS)
timestamp_folder = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
historico_dest = os.path.join(historico_root, timestamp_folder)
os.makedirs(historico_dest, exist_ok=True)

# Mover os arquivos da pasta Temp para a nova pasta de histórico
# Obs.: é importante ignorar a pasta "Histórico" para evitar realocar a estrutura já criada
for filename in os.listdir(folder_path):
    if filename == "Histórico":
        continue
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        try:
            shutil.move(file_path, historico_dest)
            message = f"Arquivo movido para histórico: {filename}"
            print(message)
            registrar_log(message)
        except Exception as e:
            message = f"Falha ao mover {filename} para histórico: {e}"
            print(message)
            registrar_log(message)

# Registrar a hora final do processo e inserir os dados do processamento
hora_fim = datetime.now().strftime("%H:%M:%S")
inserir_dados(data_atual, "Renomear arquivos eLAW", hora_inicio, hora_fim, "Processamento Ok", "Diário")
