# ================================================
# Descrição :  Deleta todos os arquivos das pastas de arquivos parquets
# Autor     :  Marcelo Cardoso
# ================================================

import os

# Lista de caminhos das pastas a serem limpas
pastas = [
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-03 - Quebra de Sigilo",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-04 - Mesa de Entrada",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-02 - SF",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes"
]

for pasta in pastas:
    print(f"🔄 Limpando: {pasta}")
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
                print(f"✅ Arquivo deletado: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao deletar {arquivo}: {e}")
    print()  # Quebra de linha para facilitar leitura
