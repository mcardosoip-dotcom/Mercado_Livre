# ================================================
# Limpeza de pastas: deleta arquivos dentro das pastas informadas
# Autor     : Marcelo Cardoso
# Uso       : Importado por 000 - Processo completo.py (limpeza Desktop antes do PBD)
# ================================================

import os


def limpar_pastas(pastas):
    """
    Remove todos os arquivos (não subpastas) de cada pasta da lista.
    pastas: lista de caminhos absolutos de pastas.
    """
    for pasta in pastas:
        if not os.path.isdir(pasta):
            print(f"⚠️ Pasta não encontrada (ignorada): {pasta}")
            continue
        print(f"🔄 Limpando: {pasta}")
        for nome in os.listdir(pasta):
            caminho = os.path.join(pasta, nome)
            if os.path.isfile(caminho):
                try:
                    os.remove(caminho)
                    print(f"✅ Arquivo deletado: {nome}")
                except Exception as e:
                    print(f"❌ Erro ao deletar {nome}: {e}")
        print()
