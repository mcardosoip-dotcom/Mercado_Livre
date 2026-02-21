"""
Script para definir o Google Chrome como navegador padrão no Windows.

No Windows 10/11 a Microsoft restringe a alteração programática do navegador padrão
(usa validação por hash no registro). Este script usa as opções disponíveis:

1. Abre as Configurações do Windows na página "Apps padrão" para você escolher o Chrome.
2. Opcional: se você tiver o SetDefaultBrowser.exe no mesmo diretório, tenta usá-lo.
"""

import subprocess
import sys
import os

# Caminhos comuns do Chrome no Windows
CHROME_PATHS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
]


def chrome_instalado():
    """Verifica se o Chrome está instalado."""
    for path in CHROME_PATHS:
        if path and os.path.isfile(path):
            return path
    return None


def abrir_configuracoes_padrao():
    """Abre as Configurações do Windows na página de Apps padrão."""
    try:
        subprocess.Popen(
            ["start", "ms-settings:defaultapps"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        print(f"Erro ao abrir Configurações: {e}")
        return False


def usar_setdefaultbrowser():
    """
    Tenta usar SetDefaultBrowser.exe se existir no mesmo diretório do script.
    Download: https://github.com/riverar/setdefaultbrowser (ou busque 'SetDefaultBrowser Windows')
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(script_dir, "SetDefaultBrowser.exe")
    if not os.path.isfile(exe_path):
        return False, "SetDefaultBrowser.exe não encontrado."
    try:
        # HKCU = usuário atual; "Chrome" ou "Google Chrome" conforme o identificador
        result = subprocess.run(
            [exe_path, "HKCU", "Chrome"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, "Chrome definido como padrão com SetDefaultBrowser."
        return False, result.stderr or result.stdout or "Erro ao executar SetDefaultBrowser."
    except subprocess.TimeoutExpired:
        return False, "SetDefaultBrowser demorou demais."
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 50)
    print("  Definir Chrome como navegador padrão")
    print("=" * 50)

    if not chrome_instalado():
        print("\nChrome não foi encontrado nos caminhos padrão.")
        print("Instale o Google Chrome e execute este script novamente.")
        sys.exit(1)

    print("\nChrome encontrado.")

    # 1) Tentar SetDefaultBrowser se existir
    ok, msg = usar_setdefaultbrowser()
    if ok:
        print(f"\n{msg}")
        sys.exit(0)

    # 2) Abrir Configurações do Windows
    print("\nAbrindo Configurações do Windows (Apps padrão)...")
    if abrir_configuracoes_padrao():
        print(
            "\nNa janela que abriu:\n"
            "  1. Clique em 'Google Chrome' (ou 'Navegador da Web').\n"
            "  2. Selecione 'Google Chrome' como padrão.\n"
        )
    else:
        print("Não foi possível abrir as Configurações.")
        sys.exit(1)

    if "SetDefaultBrowser" in msg:
        print("Dica: para definir o padrão automaticamente, coloque")
        print("SetDefaultBrowser.exe na mesma pasta deste script.")
    print()
    input("Pressione Enter para fechar...")


if __name__ == "__main__":
    main()
