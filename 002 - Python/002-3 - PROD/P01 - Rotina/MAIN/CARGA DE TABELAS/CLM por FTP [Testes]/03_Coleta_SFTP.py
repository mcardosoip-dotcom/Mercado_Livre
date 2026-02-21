"""Conexão SFTP CLM (DocuSign/SpringCM). Usa config_sftp.py. Ver README.md."""

import paramiko
import os
from pathlib import Path


def _resolver_caminho_chave(caminho_informado):
    """
    Resolve o caminho da chave: expande %TEMP%, verifica se existe.
    Se não existir no caminho informado, tenta Temp e chaves_rsa (como no 02_Testar e no FileZilla).
    Aceita .pem e .ppk (PuTTY/FileZilla).
    Retorna o caminho absoluto do arquivo encontrado ou None.
    """
    path = os.path.expandvars(os.path.expanduser(caminho_informado))
    if os.path.exists(path):
        return os.path.abspath(path)
    diretorio_atual = Path(__file__).parent
    temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
    chaves_rsa_dir = diretorio_atual / "chaves_rsa"
    # Tentar mesmos nomes em Temp e em chaves_rsa (com .pem e .ppk)
    for base, nome in [
        (temp_dir, "cliente_private_key_temp.pem"),
        (temp_dir, "cliente_private_key_temp.ppk"),
        (chaves_rsa_dir, "cliente_private_key.pem"),
        (chaves_rsa_dir, "cliente_private_key.ppk"),
    ]:
        p = os.path.join(base, nome) if isinstance(base, str) else base / nome
        if os.path.exists(p):
            return os.path.abspath(str(p))
    return None


