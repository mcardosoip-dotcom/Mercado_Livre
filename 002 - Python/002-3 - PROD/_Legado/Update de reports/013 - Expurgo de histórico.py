# ================================================
# Descrição :  O processo faz a eliminação das pastas temporárias utilizadas, 
#              principalmente de backup, mantendo sempre os últimos 2 updates 
#              e removendo o restante para evitar acúmulo de espaço
# Autor : Marcelo Cardoso
# ================================================

import os
import shutil

def limpar_diretorio(caminho, manter=3):
    """
    Remove todas as pastas do diretório 'caminho', mantendo apenas as 'manter' mais recentes (por data de criação).
    """
    # Obtém a lista completa de subpastas no diretório
    subpastas = [
        os.path.join(caminho, nome)
        for nome in os.listdir(caminho)
        if os.path.isdir(os.path.join(caminho, nome))
    ]
    
    # Ordena as pastas pela data de criação em ordem decrescente (mais novas primeiro)
    subpastas_ordenadas = sorted(subpastas, key=os.path.getctime, reverse=True)
    
    # Se houver mais pastas que o limite, as removem
    if len(subpastas_ordenadas) > manter:
        for pasta in subpastas_ordenadas[manter:]:
            try:
                shutil.rmtree(pasta)
                print(f"Pasta removida: {pasta}")
            except Exception as e:
                print(f"Erro ao remover {pasta}: {e}")
    else:
        print("Não há pastas para remover nesse diretório.")

# Lista dos diretórios a serem processados
diretorios = [
    r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Histórico",
    r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW\Arquivos tratados eLAW\Temp\Histórico",
    r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download Salesforce\Histórico",
    r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Arquivo morto\Pastas Temp"
]

# Processa cada diretório
for diretorio in diretorios:
    print(f"\nProcessando diretório: {diretorio}")
    if os.path.exists(diretorio):
        limpar_diretorio(diretorio, manter=2)
    else:
        print(f"Diretório não encontrado: {diretorio}")
