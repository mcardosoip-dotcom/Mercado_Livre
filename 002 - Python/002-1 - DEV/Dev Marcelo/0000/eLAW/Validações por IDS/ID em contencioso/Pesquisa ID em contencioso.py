import pandas as pd
import os
import datetime
import platform
import threading
import time

# ==============================================================================
#   ÁREA DE CONFIGURAÇÃO (EDITE APENAS AQUI)
# ==============================================================================

# LISTA DE IDS PARA BUSCA
IDS_PARA_BUSCAR = ["834658", "759817", "754991", "764881"]

# ==============================================================================
#   DETECÇÃO E SELEÇÃO DO SISTEMA OPERACIONAL
# ==============================================================================

def detectar_sistema():
    """Detecta o sistema operacional e permite escolha manual com timeout de 5 segundos"""
    sistema_detectado = platform.system()
    
    print("=" * 60)
    print("DETECÇÃO DE SISTEMA OPERACIONAL")
    print("=" * 60)
    
    if sistema_detectado == "Darwin":
        sistema_detectado_nome = "Mac"
    elif sistema_detectado == "Windows":
        sistema_detectado_nome = "Windows"
    else:
        sistema_detectado_nome = sistema_detectado
    
    print(f"Sistema detectado automaticamente: {sistema_detectado_nome}")
    print("\nOpções:")
    print("1 - Mac")
    print("2 - Windows")
    print("3 - Usar sistema detectado automaticamente")
    
    # Mostra contagem regressiva enquanto aguarda input
    escolha = None
    input_recebido = threading.Event()
    
    def ler_input_com_contagem():
        """Função auxiliar para capturar input em thread separada"""
        nonlocal escolha
        try:
            escolha = input("\nEscolha uma opção (1/2/3) [padrão: 3]: ").strip()
            input_recebido.set()
        except:
            pass
    
    # Cria thread para capturar input
    input_thread = threading.Thread(target=ler_input_com_contagem, daemon=True)
    input_thread.start()
    
    # Conta regressiva de 5 segundos
    print("(Aguardando 5 segundos...)", end="", flush=True)
    for i in range(5, 0, -1):
        if input_recebido.is_set():
            print()  # Nova linha após input
            break
        time.sleep(1)
        if not input_recebido.is_set():
            print(f"\r(Aguardando {i} segundo(s)...)", end="", flush=True)
    
    # Verifica se o input foi recebido
    if not input_recebido.is_set():
        print("\n\n⏱ Tempo esgotado! Usando sistema detectado automaticamente.")
        sistema_escolhido = sistema_detectado
        print(f"✓ Usando sistema detectado: {sistema_detectado_nome}")
    else:
        # Processa a escolha do usuário
        if escolha == "" or escolha == "3":
            sistema_escolhido = sistema_detectado
            print(f"✓ Usando sistema detectado: {sistema_detectado_nome}")
        elif escolha == "1":
            sistema_escolhido = "Darwin"
            print("✓ Sistema selecionado: Mac")
        elif escolha == "2":
            sistema_escolhido = "Windows"
            print("✓ Sistema selecionado: Windows")
        else:
            print("⚠ Opção inválida! Usando sistema detectado automaticamente.")
            sistema_escolhido = sistema_detectado
            print(f"✓ Usando sistema detectado: {sistema_detectado_nome}")
    
    return sistema_escolhido

# Detecta/Seleciona o sistema operacional
SISTEMA = detectar_sistema()

# Define os caminhos base conforme o sistema
if SISTEMA == "Darwin":  # Mac
    BASE_PATH = r"/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics"
elif SISTEMA == "Windows":  # Windows
    BASE_PATH = r"G:\Drives compartilhados\Legales_Analytics"
else:
    # Fallback: tenta detectar pelo caminho atual do script
    script_path = os.path.abspath(__file__)
    if "GoogleDrive" in script_path or "/Users/" in script_path:
        BASE_PATH = r"/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics"
        print(f"\n⚠ Sistema não reconhecido. Usando caminhos do Mac como padrão.")
    else:
        BASE_PATH = r"G:\Drives compartilhados\Legales_Analytics"
        print(f"\n⚠ Sistema não reconhecido. Usando caminhos do Windows como padrão.")

