import subprocess
import sys

# Caminhos completos para os scripts que você quer executar
# Use 'r' para strings cruas (raw strings) para evitar problemas com backslashes
script_tratamento_conversao = r"G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - CLM\001 - Tratemento e conversão em parquet.py"
script_carga_bucket = r"G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - CLM\001 - Tratemento e conversão em parquet.py"

print(f"Iniciando a execução de: {script_tratamento_conversao}")
subprocess.run([sys.executable, script_tratamento_conversao], check=True)

print(f"Iniciando a execução de: {script_carga_bucket}")
subprocess.run([sys.executable, script_carga_bucket], check=True)

print("\n🎉 Ambos os scripts foram executados.")