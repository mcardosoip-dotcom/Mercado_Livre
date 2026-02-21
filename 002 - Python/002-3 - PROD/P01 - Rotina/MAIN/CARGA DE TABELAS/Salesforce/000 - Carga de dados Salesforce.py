import os
import subprocess

# Caminho base onde estão os scripts
caminho_scripts = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Salesforce"

# Lista dos scripts a serem executados, na ordem
scripts = [
    "001 - Executa_conversão_em_massa.py",
    "002 - Carga_em_Bucket.py"
]

# Executa cada script
for script in scripts:
    caminho_completo = os.path.join(caminho_scripts, script)
    print(f"\n🔄 Executando: {script}")
    try:
        subprocess.run(["python", caminho_completo], check=True)
        print(f"✅ Finalizado com sucesso: {script}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na execução de: {script}")
        print(f"Detalhes: {e}")
        break  # Interrompe a sequência em caso de erro
