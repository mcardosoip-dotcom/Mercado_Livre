import subprocess
import os

# Caminho base onde estão os scripts
base_path = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\Projeto Amélia"

# Scripts a serem executados, na ordem desejada
scripts = [
    "001 - Projeto Amélia - Tratamento de arquivo eLAW.py",
    "002 - Projeto Amélia - Conversão em CSV - Bucket.py",
    "003 - Projeto Amélia - Upload arquivos em Bucket.py"
]

total_scripts = len(scripts)
print(f"📌 Total de processos a executar: {total_scripts}\n")

# Executa cada script
for idx, script in enumerate(scripts, start=1):
    script_path = os.path.join(base_path, script)
    print(f"🔄 [{idx}/{total_scripts}] Executando: {script}")
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"✅ [{idx}/{total_scripts}] Finalizado com sucesso: {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ [{idx}/{total_scripts}] Erro na execução de: {script}")
        print(f"Detalhes: {e}\n")
        break

print("🏁 Processamento finalizado.")
