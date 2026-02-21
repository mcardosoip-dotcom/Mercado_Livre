# ================================================
# Orquestrador: backup, carga em stage, validação, ETL, limpeza e processo PBD
# Autor     : Marcelo Cardoso
# Data      : 2026-01-06
# ================================================

import os
import sys
import subprocess
from datetime import datetime

from config_processo import (
    CAMINHO_BASE,
    CAMINHO_STATUS_VALIDACAO,
    SCRIPT_FINAL_PBD,
    STEPS_PROCESSO_COMPLETO,
    PASTAS_PARA_LIMPAR_DESKTOP,
)


def _limpar_pastas(pastas):
    """Remove todos os arquivos (não subpastas) de cada pasta da lista."""
    for pasta in pastas:
        if not os.path.isdir(pasta):
            print(f"⚠️ Pasta não encontrada (ignorada): {pasta}")
            continue
        print(f"🔄 Limpando: {pasta}")
        for nome in os.listdir(pasta):
            caminho = os.path.join(pasta, nome)
            if os.path.isfile(caminho):
                try:
                    os.remove(caminho)
                    print(f"✅ Arquivo deletado: {nome}")
                except Exception as e:
                    print(f"❌ Erro ao deletar {nome}: {e}")
        print()


def _caminho_script(script_relativo):
    """Resolve caminho absoluto do script (relativo a CAMINHO_BASE ou ao diretório pai)."""
    if script_relativo.startswith(".."):
        return os.path.normpath(os.path.join(CAMINHO_BASE, script_relativo))
    return os.path.join(CAMINHO_BASE, script_relativo)


def _verificar_status_validacao():
    """Exige que o arquivo de status da validação exista e contenha OK."""
    if not os.path.exists(CAMINHO_STATUS_VALIDACAO):
        raise FileNotFoundError("Arquivo 'status_validacao.txt' não encontrado.")
    with open(CAMINHO_STATUS_VALIDACAO, "r", encoding="utf-8") as f:
        status = f.read().strip()
    if status.upper() != "OK":
        raise ValueError(f"Validação de colunas falhou (Status: {status}).")


def _executar_step(step):
    """Executa um step via subprocess e aplica checkpoint se definido."""
    script_rel = step["script"]
    caminho = _caminho_script(script_rel)
    nome = step["nome"]

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Script não encontrado: {caminho}")

    subprocess.run([sys.executable, "-u", caminho], check=True, cwd=os.path.dirname(caminho) or None)

    checkpoint = step.get("checkpoint")
    if checkpoint == "validacao":
        _verificar_status_validacao()
    # "etl_sucesso" é apenas sinalizado pelo orquestrador (flag sucesso_etl)


def main():
    print(f"\n🕒 Execução iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    erro_detectado = False
    sucesso_etl = False

    for step in STEPS_PROCESSO_COMPLETO:
        nome = step["nome"]
        script_rel = step["script"]

        if step.get("skip_in_loop"):
            print(f"\n➡️ [{nome}] Pulado no loop (executado ao final).")
            continue

        print(f"\n🔄 Executando: {nome} — {script_rel}")

        try:
            _executar_step(step)
            print(f"✅ Sucesso: {nome}")

            if step.get("checkpoint") == "etl_sucesso":
                sucesso_etl = True

        except subprocess.CalledProcessError as e:
            print(f"❌ ERRO CRÍTICO no step: {nome}\n   {e}")
            erro_detectado = True
            break
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ ERRO DE FLUXO em: {nome}\n   {e}")
            erro_detectado = True
            break

    # --- Bloco final: limpeza de desktop e script PBD ---
    print("=" * 60)

    if not erro_detectado and sucesso_etl:
        _limpar_pastas(PASTAS_PARA_LIMPAR_DESKTOP)

        print("\n🚀 Iniciando processo final (Legal Spend - Processo Completo Consolidado)...")
        print(f"📂 Alvo: {os.path.basename(SCRIPT_FINAL_PBD)}")

        try:
            subprocess.run([sys.executable, "-u", SCRIPT_FINAL_PBD], check=True)
            print("\n🏆 PROCESSO COMPLETO FINALIZADO COM SUCESSO! 🏆")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erro ao executar o processo final (Legal Spend - Consolidado):\n{e}")
    else:
        print("\n⚠️ O Processo Final (Legal Spend - Consolidado) NÃO foi executado.")
        if not sucesso_etl:
            print("   Motivo: O ETL principal não concluiu ou não foi alcançado.")
        if erro_detectado:
            print("   Motivo: Houve erro em um dos steps anteriores.")

    print(f"\n🕒 Fim da execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
