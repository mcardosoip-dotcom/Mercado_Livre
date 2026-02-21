# ================================================
# Descrição :  Este processo executa todos os steps anteriores. 
#              É importante garantir que todos estejam funcionando separadamente, 
#              pois a falha de um pode comprometer o fluxo completo
# Autor : Marcelo Cardoso
# ================================================


import os
import subprocess
from datetime import datetime

# Diretórios: pasta de códigos e de logs
DIR_CODIGOS = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\_Legado\Update de reports"
DIR_LOGS = os.path.join(DIR_CODIGOS, "LOGS do processo")
LOG_FILE = os.path.join(DIR_LOGS, "LOG_Processo_completo.txt")

# Script de processo Amélia (completo)
# SCRIPT_AMELIA_COMPLETO = r"G:\Drives compartilhados\Legales_Analytics\Projetos Python\Update de reports\Projeto Amélia\Amélia - Processo completo.py"

# Limpar o arquivo de log (modo 'w' sobrescreve  o conteúdo)
with open(LOG_FILE, "w") as log:
    log.write("Log Iniciado\n\n")

def log_message(mensagem):
    with open(LOG_FILE, "a") as log:
        log.write(mensagem + "\n")

def run_script(script):
    """Executa o script registrando os horários de início e término."""
    timestamp = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message(f"Iniciando '{script}' em {timestamp()}")
    subprocess.run(["python", script], check=True)
    log_message(f"Finalizando '{script}' em {timestamp()}\n")

# Muda o diretório de trabalho para a pasta de códigos
os.chdir(DIR_CODIGOS)

# === Execução do processo Amélia ===
# run_script(SCRIPT_AMELIA_COMPLETO)

# === Execução dos scripts principais ===
run_script("000-Limpeza de cash.py")
run_script("001-Tratamento de arquivos eLAW e Salesforce.py")
run_script("002 - Captura informações de download.py")
run_script("003 - Ajustar arquivos corrompidos eLAW.py")
run_script("004 - Renomear arquivos.py")
run_script("005 - Backup de arquivos eLAW.py")
run_script("006 - Backup de arquivos Salesforce.py")
run_script("007 - Mover arquivos eLAW para pasta final.py")
run_script("008 - Update de reports diarios.py")

# Executa o script semanal somente se for segunda-feira (weekday() == 0)
if datetime.today().weekday() == 0:
    run_script("009 - Update de reports semanais.py")
else:
    log_message("Dia não é segunda-feira. '009 - Update de reports semanais.py' não foi executado.")

# run_script("010 - Conversão em CSV - Bucket - Base Ativa.py")
# run_script("011 - Conversão em CSV - Bucket - Entradas e desfechos.py")
run_script("013 - Expurgo de histórico.py")
run_script("014 - Upload arquivos em Bucket.py")
#run_script("016 - Push de informações MySQL to Bucket")
