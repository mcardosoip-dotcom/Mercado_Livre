# ================================================
# Descrição: Inclusão de nome de arquivos e data de atualização 
#            em site de controle CODA
# Autor: Marcelo Cardoso
# ================================================

import os
import time
from datetime import datetime
from coda_update_de_bases import inserir_dados_2

# Diretório dos arquivos (sem filtro de extensão)
diretorio_stage = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"

# Percorre todos os arquivos no diretório
for arquivo in os.listdir(diretorio_stage):
    # Constrói o caminho completo para o arquivo
    caminho = os.path.join(diretorio_stage, arquivo)
    
    # Verifica se o caminho é realmente um arquivo e não uma pasta
    if os.path.isfile(caminho):
        data_update = datetime.fromtimestamp(os.path.getmtime(caminho))
        nome_base = os.path.splitext(arquivo)[0]
        inserir_dados_2(nome_base, data_update.isoformat())
        time.sleep(5)  # Aguarda 5 segundos entre as requisições