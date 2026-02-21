import pandas as pd
import os
import platform
import threading
import time

# ==============================================================================
#   ÁREA DE CONFIGURAÇÃO
# ==============================================================================

# LISTA DE IDS PARA BUSCA
IDS_PARA_BUSCAR = ["894538", "852734"]

# LISTA DOS ARQUIVOS A SEREM LIDOS
LISTA_ARQUIVOS = [
    "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias.xlsx",
    "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados.xlsx",
    "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias.xlsx",
    "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes.xlsx"
]

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
    
    escolha = None
    input_recebido = threading.Event()
    
    def ler_input_com_contagem():
        nonlocal escolha
        try:
            escolha = input("\nEscolha uma opção (1/2/3) [padrão: 3]: ").strip()
            input_recebido.set()
        except:
            pass
    
    # Thread para input
    input_thread = threading.Thread(target=ler_input_com_contagem, daemon=True)
    input_thread.start()
    
    # Contagem regressiva
    print("(Aguardando 5 segundos...)", end="", flush=True)
    for i in range(5, 0, -1):
        if input_recebido.is_set():
            print()
            break
        time.sleep(1)
        if not input_recebido.is_set():
            print(f"\r(Aguardando {i} segundo(s)...)", end="", flush=True)
    
    # Processa escolha
    if not input_recebido.is_set():
        print("\n\n⏱ Tempo esgotado! Usando sistema detectado automaticamente.")
        sistema_escolhido = sistema_detectado
    else:
        if escolha == "1":
            sistema_escolhido = "Darwin"
            print("✓ Sistema selecionado: Mac")
        elif escolha == "2":
            sistema_escolhido = "Windows"
            print("✓ Sistema selecionado: Windows")
        else:
            sistema_escolhido = sistema_detectado
            print(f"✓ Usando sistema detectado: {sistema_detectado_nome}")
    
    return sistema_escolhido

# ==============================================================================
#   DEFINIÇÃO DE CAMINHOS
# ==============================================================================

SISTEMA = detectar_sistema()

if SISTEMA == "Darwin":  # Mac
    BASE_PATH = r"/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics"
elif SISTEMA == "Windows":  # Windows
    # Atualizado para o drive H: conforme solicitado
    BASE_PATH = r"H:\Drives compartilhados\Legales_Analytics"
else:
    # Fallback
    BASE_PATH = r"H:\Drives compartilhados\Legales_Analytics"

# Caminho de Entrada (Mantido padrão na pasta STAGE)
PASTA_ORIGEM = os.path.join(BASE_PATH, "001 - Base", "STAGE")

# Caminho de Saída (Atualizado para o caminho profundo solicitado)
PASTA_DESTINO = os.path.join(
    BASE_PATH, 
    "002 - Python", 
    "002-1 - DEV", 
    "Dev Marcelo", 
    "eLAW", 
    "Validações por IDS", 
    "ID em Subsídios Clean"
)

# Garante que a pasta existe (cria toda a árvore se necessário)
os.makedirs(PASTA_DESTINO, exist_ok=True)

NOME_ARQUIVO_SAIDA = "Consolidado_Busca_IDs.xlsx"
PATH_SAIDA_COMPLETO = os.path.join(PASTA_DESTINO, NOME_ARQUIVO_SAIDA)

# ==============================================================================
#   PROCESSAMENTO
# ==============================================================================

dados_resumo = []

print("\n" + "=" * 60)
print("--- INICIANDO PROCESSO ---")
print(f"Sistema: {SISTEMA}")
print(f"IDs Buscados: {IDS_PARA_BUSCAR}")
print(f"Pasta Origem: {PASTA_ORIGEM}")
print(f"Pasta Destino: {PASTA_DESTINO}")
print("=" * 60 + "\n")

with pd.ExcelWriter(PATH_SAIDA_COMPLETO, engine="openpyxl") as writer:
    
    arquivos_processados = 0

    for arquivo in LISTA_ARQUIVOS:
        caminho_arquivo = os.path.join(PASTA_ORIGEM, arquivo)
        
        # Cria nome curto para a aba
        nome_aba = arquivo.replace("Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_", "")
        nome_aba = nome_aba.replace(".xlsx", "")[:31]

        try:
            if os.path.exists(caminho_arquivo):
                print(f"Lendo: {arquivo}...")
                
                # header=5 -> Ignora as primeiras 5 linhas
                df = pd.read_excel(caminho_arquivo, header=5)
                
                if df.shape[1] >= 1:
                    # PROCURA NA COLUNA A (índice 0)
                    coluna_a = df.iloc[:, 0].astype(str).str.strip()
                    
                    filtro = coluna_a.isin(IDS_PARA_BUSCAR)
                    df_filtrado = df[filtro]
                    
                    qtd_encontrada = len(df_filtrado)
                    
                    df_filtrado.to_excel(writer, sheet_name=nome_aba, index=False)
                    
                    status = "Sucesso"
                    print(f"  -> {qtd_encontrada} registros encontrados.")
                else:
                    qtd_encontrada = 0
                    status = "Arquivo sem colunas suficientes"
                    print("  -> Erro: Arquivo vazio ou colunas insuficientes.")

            else:
                qtd_encontrada = 0
                status = "Arquivo não encontrado na pasta"
                print(f"  -> AVISO: Arquivo não encontrado: {arquivo}")

            dados_resumo.append({
                "Arquivo Fonte": arquivo,
                "Aba Criada": nome_aba,
                "Registros Encontrados": qtd_encontrada,
                "Status": status
            })
            arquivos_processados += 1

        except Exception as e:
            print(f"  -> Erro crítico ao ler {arquivo}: {e}")
            dados_resumo.append({
                "Arquivo Fonte": arquivo,
                "Aba Criada": "-",
                "Registros Encontrados": 0,
                "Status": f"Erro Python: {str(e)}"
            })

    # ==========================================================================
    #   GERAR RESUMO
    # ==========================================================================
    print("---")
    print("Gerando aba de Resumo...")
    
    df_resumo = pd.DataFrame(dados_resumo)
    df_resumo.to_excel(writer, sheet_name="RESUMO_GERAL", index=False)

print("\n" + "=" * 60)
print("CONCLUÍDO!")
print(f"Arquivo salvo em:\n{PATH_SAIDA_COMPLETO}")
print("=" * 60)