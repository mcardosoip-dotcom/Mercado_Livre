"""
Processo completo CLM por FTP: conecta ao CLM e executa os steps 4, 5 e 6.
  Step 4: Baixa os 3 reports CSV do SFTP para STAGE/CLM Database/YYYY-MM-DD
  Step 5: Converte os CSVs em Parquet (CLM_DocuSign)
  Step 6: Envia os Parquets para o bucket GCS (prod e dev)
"""
import sys
import importlib.util
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def _run_module(script_name: str, entry_name: str = "main"):
    """Carrega e executa a função entry_name do script (ex.: main ou process_latest_files_to_parquet)."""
    path = BASE_DIR / script_name
    if not path.exists():
        print(f"ERRO: Script nao encontrado: {path}")
        return False
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", "").replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, entry_name, None)
    if fn is None:
        print(f"ERRO: Funcao '{entry_name}' nao encontrada em {script_name}")
        return False
    result = fn()
    if result is not None and result != 0:
        return False
    return True


def main():
    print("=" * 60)
    print("PROCESSO COMPLETO CLM POR FTP (Steps 4, 5, 6)")
    print("=" * 60)

    print("\n[Step 4] Baixando reports do SFTP...")
    if not _run_module("04_Baixar_Reports_CLM.py", "main"):
        print("\nProcesso interrompido: falha no Step 4.")
        return 1
    print("  Step 4 concluido.\n")

    print("[Step 5] Convertendo CSVs em Parquet...")
    if not _run_module("05_Conversao_em_parquet.py", "process_latest_files_to_parquet"):
        print("\nProcesso interrompido: falha no Step 5.")
        return 1
    print("  Step 5 concluido.\n")

    print("[Step 6] Enviando Parquets para o bucket GCS...")
    if not _run_module("06_Carga_em_Bucket.py", "main"):
        print("\nProcesso interrompido: falha no Step 6.")
        return 1
    print("  Step 6 concluido.\n")

    print("=" * 60)
    print("Processo completo concluido com sucesso.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
