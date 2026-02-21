"""Configuração SFTP CLM (mesma do FileZilla). Ajuste host, usuário e chave aqui."""
import os
from pathlib import Path

# --- Dados da conexão (aba Geral do FileZilla) ---
SFTP_HOST = "sftpna11.springcm.com"
SFTP_PORT = 22
SFTP_USER = "ext_roomega@mercadolivre.com"

# Caminho da chave privada (igual ao "Arquivo com chave" do FileZilla)
# Usando chaves_rsa do projeto para não perder a chave se a pasta Temp for limpa
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chaves_rsa", "cliente_private_key.pem")

# Senha da chave privada (se a chave foi gerada com passphrase / -des3). Se não, deixe None.
PRIVATE_KEY_PASSPHRASE = None

# Pasta remota no servidor ('.' = raiz; altere se as bases estiverem em subpasta)
PASTA_REMOTA = "."


def get_private_key_path():
    """
    Retorna o caminho da chave privada usada na conexão.
    Usa PRIVATE_KEY_PATH se o arquivo existir; senão procura em %TEMP% e chaves_rsa.
    """
    if PRIVATE_KEY_PATH and os.path.exists(PRIVATE_KEY_PATH):
        return os.path.abspath(PRIVATE_KEY_PATH)
    diretorio_atual = Path(__file__).parent
    temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
    chaves_rsa_dir = diretorio_atual / "chaves_rsa"
    candidatos = [
        os.path.join(temp_dir, "cliente_private_key_temp.pem"),
        str(chaves_rsa_dir / "cliente_private_key.pem"),
    ]
    for path in candidatos:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None
