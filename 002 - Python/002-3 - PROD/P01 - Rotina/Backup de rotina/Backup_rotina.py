import shutil
import datetime
import os

# --- Configurações de Caminho ---

# Caminho da pasta de origem (a ser copiada)
# O 'r' antes da string é para criar uma raw string, o que simplifica o uso de '\' em caminhos do Windows
SOURCE_DIR = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina"

# Caminho do diretório de destino (onde a cópia será salva)
DESTINATION_BASE_DIR = r"G:\Drives compartilhados\Legales_Analytics\014 - Backup PROD Rotina"

# --- Lógica do Backup ---

try:
    # 1. Gerar o nome da nova pasta com a data atual
    # Formato: YYYY-MM-DD (exemplo: 2025-10-13)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_dir_name = f"P01 - Rotina - BACKUP_{current_date}"

    # 2. Criar o caminho de destino completo
    # Combina o caminho base de destino com o novo nome da pasta
    DESTINATION_FULL_PATH = os.path.join(DESTINATION_BASE_DIR, new_dir_name)

    # 3. Copiar o diretório de forma recursiva
    # shutil.copytree() copia todo o conteúdo da pasta de origem para o novo destino.
    # O argumento 'dirs_exist_ok=False' (padrão) garante que o script falhe
    # se a pasta de backup do dia já existir, prevenindo sobrescrita acidental.
    shutil.copytree(SOURCE_DIR, DESTINATION_FULL_PATH)

    print("-" * 50)
    print("✅ Backup realizado com sucesso!")
    print(f"Pasta de Origem: {SOURCE_DIR}")
    print(f"Pasta de Destino: {DESTINATION_FULL_PATH}")
    print("-" * 50)

except FileExistsError:
    # Este erro ocorre se a pasta de destino (com a data atual) já existir
    print("-" * 50)
    print(f"⚠️ Erro: A pasta de destino já existe para a data de hoje: {DESTINATION_FULL_PATH}")
    print("Por favor, verifique se o backup já foi executado hoje.")
    print("-" * 50)
except FileNotFoundError:
    # Este erro ocorre se a pasta de origem não for encontrada
    print("-" * 50)
    print(f"❌ Erro: A pasta de origem não foi encontrada: {SOURCE_DIR}")
    print("Verifique se o caminho da pasta de origem está correto.")
    print("-" * 50)
except Exception as e:
    # Outros erros que podem ocorrer durante a cópia
    print("-" * 50)
    print(f"❌ Ocorreu um erro durante a cópia: {e}")
    print("-" * 50)