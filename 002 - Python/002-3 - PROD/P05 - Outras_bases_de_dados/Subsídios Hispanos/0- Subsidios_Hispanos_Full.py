import os
import subprocess
from datetime import datetime

# Diretório onde estão os scripts
DIR_CODIGOS = r"G:\Drives compartilhados\Legales_Analytics\Projetos Python\Base de dados\Subsídios Hispanos"

# Função que executa um script Python
def run_script(nome_script):
    caminho_script = os.path.join(DIR_CODIGOS, nome_script)
    print(f"▶️ Executando: {caminho_script}")
    subprocess.run(["python", caminho_script], check=True)

# Execução dos scripts na ordem desejada
run_script("1 - Subsidios_Hispanos_CAP.py")
run_script("2 - Subsidios_Hispanos_DR.py")
run_script("3- Subsídios_Hispanos_Geral.py")
#run_script("4 - Subsídios_Hispanos_Geral_Limpeza.py")
