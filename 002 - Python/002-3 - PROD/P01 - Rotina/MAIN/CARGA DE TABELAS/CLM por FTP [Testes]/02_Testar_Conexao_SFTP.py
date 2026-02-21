"""Testa conexão SFTP CLM (Paramiko, chaves, config_sftp, servidor). Ver README.md."""

import subprocess
import sys
import os
import shutil
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ID do certificado retornado pelo CLM ao fazer upload da chave publica (atualize se enviar outra chave)
CLM_CERTIFICATE_ID = "4c042f9f-3c5a-4c1d-a943-480a903e7599"


def verificar_paramiko():
    """Verifica se paramiko está instalado."""
    print("\n" + "="*80)
    print("[1/7] VERIFICANDO PARAMIKO...")
    print("="*80)
    
    try:
        import paramiko
        print(f"[OK] Paramiko instalado (versao {paramiko.__version__})")
        return True
    except ImportError:
        print("[ERRO] Paramiko nao encontrado!")
        print("[INFO] Instalando Paramiko...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
            print("[OK] Paramiko instalado com sucesso!")
            return True
        except subprocess.CalledProcessError:
            print("[ERRO] Falha ao instalar Paramiko")
            return False


def verificar_openssl():
    """Verifica se OpenSSL está instalado."""
    print("\n" + "="*80)
    print("[2/7] VERIFICANDO OPENSSL...")
    print("="*80)
    
    openssl_path = shutil.which("openssl")
    if openssl_path:
        print(f"[OK] OpenSSL encontrado no PATH: {openssl_path}")
        return True, openssl_path
    
    default_paths = [
        r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe",
        r"C:\Program Files (x86)\OpenSSL-Win64\bin\openssl.exe",
        r"C:\OpenSSL-Win64\bin\openssl.exe",
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            print(f"[OK] OpenSSL encontrado: {path}")
            return True, path
    
    print("[ERRO] OpenSSL nao encontrado!")
    return False, None


def verificar_ou_gerar_chaves(openssl_path):
    """Verifica se as chaves existem. Para gerar novas chaves, use 01_Gerar_Chaves_e_Configurar.py."""
    print("\n" + "="*80)
    print("[3/7] VERIFICANDO CHAVES RSA...")
    print("="*80)
    
    # Verificar chaves no diretório temporário
    temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
    chave_privada_temp = os.path.join(temp_dir, "cliente_private_key_temp.pem")
    chave_publica_temp = os.path.join(temp_dir, "cliente_public_key_temp.pem")
    
    # Verificar chaves na pasta chaves_rsa
    diretorio_atual = Path(__file__).parent
    chaves_rsa_dir = diretorio_atual / "chaves_rsa"
    chave_privada_local = chaves_rsa_dir / "cliente_private_key.pem" if chaves_rsa_dir.exists() else None
    chave_publica_local = chaves_rsa_dir / "cliente_public_key.pem" if chaves_rsa_dir.exists() else None
    
    chave_privada = None
    chave_publica = None
    
    if os.path.exists(chave_privada_temp) and os.path.exists(chave_publica_temp):
        chave_privada = chave_privada_temp
        chave_publica = chave_publica_temp
        print(f"[OK] Chaves encontradas em: {temp_dir}")
    elif chave_privada_local and chave_privada_local.exists() and chave_publica_local and chave_publica_local.exists():
        chave_privada = str(chave_privada_local)
        chave_publica = str(chave_publica_local)
        print(f"[OK] Chaves encontradas em: {chaves_rsa_dir}")
    else:
        print("[ERRO] Chaves nao encontradas!")
        print("[INFO] Para gerar chaves, execute: python 01_Gerar_Chaves_e_Configurar.py")
        return None, None
    
    if chave_privada and os.path.exists(chave_privada):
        print(f"[OK] Chave Privada: {chave_privada}")
    else:
        print("[ERRO] Chave privada nao encontrada!")
        return None, None
    
    if chave_publica and os.path.exists(chave_publica):
        print(f"[OK] Chave Publica: {chave_publica}")
    else:
        print("[ERRO] Chave publica nao encontrada!")
        return None, None
    
    return chave_privada, chave_publica


def verificar_configuracao_script(chave_privada):
    """Verifica config_sftp.py (mesma config do FileZilla) e se a chave existe."""
    print("\n" + "="*80)
    print("[4/7] VERIFICANDO CONFIGURACAO (config_sftp.py)...")
    print("="*80)
    try:
        import config_sftp as cfg
    except ImportError:
        print("[ERRO] config_sftp.py nao encontrado na mesma pasta.")
        return False, None
    sftp_host = cfg.SFTP_HOST
    username = cfg.SFTP_USER
    private_key_path = cfg.get_private_key_path()
    private_key_password = cfg.PRIVATE_KEY_PASSPHRASE
    print(f"SFTP_HOST: {sftp_host}")
    print(f"USERNAME: {username}")
    print(f"PRIVATE_KEY_PATH: {private_key_path or '[NAO ENCONTRADA]'}")
    print(f"PRIVATE_KEY_PASSPHRASE: {'[CONFIGURADO]' if private_key_password else 'None'}")
    if not private_key_path:
        print("\n[ERRO] Chave privada nao encontrada. Use a mesma chave do FileZilla em %TEMP% ou chaves_rsa\\")
        return False, None
    print("\n[OK] Configuracao OK (mesma do FileZilla)")
    return True, {
        'SFTP_HOST': sftp_host,
        'USERNAME': username,
        'PRIVATE_KEY_PATH': private_key_path,
        'PRIVATE_KEY_PASSWORD': private_key_password,
    }


def testar_carregamento_chave(private_key_path, password=None):
    """Testa se a chave privada pode ser carregada (mesma funcao do 03_Coleta_SFTP)."""
    print("\n" + "="*80)
    print("[5/7] TESTANDO CARREGAMENTO DA CHAVE...")
    print("="*80)
    try:
        import importlib.util
        path_03 = Path(__file__).parent / "03_Coleta_SFTP.py"
        spec = importlib.util.spec_from_file_location("coleta_sftp", path_03)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not os.path.exists(private_key_path):
            print(f"[ERRO] Arquivo nao encontrado: {private_key_path}")
            return False
        mod.carregar_chave_privada(private_key_path, password=password)
        print("[OK] Chave privada carregada com sucesso!")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao carregar chave: {e}")
        return False


def fingerprint_chave_publica(caminho_publica):
    """Retorna fingerprint (MD5) da chave publica para comparacao com o CLM."""
    if not caminho_publica or not os.path.exists(caminho_publica):
        return None
    try:
        import hashlib
        with open(caminho_publica, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def mostrar_confronto_clm(caminho_publica):
    """Exibe confronto: ID do certificado no CLM vs fingerprint da chave gerada neste PC."""
    fp = fingerprint_chave_publica(caminho_publica)
    print("\n" + "="*80)
    print("CONFRONTO CLM x CHAVE GERADA (este PC)")
    print("="*80)
    print(f"  CLM retornou (ID do certificado): {CLM_CERTIFICATE_ID}")
    print(f"  Chave neste PC (arquivo):          {caminho_publica or '(nao encontrada)'}")
    print(f"  Fingerprint MD5 da chave local:   {fp or '(nao calculado)'}")
    print("  -> O certificado com esse ID no CLM deve ser o upload DESTE arquivo.")
    print("     Se o fingerprint mudar (ex.: apos rodar 01_Gerar_Chaves), faca upload de novo.")
    print("="*80)


def testar_conexao_sftp(config):
    """Testa a conexão SFTP usando a mesma função do 03_Coleta_SFTP (mesma lógica do FileZilla).
    Retorna (True, None) em sucesso ou (False, mensagem_erro) em falha."""
    print("\n" + "="*80)
    print("[6/7] TESTANDO CONEXAO SFTP (mesma conexao do 03_Coleta_SFTP / FileZilla)...")
    print("="*80)
    try:
        import importlib.util
        diretorio_script = Path(__file__).parent
        path_03 = diretorio_script / "03_Coleta_SFTP.py"
        spec = importlib.util.spec_from_file_location("coleta_sftp", path_03)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        conectar_sftp = mod.conectar_sftp
        ssh, sftp, err = conectar_sftp(
            host=config['SFTP_HOST'],
            port=22,
            username=config['USERNAME'],
            private_key_path=config['PRIVATE_KEY_PATH'],
            password=config.get('PRIVATE_KEY_PASSWORD'),
        )
        if ssh is None or sftp is None:
            print("[ERRO] Falha na conexao (mesma funcao que o 03_Coleta_SFTP).")
            if err:
                print(f"  Detalhe: {err}")
            return False, (err or "Conexao recusada")
        try:
            items = sftp.listdir_attr('.')
            print(f"\n[OK] Listagem de arquivos bem-sucedida! Total de itens: {len(items)}")
            if items:
                print("\n     Primeiros itens:")
                for item in items[:5]:
                    tipo = "[DIR]" if item.st_mode & 0o040000 else "[FILE]"
                    print(f"       {tipo} {item.filename}")
                if len(items) > 5:
                    print(f"       ... e mais {len(items) - 5} itens")
        except Exception as e:
            print(f"[AVISO] Nao foi possivel listar arquivos: {e}")
        sftp.close()
        ssh.close()
        print("\n[OK] Teste de conexao concluido com sucesso!")
        return True, None
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)


def main():
    print("="*80)
    print("TESTE COMPLETO - SFTP CLM.DS (02_Testar_Conexao_SFTP)")
    print("="*80)
    resultados = {'paramiko': False, 'openssl': False, 'chaves': False, 'configuracao': False, 'carregamento_chave': False, 'conexao': False}
    
    resultados['paramiko'] = verificar_paramiko()
    if not resultados['paramiko']:
        print("\n[ERRO] Teste interrompido: Paramiko necessario")
        return
    openssl_ok, openssl_path = verificar_openssl()
    resultados['openssl'] = openssl_ok
    chave_privada, chave_publica = verificar_ou_gerar_chaves(openssl_path)
    resultados['chaves'] = chave_privada is not None and chave_publica is not None
    if not resultados['chaves']:
        print("\n[ERRO] Teste interrompido: Chaves necessarias")
        return
    mostrar_confronto_clm(chave_publica)
    config_ok, config = verificar_configuracao_script(chave_privada)
    resultados['configuracao'] = config_ok
    if not config_ok or not config:
        print("\n[ERRO] Teste interrompido: Configuracao incompleta")
        print("[INFO] Execute: python '01_Gerar_Chaves_e_Configurar.py'")
        return
    resultados['carregamento_chave'] = testar_carregamento_chave(config['PRIVATE_KEY_PATH'], config['PRIVATE_KEY_PASSWORD'])
    if not resultados['carregamento_chave']:
        print("\n[ERRO] Teste interrompido: Chave nao pode ser carregada")
        return
    resultados['conexao'], erro_conexao = testar_conexao_sftp(config)
    
    print("\n" + "="*80)
    print("[7/7] RESUMO DOS TESTES")
    print("="*80)
    print(f"\n[{'OK' if resultados['paramiko'] else 'ERRO'}] Paramiko")
    print(f"[{'OK' if resultados['openssl'] else 'AVISO'}] OpenSSL")
    print(f"[{'OK' if resultados['chaves'] else 'ERRO'}] Chaves RSA")
    print(f"[{'OK' if resultados['configuracao'] else 'ERRO'}] Configuracao do Script")
    print(f"[{'OK' if resultados['carregamento_chave'] else 'ERRO'}] Carregamento da Chave")
    print(f"[{'OK' if resultados['conexao'] else 'ERRO'}] Conexao SFTP")
    
    if all([resultados['paramiko'], resultados['chaves'], resultados['configuracao'], resultados['carregamento_chave'], resultados['conexao']]):
        print("\n[OK] TODOS OS TESTES PASSARAM!")
        print("\n[INFO] Voce pode usar o script principal: python '03_Coleta_SFTP.py'")
    else:
        print("\n[ERRO] ALGUNS TESTES FALHARAM")
        if not resultados['conexao'] and erro_conexao:
            print(f"\n[INFO] Erro da conexao: {erro_conexao}")
            fp = fingerprint_chave_publica(chave_publica)
            print("\n[INFO] Se a conexao falhou por autenticacao:")
            print(f"  1. Chave publica usada neste PC: {chave_publica}")
            if fp:
                print(f"     Fingerprint (MD5) desta chave: {fp}")
            print("  2. No CLM: User Icon -> Manage Profile -> Privacy and Security -> Certificates")
            print("  3. A chave no CLM deve ser a MESMA que voce fez upload.")
            print("     Se voce rodou 01_Gerar_Chaves DEPOIS do upload, a chave em Temp mudou -> faca upload de novo.")
            print("  4. Confirme que o SFTP esta habilitado (CLM Admin -> Integrations -> System Domains).")
    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ERRO] Teste cancelado pelo usuario.")
    except Exception as e:
        print(f"\n[ERRO] ERRO inesperado: {e}")
        import traceback
        traceback.print_exc()
