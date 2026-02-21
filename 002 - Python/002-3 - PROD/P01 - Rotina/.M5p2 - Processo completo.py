# ================================================
# Orquestrador M5: ETL, Download Bucket, CODA Input e PBD (Arquivos tratados)
# Sem backup e sem limpeza de Desktop
# Autor     : Marcelo Cardoso
# Data      : 2026-01-06
# ================================================

import os
import sys
import subprocess
from datetime import datetime

from config_processo import CAMINHO_BASE, SCRIPT_FINAL_PBD_M5

# Steps do fluxo M5 (subset do processo completo)
STEPS_M5 = [
    {"nome": "ETL principal", "script": "004 - ETL de arquivos.py", "checkpoint": "etl_sucesso"},
    {"nome": "Download Bucket", "script": r"..\Download de banco\002 - Download Bucket.py"},
    {"nome": "CODA Input", "script": "CODA - Input.py"},
]


def _caminho_script(step):
    script = step["script"]
    return os.path.normpath(os.path.join(CAMINHO_BASE, script))


def main():
    print(f"\n🕒 Execução M5 iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    erro_detectado = False
    sucesso_etl = False

    for step in STEPS_M5:
        nome = step["nome"]
        caminho = _caminho_script(step)
        print(f"\n🔄 Executando: {nome}")

        try:
            subprocess.run([sys.executable, "-u", caminho], check=True, cwd=os.path.dirname(caminho) or None)
            print(f"✅ Sucesso: {nome}")
            if step.get("checkpoint") == "etl_sucesso":
                sucesso_etl = True
        except subprocess.CalledProcessError as e:
            print(f"❌ ERRO no step: {nome}\n   {e}")
            erro_detectado = True
            break

    print("=" * 60)

    if not erro_detectado and sucesso_etl:
        print("\n🚀 Iniciando processo final (PBD - Arquivos tratados)...")
        print(f"📂 Alvo: {os.path.basename(SCRIPT_FINAL_PBD_M5)}")
        try:
            subprocess.run([sys.executable, "-u", SCRIPT_FINAL_PBD_M5], check=True)
            print("\n🏆 PROCESSO M5 FINALIZADO COM SUCESSO! 🏆")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erro ao executar PBD:\n{e}")
    else:
        print("\n⚠️ O Processo Final (PBD) NÃO foi executado.")
        if not sucesso_etl:
            print("   Motivo: O ETL principal não concluiu.")
        if erro_detectado:
            print("   Motivo: Houve erro em um dos steps.")

    print(f"\n🕒 Fim da execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
