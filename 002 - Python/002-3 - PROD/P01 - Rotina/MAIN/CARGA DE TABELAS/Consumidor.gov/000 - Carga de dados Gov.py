import subprocess

# Lista dos caminhos completos dos scripts
scripts = [
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Consumidor.gov\002 - Criação de consolidado por ano.py",
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Consumidor.gov\003 - Criação de consolidado geral.py",
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Consumidor.gov\004 - Criação de arquivo parquet.py",
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\Consumidor.gov\005 - Carga em Bucket.py"
]

# Executa cada script em sequência
for script in scripts:
    print(f"\n▶️ Executando: {script}")
    try:
        subprocess.run(["python", script], check=True)
        print("✅ Concluído com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na execução de: {script}")
        print(e)
        break
