import subprocess
import os
from datetime import datetime

SCRIPT_1 = "/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics/002 - Python/002-3 - PROD/P01 - Rotina/MAIN/CARGA DE TABELAS/Mesa de entrada/Apenas_Exec_MAC/001 - Download.py"
SCRIPT_2 = "/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics/002 - Python/002-3 - PROD/P01 - Rotina/MAIN/CARGA DE TABELAS/Mesa de entrada/Apenas_Exec_MAC/002 - Carga_Bucket.py"

PYTHON_BIN = "/usr/local/bin/python3.14"

def verificar_script(script_path):
    return os.path.exists(script_path) and os.access(script_path, os.R_OK)

def rodar(script):
    script_name = os.path.basename(script)

    if not verificar_script(script):
        print(f"❌ ERRO: Script não encontrado ou sem permissão: {script_name}")
        return False

    print(f"\n{'='*60}")
    print(f"▶ Executando: {script_name}")
    print(f"{'='*60}")

    try:
        process = subprocess.Popen(
            [PYTHON_BIN, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Captura output mas não imprime todas as linhas para reduzir ruído
        output_lines = []
        for line in process.stdout:
            output_lines.append(line.rstrip())
            # Mostra apenas linhas importantes (erros, warnings, ou mensagens específicas)
            if any(keyword in line.upper() for keyword in ['ERRO', 'ERROR', 'FALHA', 'WARNING', 'SUCESSO', 'CONCLUÍDO']):
                print(f"  → {line.rstrip()}")

        process.wait()

        if process.returncode != 0:
            print(f"\n❌ ERRO: {script_name} falhou (código: {process.returncode})")
            # Mostra últimas linhas do output em caso de erro
            if output_lines:
                print(f"\nÚltimas linhas do log:")
                for line in output_lines[-5:]:
                    print(f"  {line}")
            return False

        print(f"✓ {script_name} concluído com sucesso")
        return True

    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {script_name} excedeu o tempo limite")
        return False
    except Exception as e:
        print(f"❌ FALHA: {script_name} | Erro: {e}")
        return False

if __name__ == "__main__":
    inicio_total = datetime.now()
    
    print("\n" + "="*60)
    print("🚀 INICIANDO PIPELINE DE CARGA")
    print("="*60)
    print(f"Início: {inicio_total.strftime('%Y-%m-%d %H:%M:%S')}\n")

    resultados = []

    sucesso_1 = rodar(SCRIPT_1)
    resultados.append(("001 - Download.py", sucesso_1))

    if sucesso_1:
        sucesso_2 = rodar(SCRIPT_2)
        resultados.append(("002 - Carga_Bucket.py", sucesso_2))
    else:
        print(f"\n⚠️  Pulando {os.path.basename(SCRIPT_2)} devido a falha anterior")
        resultados.append(("002 - Carga_Bucket.py", False))

    fim_total = datetime.now()
    duracao_total = fim_total - inicio_total

    print("\n" + "="*60)
    print("📊 RESUMO DA EXECUÇÃO")
    print("="*60)
    print(f"Fim: {fim_total.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duração total: {duracao_total}")
    print("\nResultados:")
    
    for nome, sucesso in resultados:
        status = "✓ SUCESSO" if sucesso else "❌ FALHA"
        print(f"  {status} - {nome}")
    
    print("="*60 + "\n")
