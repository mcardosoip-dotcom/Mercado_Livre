import pandas as pd
import os
import unicodedata # Biblioteca necessária para remover os acentos

# Caminho do arquivo CSV de entrada
caminho_csv = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\Consumidor.gov\Consolidado Geral.csv"

# Nome do arquivo Parquet de saída
nome_saida = "Base_GOV_Consolidada.parquet"

# Diretório onde o Parquet será salvo
pasta_saida = os.path.dirname(caminho_csv)
caminho_saida = os.path.join(pasta_saida, nome_saida)

try:
    # Leitura do CSV
    df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8', low_memory=False)

    # ----- INÍCIO DA MODIFICAÇÃO -----
    # 1. Armazena os nomes originais das colunas (opcional, bom para debug)
    colunas_originais = df.columns.tolist()

    # 2. Cria uma nova lista de nomes de colunas, já limpos
    #    - unicodedata.normalize remove os acentos (ex: 'Região' -> 'Regiao')
    #    - .replace(' ', '_') substitui os espaços por underlines
    colunas_novas = [
        ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
        .replace(' ', '_')
        for col in df.columns
    ]

    # 3. Atribui a nova lista de nomes ao DataFrame
    df.columns = colunas_novas
    # ----- FIM DA MODIFICAÇÃO -----

    # Escrita do Parquet com as colunas renomeadas
    df.to_parquet(caminho_saida, index=False)
    
    print(f"✅ Arquivo Parquet salvo com sucesso em: {caminho_saida}")
    print("\nNomes das colunas ajustados para:")
    print(df.columns.tolist())

except Exception as e:
    print(f"❌ Erro ao processar o arquivo: {e}")