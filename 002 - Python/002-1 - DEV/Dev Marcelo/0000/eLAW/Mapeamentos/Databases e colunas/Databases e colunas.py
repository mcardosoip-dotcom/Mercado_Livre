import pandas as pd
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm  # pip install tqdm
import platform
import threading
import time
import os

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
    BASE_PATH = Path("/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics")
elif SISTEMA == "Windows":  # Windows
    BASE_PATH = Path(r"G:\Drives compartilhados\Legales_Analytics")
else:
    # Fallback para Windows caso não identificado
    BASE_PATH = Path(r"G:\Drives compartilhados\Legales_Analytics")

# Caminhos relativos usando pathlib (funciona em ambos os sistemas)
PASTA_LEITURA = BASE_PATH / "001 - Base" / "STAGE"
PASTA_SAIDA = BASE_PATH / "002 - Python" / "002-1 - DEV" / "Dev Marcelo" / "eLAW" / "Mapeamentos" / "Databases e colunas"

PADRAO_ARQUIVOS = "*eLAW*.xlsx"
NOME_ARQUIVO_SAIDA = "Relatorio_Estrutura_eLAW.xlsx"

LINHAS_A_PULAR = 5
COLUNA_CABECALHO = 0

# ==============================================================================
#   LÓGICA DE PROCESSAMENTO
# ==============================================================================

def ler_arquivo_excel(caminho: Path) -> pd.DataFrame:
    """Lê um arquivo Excel com parâmetros predefinidos."""
    df = pd.read_excel(
        caminho,
        engine="openpyxl",
        skiprows=LINHAS_A_PULAR,
        header=COLUNA_CABECALHO
    )
    return df.dropna(how="all")


def processar_arquivos(lista_arquivos: list[Path]):
    """Processa a lista de arquivos, extraindo colunas e registros não nulos."""
    dados_colunas = []  # Cada coluna vira uma linha
    mapeamento_colunas = defaultdict(list)

    for caminho in tqdm(lista_arquivos, desc="Processando arquivos"):
        nome_arquivo = caminho.name
        try:
            df = ler_arquivo_excel(caminho)
            colunas = [str(c).strip() for c in df.columns]

            # Para cada coluna do arquivo, cria uma linha na aba _Colunas_e_Registros
            for coluna in colunas:
                qtd_registros = df[coluna].notna().sum()  # apenas valores preenchidos

                dados_colunas.append({
                    "Nome do Arquivo": nome_arquivo,
                    "Nome da Coluna": coluna,
                    "Quantidade de Registros (Preenchidos)": qtd_registros
                })

                if nome_arquivo not in mapeamento_colunas[coluna]:
                    mapeamento_colunas[coluna].append(nome_arquivo)

        except Exception as e:
            print(f"[ERRO] Falha ao ler {nome_arquivo}: {e}")

    return dados_colunas, mapeamento_colunas


def formatar_mapeamento(mapeamento_colunas: dict) -> pd.DataFrame:
    """Transforma o dicionário de colunas em DataFrame resumido (sem duplicidade)."""
    linhas = [
        {
            "Nome da Coluna": coluna,
            "Quantidade de Bases/Extrações": len(set(arquivos))
        }
        for coluna, arquivos in mapeamento_colunas.items()
    ]

    return pd.DataFrame(linhas).sort_values(
        by=["Nome da Coluna"]
    ).reset_index(drop=True)


def salvar_relatorio(dados_colunas, df_mapeamento):
    """Salva os resultados em um arquivo Excel."""
    caminho_saida = PASTA_SAIDA / NOME_ARQUIVO_SAIDA
    
    # Cria a pasta se não existir
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    print(f"\nTentando salvar em: {caminho_saida}")

    try:
        with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
            # Aba 1: uma linha por Nome do Arquivo + Nome da Coluna
            pd.DataFrame(dados_colunas).to_excel(
                writer, sheet_name="_Colunas_e_Registros", index=False
            )

            # Aba 2: colunas únicas + contagem de bases
            df_mapeamento.to_excel(
                writer, sheet_name="_Mapeamento_Colunas", index=False
            )

        print(f"[OK] Relatório gerado com sucesso!")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar relatório: {e}")


def main():
    print("\n" + "-" * 60)
    print(f"Iniciando análise...")
    print(f"Pasta Leitura: {PASTA_LEITURA}")
    print(f"Pasta Saída:   {PASTA_SAIDA}")
    print(f"Configuração:  cabeçalho lido após {LINHAS_A_PULAR} linhas")
    print("-" * 60 + "\n")

    # Verifica se o caminho existe antes de listar
    if not PASTA_LEITURA.exists():
        print(f"[ERRO CRÍTICO] A pasta de leitura não foi encontrada:\n{PASTA_LEITURA}")
        return

    lista_arquivos = list(PASTA_LEITURA.glob(PADRAO_ARQUIVOS))

    if not lista_arquivos:
        print("[INFO] Nenhum arquivo encontrado correspondente ao padrão.")
        return

    print(f"[INFO] {len(lista_arquivos)} arquivos encontrados.")
    dados_colunas, mapeamento_colunas = processar_arquivos(lista_arquivos)

    df_mapeamento = formatar_mapeamento(mapeamento_colunas)
    salvar_relatorio(dados_colunas, df_mapeamento)


if __name__ == "__main__":
    main()