def _carregar_chave_privada(private_key_path, password=None):
    """
    Carrega chave privada em formato PEM (OpenSSL).
    O Paramiko não suporta .ppk (PuTTY/FileZilla); use o mesmo arquivo .pem ou converta PPK em PuTTYgen.
    Retorna objeto de chave para paramiko ou levanta exceção.
    """
    path = os.path.abspath(os.path.expandvars(os.path.expanduser(private_key_path)))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    nome = os.path.basename(path).lower()
    if nome.endswith(".ppk"):
        raise ValueError(
            "Arquivo .ppk (PuTTY/FileZilla): o Paramiko não suporta PPK. "
            "No FileZilla use o mesmo arquivo .pem que o script, ou converta o PPK em PuTTYgen: Conversions → Export OpenSSH key."
        )
    # Formato PEM
    try:
        if password is not None:
            return paramiko.RSAKey.from_private_key_file(path, password=password)
        return paramiko.RSAKey.from_private_key_file(path)
    except paramiko.ssh_exception.SSHException:
        pass
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        with open(path, 'rb') as f:
            key_data = f.read()
        private_key_obj = serialization.load_pem_private_key(
            key_data, password=password, backend=default_backend()
        )
        private_key = paramiko.RSAKey(
            data=private_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
        return private_key
    except Exception as e:
        raise ValueError(f"Não foi possível carregar a chave PEM: {e}") from e


def carregar_chave_privada(private_key_path, password=None):
    """Carrega a chave privada (mesma lógica do FileZilla). Para uso pelo 02_Testar e outros."""
    return _carregar_chave_privada(private_key_path, password=password)


def _conectar_ssh(ssh, host, port, username, private_key, disabled_algorithms=None):
    """Abre conexão SSH com os parâmetros dados."""
    kwargs = dict(
        hostname=host,
        port=port,
        username=username,
        pkey=private_key,
        timeout=30,
        allow_agent=False,
        look_for_keys=False,
    )
    if disabled_algorithms is not None:
        kwargs["disabled_algorithms"] = disabled_algorithms
    ssh.connect(**kwargs)


def conectar_sftp(host, username, private_key_path, port=22, password=None):
    """Conecta ao servidor SFTP usando chave privada (PEM ou PPK, como no FileZilla)."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        path_resolvido = _resolver_caminho_chave(private_key_path)
        if path_resolvido is None:
            msg = f"Arquivo de chave não encontrado: {private_key_path}"
            print(f"ERRO: {msg}")
            print("  Procurado também em: %%TEMP%%\\cliente_private_key_temp.pem e chaves_rsa\\cliente_private_key.pem")
            return None, None, msg
        private_key_path = path_resolvido
        print(f"Usando chave: {private_key_path}")
        try:
            private_key = _carregar_chave_privada(private_key_path, password=password)
        except Exception as e:
            msg = str(e)
            print(f"ERRO ao carregar chave: {e}")
            print("  - Se a chave tem senha, configure PRIVATE_KEY_PASSPHRASE em config_sftp.py.")
            return None, None, msg
        print(f"Conectando ao servidor {host}:{port}...")
        # SpringCM/DocuSign: forçar ssh-rsa (igual ao FileZilla; servidor pode não aceitar rsa-sha2-*)
        disabled_algos = {"pubkeys": ["rsa-sha2-512", "rsa-sha2-256"]}
        _conectar_ssh(ssh, host, port, username, private_key, disabled_algos)
        sftp = ssh.open_sftp()
        print("Conexão estabelecida com sucesso!")
        return ssh, sftp, None
    except paramiko.AuthenticationException as e:
        msg = f"Falha na autenticação: {e}"
        print("ERRO:", msg)
        print("  Verifique: chave pública no DocuSign, usuário correto, senha da chave (se tiver).")
        return None, None, msg
    except paramiko.SSHException as e:
        msg = str(e)
        print(f"ERRO na conexão SSH: {e}")
        return None, None, msg
    except Exception as e:
        msg = str(e)
        print(f"ERRO inesperado: {e}")
        import traceback
        traceback.print_exc()
        return None, None, msg


def listar_arquivos(sftp, caminho='.'):
    """Lista arquivos e diretórios no servidor SFTP."""
    try:
        print(f"\nConteúdo do diretório: {caminho}")
        print("-" * 80)
        
        items = sftp.listdir_attr(caminho)
        
        arquivos = []
        diretorios = []
        
        for item in items:
            nome = item.filename
            if item.st_mode & 0o040000:
                diretorios.append(nome)
            else:
                arquivos.append((nome, item.st_size))
        
        if diretorios:
            print("\nDIRETÓRIOS:")
            for dir_name in sorted(diretorios):
                print(f"  [DIR] {dir_name}/")
        
        if arquivos:
            print("\nARQUIVOS:")
            for nome, tamanho in sorted(arquivos, key=lambda x: x[0]):
                tamanho_mb = tamanho / (1024 * 1024) if tamanho > 0 else 0
                print(f"  [FILE] {nome:<50} {tamanho_mb:>10.2f} MB")
        
        print("-" * 80)
        print(f"\nTotal: {len(diretorios)} diretório(s) e {len(arquivos)} arquivo(s)")
        
        return diretorios, arquivos
    
    except Exception as e:
        print(f"ERRO ao listar arquivos: {e}")
        return [], []


def mostrar_instrucoes_geracao_chaves():
    """Mostra instruções resumidas para gerar chaves RSA."""
    print("\n" + "="*80)
    print("GERAR CHAVES RSA:")
    print("="*80)
    print("1. Baixar OpenSSL: https://slproweb.com/products/Win32OpenSSL.html")
    print("2. Abrir Command Prompt como Administrador")
    print("3. cd C:\\Program Files\\OpenSSL-Win64\\bin")
    print("4. openssl genrsa -des3 -out cliente_private_key.pem 2048")
    print("5. openssl rsa -in cliente_private_key.pem -outform PEM -pubout -out cliente_public_key.pem")
    print("6. Upload da chave pública no DocuSign: User Icon → Manage Profile → Privacy and Security → Certificates")
    print("="*80 + "\n")


def mostrar_instrucoes_sftp_host():
    """Mostra instruções para obter o SFTP domain."""
    print("\n" + "="*80)
    print("OBTER SFTP DOMAIN:")
    print("="*80)
    print("DocuSign → CLM → Admin → System Domains → copie o 'SFTP domain'")
    print("Formato típico: sftp-XXXXX.docusign.com")
    print("="*80 + "\n")


def main():
    """Função principal – usa a mesma configuração do FileZilla (config_sftp.py)."""
    try:
        import config_sftp as cfg
    except ImportError:
        print("ERRO: Arquivo config_sftp.py não encontrado na mesma pasta.")
        return

    SFTP_HOST = cfg.SFTP_HOST
    USERNAME = cfg.SFTP_USER
    PORT = cfg.SFTP_PORT
    PRIVATE_KEY_PASSWORD = cfg.PRIVATE_KEY_PASSPHRASE
    PASTA_REMOTA = cfg.PASTA_REMOTA
    PRIVATE_KEY_PATH = cfg.get_private_key_path()

    if not PRIVATE_KEY_PATH:
        print("ERRO: Chave privada não encontrada.")
        print("  Procurado em: %TEMP%\\cliente_private_key_temp.pem e chaves_rsa\\cliente_private_key.pem")
        print("  Use o mesmo arquivo de chave que está no FileZilla (Arquivo com chave).")
        mostrar_instrucoes_geracao_chaves()
        return

    print("=" * 80)
    print("CONEXÃO SFTP - CLM.DS (mesma config do FileZilla)")
    print("=" * 80)

    ssh, sftp, err = conectar_sftp(
        host=SFTP_HOST,
        username=USERNAME,
        private_key_path=PRIVATE_KEY_PATH,
        port=PORT,
        password=PRIVATE_KEY_PASSWORD,
    )

    if ssh is None or sftp is None:
        if err:
            print(f"\nFalha: {err}")
        print("Verifique config_sftp.py (Host, usuário, chave) e tente novamente.")
        return

    try:
        listar_arquivos(sftp, PASTA_REMOTA)
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
        print("\nConexão encerrada.")


if __name__ == "__main__":
    main()
