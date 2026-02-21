# ================================================
# Descrição :  Depois dos arquivos devidamente baixados e os seus backups atualizados, 
#              os arquivos são movidos para a pasta final onde estão todas as tabelas 
#              que são usadas no processo
# Autor : Marcelo Cardoso
# ================================================

import os
import shutil
import logging
from datetime import datetime
from coda_processo_geral import inserir_dados

data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

def main():
    # Diretório e arquivo de log
    log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "LOG_Mover_arquivos_eLAW_para_pasta_final.log")

    # Configuração simples do logging com quebra de linha no formato
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s:\n%(message)s\n",  # quebra de linha antes e depois da mensagem
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.info("Início do script de cópia de arquivos.")

    source_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Arquivos tratados eLAW"
    dest_dir   = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões"
    os.makedirs(dest_dir, exist_ok=True)
    logging.info(f"Diretório de destino verificado: {dest_dir}")

    for file_name in os.listdir(source_dir):
        # Verifica se o arquivo possui a extensão .xlsx (independente de maiúsculas ou minúsculas)
        if not file_name.lower().endswith('.xlsx'):
            continue

        source_file = os.path.join(source_dir, file_name)
        if os.path.isfile(source_file):
            dest_file = os.path.join(dest_dir, file_name)
            try:
                shutil.copy2(source_file, dest_file)
                logging.info(f"Arquivo copiado: {source_file} -> {dest_file}")
            except Exception as e:
                logging.error(f"Erro ao copiar {source_file} para {dest_file}: {e}")

    logging.info("Fim do script.")

    hora_fim = datetime.now().strftime("%H:%M:%S")
    inserir_dados(data_atual, "Mover arquivos eLAW para pasta final", hora_inicio, hora_fim, "Processamento Ok", "Diário")

if __name__ == '__main__':
    main()
