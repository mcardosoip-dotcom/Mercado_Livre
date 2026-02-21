# ============================================================
# GERADOR DE EXECUTÁVEL - UPLOAD SALESFORCE
# ============================================================
# Descrição: Script para gerar executável do processo Upload Salesforce
#            Usa PyInstaller para criar um .exe portável
# Autor: Gerado automaticamente
# ============================================================

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Caminho do script principal
SCRIPT_PRINCIPAL = r"000 - Upload_Salesforce.py"

# Pasta onde o executável será salvo
PASTA_EXECUTAVEL = r"Executável"

# Nome do executável final
NOME_EXECUTAVEL = "Upload_Salesforce"

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado."""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não encontrado")
        print("   Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar PyInstaller")
            return False

def limpar_builds_anteriores():
    """Remove pastas de build anteriores do PyInstaller."""
    pastas_limpar = ["build", "dist", "__pycache__"]
    arquivos_limpar = [f"{NOME_EXECUTAVEL}.spec"]
    
    print("\n🧹 Limpando builds anteriores...")
    
    for pasta in pastas_limpar:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"   ✓ Removida: {pasta}")
            except Exception as e:
                print(f"   ⚠ Erro ao remover {pasta}: {e}")
    
    for arquivo in arquivos_limpar:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"   ✓ Removido: {arquivo}")
            except Exception as e:
                print(f"   ⚠ Erro ao remover {arquivo}: {e}")

def criar_executavel():
    """Cria o executável usando PyInstaller."""
    print("\n" + "="*60)
    print("GERANDO EXECUTÁVEL")
    print("="*60)
    
    # Obtém o diretório atual (onde está este script)
    diretorio_atual = Path(__file__).parent.absolute()
    caminho_script = diretorio_atual / SCRIPT_PRINCIPAL
    caminho_destino = diretorio_atual / PASTA_EXECUTAVEL
    
    # Verifica se o script principal existe
    if not caminho_script.exists():
        print(f"❌ ERRO: Script principal não encontrado: {caminho_script}")
        return False
    
    # Cria a pasta de destino se não existir
    caminho_destino.mkdir(exist_ok=True)
    
    # Comando PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",                    # Cria um único arquivo executável
        "--console",                    # Mantém console visível (para ver logs)
        "--name", NOME_EXECUTAVEL,      # Nome do executável
        "--distpath", str(caminho_destino),  # Pasta de destino
        "--workpath", str(diretorio_atual / "build"),  # Pasta temporária de build
        "--specpath", str(diretorio_atual),   # Onde salvar o .spec
        "--clean",                      # Limpa cache antes de construir
        "--noconfirm",                  # Não pede confirmação
        str(caminho_script)             # Script a ser compilado
    ]
    
    print(f"\n📝 Script principal: {caminho_script}")
    print(f"📂 Destino: {caminho_destino}")
    print(f"🔧 Comando: {' '.join(comando)}\n")
    
    try:
        # Executa PyInstaller
        resultado = subprocess.run(
            comando,
            check=True,
            cwd=str(diretorio_atual)
        )
        
        # Verifica se o executável foi criado
        executavel_criado = caminho_destino / f"{NOME_EXECUTAVEL}.exe"
        if executavel_criado.exists():
            tamanho_mb = executavel_criado.stat().st_size / (1024 * 1024)
            print("\n" + "="*60)
            print("✅ EXECUTÁVEL CRIADO COM SUCESSO!")
            print("="*60)
            print(f"📦 Arquivo: {executavel_criado}")
            print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
            print(f"\n💡 O executável está pronto para uso em qualquer notebook Windows!")
            return True
        else:
            print("❌ ERRO: Executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERRO ao executar PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")
        return False

def limpar_arquivos_temporarios():
    """Remove arquivos temporários após a criação do executável."""
    print("\n🧹 Limpando arquivos temporários...")
    
    pastas_limpar = ["build"]
    arquivos_limpar = [f"{NOME_EXECUTAVEL}.spec"]
    
    for pasta in pastas_limpar:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"   ✓ Removida: {pasta}")
            except Exception as e:
                print(f"   ⚠ Erro ao remover {pasta}: {e}")
    
    for arquivo in arquivos_limpar:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"   ✓ Removido: {arquivo}")
            except Exception as e:
                print(f"   ⚠ Erro ao remover {arquivo}: {e}")

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    """Função principal."""
    print("\n" + "="*60)
    print("GERADOR DE EXECUTÁVEL - UPLOAD SALESFORCE")
    print("="*60)
    
    # 1. Verificar PyInstaller
    if not verificar_pyinstaller():
        print("\n❌ Não foi possível continuar sem PyInstaller")
        input("\nPressione Enter para sair...")
        return
    
    # 2. Limpar builds anteriores
    limpar_builds_anteriores()
    
    # 3. Criar executável
    sucesso = criar_executavel()
    
    # 4. Limpar arquivos temporários (mantém apenas o executável)
    if sucesso:
        limpar_arquivos_temporarios()
    
    print("\n" + "="*60)
    print("PROCESSO FINALIZADO")
    print("="*60)
    
    if not sucesso:
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()

