import os
import sys
import subprocess

# Importa utilitário de caminhos cross-platform
from utils_caminhos import get_caminho_base_rotina

# Caminho base adaptado ao SO
CAMINHO_BASE = get_caminho_base_rotina()

# Lista dos caminhos relativos dos scripts a serem executados (cross-platform)
scripts_relativos = [
    os.path.join("MAIN", "CARGA DE TABELAS", "Salesforce", "000 - Carga de dados Salesforce.py"),
    os.path.join("MAIN", "CARGA DE TABELAS", "eLAW", "000 - Carga de dados eLAW.py"),
    os.path.join("DIM", "000 - Carga de dados dimensoes.py"),
    os.path.join("MAIN", "CARGA DE TABELAS", "Consumidor.gov", "000 - Carga de dados Gov.py"),
    os.path.join("MAIN", "CARGA DE TABELAS", "Quebra de sigilo", "000 - Carga de dados QS.py"),
    os.path.join("MAIN", "CARGA DE TABELAS", "Mesa de entrada", "000_Push_e_carga_mesa_de_entrada.py"),
    os.path.join("MAIN", "CARGA DE TABELAS", "eLAW", "002 - Carga em Bucket.py"),
    # NOVO SCRIPT ADICIONADO AQUI
    os.path.join("MAIN", "CARGA DE TABELAS", "CLM_DocuSign", "000 - Processo completo.py")
]

# Constrói caminhos absolutos a partir dos caminhos relativos
scripts = [os.path.normpath(os.path.join(CAMINHO_BASE, script_rel)) for script_rel in scripts_relativos]

for script in scripts:
    print(f"\n🔄 Executando: {script}")
    try:
        # Usa sys.executable para garantir que o mesmo interpretador Python seja usado
        # O 'check=True' garante que um erro no script Python levante uma exceção.
        subprocess.run([sys.executable, "-u", script], check=True, cwd=os.path.dirname(script) or None)
        print("✅ Execução concluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script}")
        print(f"Detalhes: {e}")