import os
import subprocess
import sys # <--- NOVO: Importa o módulo 'sys'

# Caminho base onde estão os scripts
caminho_scripts = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\eLAW"

# Lista dos scripts a serem executados, na ordem
scripts = [
    "001 - Executa conversão em massa.py",
    "001.1 - Carga tratamento individual.py",
    "002 - Carga em Bucket.py"
]

# Executa cada script
for script in scripts:
    caminho_completo = os.path.join(caminho_scripts, script)
    print(f"\n🔄 Executando: {script}")
    try:
        # MELHORIA: Substituído "python" por sys.executable
        # Isso garante que o mesmo interpretador Python (e ambiente virtual) seja usado
        subprocess.run([sys.executable, caminho_completo], check=True)
        print(f"✅ Finalizado com sucesso: {script}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na execução de: {script}")
        print(f"Detalhes do Erro (Código {e.returncode}):")
        # Se os scripts printam mensagens de erro, elas aparecerão aqui:
        # print(e.stderr) 
        print(f"Comando falho: {e.cmd}")
        break  # Interrompe a sequência em caso de erro
    except FileNotFoundError:
        print(f"❌ Erro Crítico: O interpretador Python em '{sys.executable}' não foi encontrado.")
        print("Verifique seu ambiente ou altere o comando 'subprocess.run'.")
        break