# ================================================
# Descrição :  O processo faz o backup dos arquivos baixados da plataforma eLAW
# Autor : Marcelo Cardoso
# ================================================

import os
import shutil
from datetime import datetime
from coda_processo_geral import inserir_dados

# Obtém a data atual e o horário de início
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Definição dos caminhos das pastas
source_folder = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW"
base_dest_folder = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Histórico"

# Cria uma subpasta no histórico com a data e hora atuais
dest_folder = os.path.join(base_dest_folder, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
os.makedirs(dest_folder, exist_ok=True)
print(f"Pasta criada: {dest_folder}")

# Itera sobre os arquivos na pasta de origem e os copia para a nova pasta
for file_name in os.listdir(source_folder):
    if file_name.lower().endswith('.xlsx'):
        source_file = os.path.join(source_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)

        # Remove o arquivo de destino caso ele já exista para permitir a substituição
        if os.path.exists(dest_file):
            os.remove(dest_file)
            print(f"Arquivo {dest_file} substituído.")

        # Copia o arquivo para a pasta de destino
        shutil.copy(source_file, dest_file)
        print(f"Arquivo {source_file} copiado para {dest_file}.")

# Registra o horário de término e insere os dados de log
hora_fim = datetime.now().strftime("%H:%M:%S")
inserir_dados(data_atual, "Backup de arquivos eLAW", hora_inicio, hora_fim, "Processamento Ok", "Diário")
