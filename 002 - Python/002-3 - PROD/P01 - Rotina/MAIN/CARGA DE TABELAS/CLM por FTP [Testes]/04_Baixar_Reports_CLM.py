"""
Baixa os 3 reports CLM via SFTP e salva em STAGE/CLM Database/YYYY-MM-DD.
Usa config_sftp e 03_Coleta_SFTP para a conexão.
"""
import sys
import os
from pathlib import Path
from datetime import date

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Permitir importar config e 03_Coleta_SFTP a partir desta pasta
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# Pasta base local (STAGE CLM Database)
BASE_LOCAL = Path(r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\CLM Database")

# Caminhos remotos no SFTP (pasta Data Analitics Legales)
REPORTS_REMOTOS = [
    "Mercado Libre S.R.L.- CLM/Admin/Run Reports/Data Analitics Legales/Control de contratos reporte.csv",
    "Mercado Libre S.R.L.- CLM/Admin/Run Reports/Data Analitics Legales/Metricas de contratos reporte.csv",
    "Mercado Libre S.R.L.- CLM/Admin/Run Reports/Data Analitics Legales/Metricas de flujos activos reporte.csv",
]


def main():
    import config_sftp as cfg
    import importlib.util
    spec = importlib.util.spec_from_file_location("coleta_sftp", _SCRIPT_DIR / "03_Coleta_SFTP.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    conectar_sftp = mod.conectar_sftp

    key_path = cfg.get_private_key_path()
    if not key_path:
        print("ERRO: Chave privada nao encontrada. Verifique config_sftp.py.")
        return 1

    print("Conectando ao SFTP CLM...")
    ssh, sftp, err = conectar_sftp(
        host=cfg.SFTP_HOST,
        port=cfg.SFTP_PORT,
        username=cfg.SFTP_USER,
        private_key_path=key_path,
        password=cfg.PRIVATE_KEY_PASSPHRASE,
    )
    if ssh is None or sftp is None:
        print("ERRO: Falha na conexao.", err or "")
        return 1

    hoje = date.today().strftime("%Y-%m-%d")
    pasta_destino = BASE_LOCAL / hoje
    pasta_destino.mkdir(parents=True, exist_ok=True)
    print(f"Pasta de destino: {pasta_destino}")

    ok = 0
    for caminho_remoto in REPORTS_REMOTOS:
        nome_arquivo = os.path.basename(caminho_remoto)
        caminho_local = pasta_destino / nome_arquivo
        try:
            sftp.get(caminho_remoto, str(caminho_local))
            print(f"  OK: {nome_arquivo}")
            ok += 1
        except Exception as e:
            print(f"  ERRO: {nome_arquivo} -> {e}")

    sftp.close()
    ssh.close()
    print(f"\nConcluido: {ok}/{len(REPORTS_REMOTOS)} arquivos em {pasta_destino}")
    return 0 if ok == len(REPORTS_REMOTOS) else 1


if __name__ == "__main__":
    sys.exit(main())
