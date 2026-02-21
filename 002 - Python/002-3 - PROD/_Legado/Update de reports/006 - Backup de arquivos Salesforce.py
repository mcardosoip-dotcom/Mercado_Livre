# ================================================
# Descrição :  O processo faz o backup dos arquivos baixados da plataforma Salesforce
# Autor : Marcelo Cardoso
# ================================================

import os
import shutil
from datetime import datetime
from coda_processo_geral import inserir_dados

# Registro da data atual e do horário de início
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Caminho de origem comum (pasta "Download Salesforce")
source_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download Salesforce"

# Destino para os arquivos de Embargos
embargos_dest = r"G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\028 - Controle operacional Legal OPS\002 - Versão 2\Database Salesforce\Embargos Salesforce"

# Destino para os arquivos de Ofícios/Informativos
oficios_dest = r"G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\028 - Controle operacional Legal OPS\002 - Versão 2\Database Salesforce\Ofícios Salesforce"

# Listas de arquivos a copiar (extensão .csv)
embargos_files = [
    "Incoming Embargos.csv",
    "Outgoing Embargos.csv",
    "Pending Embargos (BCRA e não BCRA).csv"
]

oficios_files = [
    "Incoming Oficios.csv",
    "Outcoming Ofícios.csv",
    "Pending Informativos.csv"
]

# Função para copiar arquivos individuais, substituindo se necessário
def copy_files(file_list, source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for file_name in file_list:
        source_path = os.path.join(source, file_name)
        dest_path = os.path.join(destination, file_name)
        
        if not os.path.isfile(source_path):
            print(f"Arquivo não encontrado: {source_path}")
            continue

        if os.path.exists(dest_path):
            os.remove(dest_path)
            print(f"Arquivo existente removido: {dest_path}")

        try:
            shutil.copy2(source_path, dest_path)
            print(f"Arquivo copiado com sucesso:\n   Origem: {source_path}\n   Destino: {dest_path}")
        except Exception as e:
            print(f"Erro ao copiar o arquivo {file_name}: {e}")

# Copiar os arquivos de Embargos para o destino correspondente
print("Copiando arquivos de Embargos...")
copy_files(embargos_files, source_dir, embargos_dest)

print("\nCopiando arquivos de Ofícios/Informativos...")
copy_files(oficios_files, source_dir, oficios_dest)

# ---------------------------------------------------------------------------
# Após processar os arquivos, copiar o conteúdo da pasta "Download Salesforce"
# para um subdiretório dentro da pasta "Histórico" (nomeado com data e hora atuais)
# ---------------------------------------------------------------------------

# Diretório base para histórico
base_historico_folder = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download Salesforce\Histórico"

# Cria um novo subdiretório no histórico com a data e hora atuais
historico_dest = os.path.join(base_historico_folder, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
os.makedirs(historico_dest, exist_ok=True)
print(f"\nPasta de histórico criada: {historico_dest}")

# Função para copiar todo o conteúdo da pasta de origem para o destino,
# ignorando a pasta "Histórico" para evitar recursão
def copy_all_files(source, destination):
    for item in os.listdir(source):
        # Ignora a pasta "Histórico" (independente de acentuação) para não copiar recursivamente
        if item.lower() in ['histórico', 'historico']:
            continue
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
            print(f"Arquivo copiado: {s} -> {d}")
        elif os.path.isdir(s):
            shutil.copytree(s, d)
            print(f"Pasta copiada: {s} -> {d}")

print("\nCopiando conteúdo de 'Download Salesforce' para o diretório de histórico...")
copy_all_files(source_dir, historico_dest)

# Registro do horário de término e inserção dos dados de log
hora_fim = datetime.now().strftime("%H:%M:%S")
inserir_dados(data_atual, "Backup de arquivos Salesforce", hora_inicio, hora_fim, "Processamento Ok", "Diário")
