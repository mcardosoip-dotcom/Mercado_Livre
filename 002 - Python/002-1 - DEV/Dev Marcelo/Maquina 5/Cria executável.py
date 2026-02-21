import os
import subprocess
import sys
import shutil

# ==========================================
# CONFIGURAÇÕES
# ==========================================
script_origem = r"Processo_M5.py"
pasta_destino = r"Executável"
nome_executavel = "Processo_M5"

# Caminhos absolutos
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_script = os.path.join(diretorio_atual, script_origem)
caminho_destino = os.path.join(diretorio_atual, pasta_destino)

# ==========================================
# VERIFICAÇÕES INICIAIS
# ==========================================
print("=" * 60)
print("CRIADOR DE EXECUTÁVEL - Processo_M5")
print("=" * 60)

if not os.path.exists(caminho_script):
    print(f"ERRO: Arquivo não encontrado: {caminho_script}")
    sys.exit(1)

print(f"Script origem: {caminho_script}")
print(f"Pasta destino: {caminho_destino}")

# Criar pasta de destino se não existir
os.makedirs(caminho_destino, exist_ok=True)

# ==========================================
# VERIFICAR SE PyInstaller ESTÁ INSTALADO
# ==========================================
print("\nVerificando PyInstaller...")
try:
    import PyInstaller
    print(f"PyInstaller encontrado (versão: {PyInstaller.__version__})")
except ImportError:
    print("PyInstaller não encontrado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("PyInstaller instalado com sucesso!")

# ==========================================
# LIMPAR BUILD ANTERIOR (OPCIONAL)
# ==========================================
print("\nLimpando builds anteriores...")
pastas_limpar = ["build", "dist", "__pycache__"]
for pasta in pastas_limpar:
    caminho_limpar = os.path.join(diretorio_atual, pasta)
    if os.path.exists(caminho_limpar):
        try:
            shutil.rmtree(caminho_limpar)
            print(f"Pasta removida: {pasta}")
        except Exception as e:
            print(f"Aviso: Não foi possível remover {pasta}: {e}")

# Remover .spec se existir
spec_file = os.path.join(diretorio_atual, f"{nome_executavel}.spec")
if os.path.exists(spec_file):
    try:
        os.remove(spec_file)
        print("Arquivo .spec removido")
    except Exception as e:
        print(f"Aviso: Não foi possível remover .spec: {e}")

# ==========================================
# COMANDO PyInstaller
# ==========================================
print("\n" + "=" * 60)
print("GERANDO EXECUTÁVEL...")
print("=" * 60)

# Opções do PyInstaller:
# --onefile: Cria um único arquivo executável
# --name: Nome do executável
# --distpath: Pasta onde será gerado o executável
# --workpath: Pasta temporária de trabalho
# --clean: Limpa cache antes de construir
# --noconsole: Remove a janela de console (use --console se quiser ver os prints)
# --console: Mantém a janela de console (para ver os prints do Processo_M5.py)
# --hidden-import: Importa módulos que podem não ser detectados automaticamente

comando = [
    sys.executable,
    "-m", "PyInstaller",
    "--onefile",  # Um único arquivo executável
    "--name", nome_executavel,
    "--distpath", caminho_destino,
    "--workpath", os.path.join(diretorio_atual, "build"),
    "--clean",  # Limpa cache
    "--console",  # Mantém console para ver os prints
    "--hidden-import", "pandas",
    "--hidden-import", "openpyxl",
    "--hidden-import", "xlsxwriter",
    "--hidden-import", "shutil",
    "--hidden-import", "subprocess",
    caminho_script
]

print(f"\nComando executado:")
print(" ".join(comando))
print()

# ==========================================
# EXECUTAR PyInstaller
# ==========================================
try:
    resultado = subprocess.run(
        comando,
        check=True,
        capture_output=True,
        text=True
    )
    
    print("=" * 60)
    print("EXECUTÁVEL CRIADO COM SUCESSO!")
    print("=" * 60)
    
    # Verificar se o executável foi criado
    extensao = ".exe" if sys.platform == "win32" else ""
    caminho_executavel = os.path.join(caminho_destino, f"{nome_executavel}{extensao}")
    
    if os.path.exists(caminho_executavel):
        tamanho_mb = os.path.getsize(caminho_executavel) / (1024 * 1024)
        print(f"\nExecutável criado:")
        print(f"  Local: {caminho_executavel}")
        print(f"  Tamanho: {tamanho_mb:.2f} MB")
        print(f"\nO executável está pronto para uso em qualquer máquina Windows!")
    else:
        print(f"\nAVISO: Executável não encontrado em: {caminho_executavel}")
        print("Verifique a pasta de destino para arquivos gerados.")
    
    # Mostrar saída do PyInstaller se houver
    if resultado.stdout:
        print("\n--- Saída do PyInstaller ---")
        print(resultado.stdout)
    
except subprocess.CalledProcessError as e:
    print("\n" + "=" * 60)
    print("ERRO AO CRIAR EXECUTÁVEL")
    print("=" * 60)
    print(f"Código de erro: {e.returncode}")
    if e.stdout:
        print("\n--- STDOUT ---")
        print(e.stdout)
    if e.stderr:
        print("\n--- STDERR ---")
        print(e.stderr)
    sys.exit(1)

except Exception as e:
    print(f"\nERRO INESPERADO: {e}")
    sys.exit(1)

# ==========================================
# LIMPEZA FINAL
# ==========================================
print("\n" + "=" * 60)
print("LIMPEZA FINAL")
print("=" * 60)

# Remover pastas temporárias
pastas_remover = ["build"]
for pasta in pastas_remover:
    caminho_remover = os.path.join(diretorio_atual, pasta)
    if os.path.exists(caminho_remover):
        try:
            shutil.rmtree(caminho_remover)
            print(f"Pasta temporária removida: {pasta}")
        except Exception as e:
            print(f"Aviso: Não foi possível remover {pasta}: {e}")

# Remover .spec
if os.path.exists(spec_file):
    try:
        os.remove(spec_file)
        print("Arquivo .spec removido")
    except Exception as e:
        print(f"Aviso: Não foi possível remover .spec: {e}")

print("\n" + "=" * 60)
print("PROCESSO FINALIZADO!")
print("=" * 60)
print(f"\nO executável está disponível em:")
print(f"  {caminho_executavel}")
print("\nVocê pode copiar este arquivo para qualquer máquina Windows e executá-lo diretamente!")
