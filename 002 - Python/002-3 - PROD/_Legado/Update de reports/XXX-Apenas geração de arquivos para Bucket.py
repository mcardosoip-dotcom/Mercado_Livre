# ================================================
# Descrição :  Processo separado responsável pela carga de informações 
#              no ambiente do Mercado Livre
# Autor : Marcelo Cardoso
# ================================================

import os
import subprocess

# Diretório onde estão os scripts
DIR_CODIGOS = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports"

def run_script(script):
    """Executa o script sem registrar logs."""
    subprocess.run(["python", script], check=True)

# Muda o diretório de trabalho para a pasta de códigos
os.chdir(DIR_CODIGOS)

# Execução dos scripts
run_script("010 - Conversão em CSV - Bucket - Base Ativa.py")
run_script("011 - Conversão em CSV - Bucket - Entradas e desfechos.py")
run_script("012 - Conversão em CSV - Bucket - Pagamentos em garantia.py")
run_script("013 - Conversão em CSV - Bucket - Base Amélia.py")
run_script("014 - Expurgo de histórico.py")
run_script("015 - Upload arquivos em Bucket.py")