# CAMINHOS DAS PASTAS (ajustados automaticamente conforme o sistema)
PASTA_ORIGEM = os.path.join(BASE_PATH, "001 - Base", "STAGE")
PASTA_DESTINO = os.path.join(BASE_PATH, "002 - Python", "002-1 - DEV", "Dev Marcelo", "eLAW", "Validações por IDS", "ID em contencioso")

# LISTA DOS ARQUIVOS A SEREM LIDOS
LISTA_ARQUIVOS = [
    "Database_eLAW_Contencioso_Brasil_Completo.xlsx",
    "Database_eLAW_Contencioso_Brasil_Ongoing.xlsx",
    "Database_eLAW_Contencioso_Brasil_Outgoing.xlsx",
    "Database_eLAW_Contencioso_Brasil_Incoming.xlsx",
    "Database_eLAW_Contencioso_Hispanos_Incoming.xlsx",
    "Database_eLAW_Contencioso_Hispanos_Ongoing.xlsx",
    "Database_eLAW_Contencioso_Hispanos_Outgoing.xlsx"
]

# ==============================================================================
#   FIM DA CONFIGURAÇÃO
# ==============================================================================

# Nome do arquivo de saída
nome_arquivo_saida = "Informações_Contencioso_Consolidado.xlsx"
path_saida_completo = os.path.join(PASTA_DESTINO, nome_arquivo_saida)

# Garante que a pasta de destino existe
os.makedirs(PASTA_DESTINO, exist_ok=True)

dados_resumo = []

print("\n" + "=" * 60)
print("--- INICIANDO PROCESSO ---")
print("=" * 60)
print(f"Sistema operacional: {'Mac' if SISTEMA == 'Darwin' else 'Windows'}")
print(f"IDs pesquisados: {', '.join(IDS_PARA_BUSCAR)}")
print(f"Pasta de origem: {PASTA_ORIGEM}")
print(f"Pasta de destino: {PASTA_DESTINO}")
print("=" * 60 + "\n")

# Criar o escritor do Excel
with pd.ExcelWriter(path_saida_completo, engine="openpyxl") as writer:

    for arquivo in LISTA_ARQUIVOS:
        caminho_arquivo = os.path.join(PASTA_ORIGEM, arquivo)

        # Nome curto para a aba
        nome_aba = arquivo.replace("Database_eLAW_Contencioso_", "").replace(".xlsx", "")
        nome_aba = nome_aba[:31]

        try:
            if os.path.exists(caminho_arquivo):
                print(f"Lendo: {arquivo}...")

                # header=5: ignora as primeiras 5 linhas
                df = pd.read_excel(caminho_arquivo, header=5)

                if df.shape[1] >= 2:
                    coluna_id = df.iloc[:, 1].astype(str).str.strip()
                    filtro = coluna_id.isin(IDS_PARA_BUSCAR)
                    df_filtrado = df[filtro]

                    df_filtrado.to_excel(
                        writer,
                        sheet_name=nome_aba,
                        index=False
                    )

                    qtd_encontrada = len(df_filtrado)
                    print(f"  -> {qtd_encontrada} registros encontrados.")
                else:
                    qtd_encontrada = 0
                    print("  -> Erro: arquivo sem colunas suficientes.")

                dados_resumo.append({
                    "Base Original": arquivo,
                    "Nome da Aba": nome_aba,
                    "Registros Encontrados": qtd_encontrada,
                    "Status": "Sucesso"
                })

            else:
                print(f"  -> Arquivo NÃO encontrado: {arquivo}")
                dados_resumo.append({
                    "Base Original": arquivo,
                    "Nome da Aba": "-",
                    "Registros Encontrados": 0,
                    "Status": "Arquivo Inexistente"
                })

        except Exception as e:
            print(f"  -> Erro crítico em {arquivo}: {e}")
            dados_resumo.append({
                "Base Original": arquivo,
                "Nome da Aba": "-",
                "Registros Encontrados": 0,
                "Status": f"Erro: {str(e)}"
            })

    print("---")
    print("Gerando Resumo Final...")

    df_resumo = pd.DataFrame(dados_resumo)
    df_resumo = df_resumo[
        ["Base Original", "Nome da Aba", "Registros Encontrados", "Status"]
    ]
    df_resumo.to_excel(
        writer,
        sheet_name="RESUMO_GERAL",
        index=False
    )

print("CONCLUÍDO!")
print(f"Arquivo salvo em:\n{path_saida_completo}")
