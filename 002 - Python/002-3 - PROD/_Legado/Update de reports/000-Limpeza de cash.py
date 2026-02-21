# ================================================
# Descrição :  Rodamos esse processo para garantir que o código funcione normalmente. 
#              Às vezes ele apresenta problemas relacionados ao cache, e esse processo 
#              libera o cache para que a execução ocorra sem falhas.
# Autor : Marcelo Cardoso
# ================================================

import os
import shutil
import time
from datetime import datetime
from coda_processo_geral import inserir_dados

# Obtém a data atual e o horário de início
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Limpa o cache gerado do win32com
gen_py = os.path.join(os.environ["LOCALAPPDATA"], "Temp", "gen_py")
if os.path.exists(gen_py):
    shutil.rmtree(gen_py)
    print("Cache win32com removido com sucesso. Será regenerado na próxima execução.")
else:
    print("Cache win32com não encontrado.")


# Registro do horário de término e inserção dos dados de log
hora_fim = datetime.now().strftime("%H:%M:%S")
inserir_dados(data_atual, "Limpeza de cash", hora_inicio, hora_fim, "Processamento Ok", "Diário")
