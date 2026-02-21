import pandas as pd
import numpy as np
from datetime import date

def analisar_coluna_data(df, col_index, col_letra):
    """
    Analisa a coluna de data especificada e imprime as contagens totais
    e as 10 datas mais recentes com a frequência associada.
    """
    try:
        # Pega o nome real da coluna com base no índice (0-base) após pular 5 linhas
        col_name = df.columns[col_index]

        print(f"\n=======================================================")
        print(f"       ✅ Análise da Coluna {col_letra} (Header: '{col_name}')       ")
        print(f"=======================================================")

        # 1. Limpeza e Conversão para Data (apenas a parte da data)
        # errors='coerce' transforma valores não-data (ex: texto) em NaT (Not a Time)
        series_data = pd.to_datetime(df[col_name], errors='coerce').dt.date

        # 2. Contagem Total de Datas Válidas (excluindo NaT)
        total_datas_validas = series_data.dropna().size
        print(f"⭐ Contagem Total de Registros Válidos na Coluna {col_letra}: {total_datas_validas}")

        # 3. Contagem por Data
        # Conta a frequência de cada data única
        contagem_por_data = series_data.value_counts()

        # 4. Encontrar as 10 Datas Mais Recentes
        # Ordena o índice (as datas) de forma decrescente (mais recente primeiro) e pega as 10 primeiras.
        ultimas_10_datas = contagem_por_data.sort_index(ascending=False).head(10)

        print("\n🏆 As 10 Datas Mais Recentes e a Quantidade de Casos Associados:")
        # Imprime a tabela de forma formatada para o console
        print(ultimas_10_datas.to_string(header=['Quantidade de Casos']))

    except IndexError:
        print(f"\n❌ ERRO: A Coluna {col_letra} (Índice {col_index}) não foi encontrada.")
        print("Verifique se o arquivo tem a quantidade de colunas esperada.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao processar a Coluna {col_letra}: {e}")


# --- Configurações Principais ---

# ⚠️ ATUALIZE ESTE CAMINHO EXATAMENTE COM O QUE VOCÊ FORNECEU
FILE_PATH = r"C:\Users\mcard\Desktop\eLAW Bases\Audiencia_-_Amelia-176335283283917362875969601474111.xlsx"

# Coluna D: Índice 3 (A=0, B=1, C=2, D=3)
COL_D_INDEX = 3
# Coluna V: Índice 21 (V é a 22ª letra, índice 21)
COL_V_INDEX = 21
# Pular as 5 primeiras linhas
SKIP_ROWS = 5

# --- Execução do Script ---

print("Iniciando a leitura do arquivo...")

try:
    # Lê o arquivo Excel, pulando as primeiras 5 linhas.
    # A 6ª linha (skiprows=5) será usada como cabeçalho.
    # Usamos usecols para otimizar, lendo apenas as colunas A até V (para garantir D e V estão no índice correto).
    # Como as colunas D e V são separadas, é mais seguro ler tudo ou por índice.
    # Para garantir que D e V são os índices 3 e 21, vamos ler todas as colunas
    df = pd.read_excel(FILE_PATH, skiprows=SKIP_ROWS)

    print(f"✅ Arquivo carregado com sucesso! Total de linhas de dados: {len(df)}")
    print("Iniciando a análise das colunas D e V...")

    # Executa a análise para a Coluna D
    analisar_coluna_data(df, COL_D_INDEX, 'D')

    # Executa a análise para a Coluna V
    analisar_coluna_data(df, COL_V_INDEX, 'V')

except FileNotFoundError:
    print(f"\n❌ ERRO: O arquivo no caminho '{FILE_PATH}' não foi encontrado.")
    print("Verifique se o caminho está correto e se você tem permissão de acesso.")
except Exception as e:
    print(f"\n❌ Ocorreu um erro inesperado durante a leitura: {e}")