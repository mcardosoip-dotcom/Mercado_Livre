import os
import subprocess
import sys

# O caminho base onde estão os scripts
# O caminho final dos scripts é:
# G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\CLM_DocuSign
caminho_base = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\CLM_DocuSign"

# Lista dos scripts a serem executados, na ordem
scripts = [
    "001 - Conversao em parquet.py",
    "002 - Carga em Bucket.py"
]

print("Iniciando a execução sequencial dos scripts Python...\n")

# Executa cada script
for script in scripts:
    caminho_completo = os.path.join(caminho_base, script)
    print(f"\n🔄 Executando: {script}")
    
    # Usamos sys.executable para garantir que o mesmo interpretador Python seja usado,
    # embora "python" no PATH geralmente funcione bem, este é mais robusto.
    comando = [sys.executable, caminho_completo]
    
    try:
        # Executa o script. 'check=True' garante que uma exceção seja levantada se 
        # o script retornar um código de erro diferente de zero.
        subprocess.run(comando, check=True)
        print(f"✅ Finalizado com sucesso: {script}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na execução de: {script}")
        print(f"Detalhes: O script retornou o código de erro: {e.returncode}")
        # Se quiser ver a saída de erro do script filho, pode descomentar:
        # if e.stderr:
        #     print(f"Saída de Erro (STDERR):\n{e.stderr.decode(sys.stderr.encoding)}")
        
        print("\n🚫 Interrompendo a sequência de execução.")
        break  # Interrompe a sequência em caso de erro

print("\nProcesso de execução sequencial CONCLUÍDO.")

# Exibir a pasta da rede de onde os arquivos foram coletados (mesma lógica do script de conversão)
SOURCE_DIR = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\CLM Database"
try:
    list_of_subdirs = [
        os.path.join(SOURCE_DIR, d)
        for d in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, d))
    ]
    if list_of_subdirs:
        pasta_coletada = max(list_of_subdirs, key=os.path.getmtime)
        print(f"\n📂 Pasta da rede de onde os arquivos foram coletados:\n   {pasta_coletada}")
    else:
        print(f"\n📂 Nenhuma subpasta encontrada em: {SOURCE_DIR}")
except Exception as e:
    print(f"\n📂 Não foi possível obter a pasta de origem: {e}")