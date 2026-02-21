"""Gera par de chaves RSA e atualiza config_sftp. Só quando precisar de chave nova. Ver README.md."""
import subprocess
import sys
import os
import re
import shutil
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

USERNAME_CLM = "ext_roomega@mercadolivre.com"
SCRIPT_COLETA = "03_Coleta_SFTP.py"
SCRIPT_TESTE = "02_Testar_Conexao_SFTP.py"

def encontrar_openssl():
    p = shutil.which("openssl")
    if p:
        return p
    for path in [
        r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe",
        r"C:\Program Files (x86)\OpenSSL-Win64\bin\openssl.exe",
        r"C:\OpenSSL-Win64\bin\openssl.exe",
    ]:
        if os.path.exists(path):
            return path
    return None


def validar_par_chaves(chave_privada, chave_publica):
    """
    Valida se a chave publica corresponde à chave privada (par consistente).
    Retorna (True, None) se OK, ou (False, mensagem_erro).
    """
    if not os.path.exists(chave_privada):
        return False, f"Arquivo nao encontrado: {chave_privada}"
    if not os.path.exists(chave_publica):
        return False, f"Arquivo nao encontrado: {chave_publica}"

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.backends import default_backend

        with open(chave_privada, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
        with open(chave_publica, "rb") as f:
            public_key = load_pem_public_key(f.read(), backend=default_backend())

        # A chave publica derivada da privada deve ser igual à do arquivo
        public_from_private = private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        public_file_bytes = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        if public_from_private != public_file_bytes:
            return False, "A chave publica do arquivo NAO corresponde à chave privada (par invalido)."
        return True, None
    except ImportError:
        # Fallback: usar OpenSSL para derivar publica da privada e comparar arquivos
        openssl_path = encontrar_openssl()
        if not openssl_path:
            return False, "Biblioteca cryptography nao encontrada e OpenSSL indisponivel."
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            subprocess.run(
                [openssl_path, "rsa", "-in", chave_privada, "-pubout", "-out", tmp_path],
                check=True, capture_output=True
            )
            with open(tmp_path, "rb") as f:
                derived = f.read()
            with open(chave_publica, "rb") as f:
                arquivo = f.read()
            # Normalizar quebras de linha para comparar
            if derived.replace(b"\r\n", b"\n").strip() != arquivo.replace(b"\r\n", b"\n").strip():
                return False, "A chave publica do arquivo NAO corresponde à chave privada (par invalido)."
            return True, None
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except Exception as e:
        return False, f"Erro ao validar: {e}"


def main():
    base = Path(__file__).parent
    arquivo_principal = base / SCRIPT_COLETA

    print("=" * 60)
    print("GERAR CHAVES E CONFIGURAR TUDO (ext_roomega@mercadolivre.com)")
    print("=" * 60)

    openssl_path = encontrar_openssl()
    if not openssl_path:
        print("[ERRO] OpenSSL nao encontrado. Instale OpenSSL e tente novamente.")
        return 1

    temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
    chaves_rsa_dir = base / "chaves_rsa"
    chaves_rsa_dir.mkdir(exist_ok=True)

    chave_privada_temp = os.path.join(temp_dir, "cliente_private_key_temp.pem")
    chave_publica_temp = os.path.join(temp_dir, "cliente_public_key_temp.pem")
    chave_privada_local = chaves_rsa_dir / "cliente_private_key.pem"
    chave_publica_local = chaves_rsa_dir / "cliente_public_key.pem"

    # Gerar em Temp primeiro
    print("\n[1] Gerando novas chaves RSA em:", temp_dir)
    try:
        subprocess.run(
            [openssl_path, "genrsa", "-traditional", "-out", chave_privada_temp, "2048"],
            check=True, capture_output=True
        )
        subprocess.run(
            [openssl_path, "rsa", "-in", chave_privada_temp, "-outform", "PEM", "-pubout", "-out", chave_publica_temp],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print("[ERRO] Falha ao gerar chaves:", e.stderr.decode(errors="replace") if e.stderr else e)
        return 1
    print("[OK] Chaves geradas.")

    # Copiar para chaves_rsa (backup persistente)
    shutil.copy2(chave_privada_temp, chave_privada_local)
    shutil.copy2(chave_publica_temp, chave_publica_local)
    print(f"[OK] Copia salva em: {chaves_rsa_dir}")

    chave_privada = chave_privada_temp
    chave_publica = chave_publica_temp

    print("\n[1b] Validando par de chaves (privada x publica)...")
    ok, err = validar_par_chaves(chave_privada, chave_publica)
    if not ok:
        print("[ERRO] Validacao falhou:", err)
        return 1
    print("[OK] Par de chaves valido: a chave publica corresponde à chave privada.")

    config_sftp = base / "config_sftp.py"
    if config_sftp.exists():
        print("\n[2] Atualizando config_sftp.py (mesma config do FileZilla)...")
        with open(config_sftp, "r", encoding="utf-8") as f:
            conteudo = f.read()
        conteudo = re.sub(
            r'SFTP_USER\s*=\s*["\'][^"\']+["\']',
            f'SFTP_USER = "{USERNAME_CLM}"',
            conteudo
        )
        with open(config_sftp, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("[OK] SFTP_USER atualizado em config_sftp.py. A chave e encontrada em %TEMP% e chaves_rsa.")
    else:
        print("\n[AVISO] config_sftp.py nao encontrado; configure manualmente Host/Usuario em config_sftp.py.")

    print("\n" + "=" * 60)
    print("PRÓXIMO PASSO (obrigatório):")
    print("=" * 60)
    print("1. Abra o DocuSign e faca login com o usuario:", USERNAME_CLM)
    print("2. Va em: User Icon -> Manage Profile -> Privacy and Security -> Certificates")
    print("3. Clique em 'Add Public Key' e faca upload deste arquivo:")
    print("   ", chave_publica)
    print("   (ou a copia em:", chave_publica_local, ")")
    print("4. Depois execute para testar a conexao:")
    print(f'   python "{SCRIPT_TESTE}"')
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
