import os
import pandas as pd

# Caminho da pasta de entrada
pasta_stage = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"

# Caminho de saída
pasta_saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Padrão de bases e colunas"
os.makedirs(pasta_saida, exist_ok=True)

# Apenas alterei o nome do arquivo de saída aqui
caminho_saida = os.path.join(pasta_saida, "Mapa_de_colunas_padrão.xlsx")

# Dicionário: chave = nome do arquivo | valor = lista de colunas
colunas_por_arquivo = {}

# Lê arquivos .xlsx e .csv da pasta
for nome_arquivo in os.listdir(pasta_stage):
    caminho_arquivo = os.path.join(pasta_stage, nome_arquivo)
    # print(f"Processando arquivo: {nome_arquivo}") # DEBUG: Mantido para ajudar na verificação

    try:
        df = None
        if nome_arquivo.lower().endswith('.xlsx'):
            if "eLAW" in nome_arquivo:
                df = pd.read_excel(caminho_arquivo, skiprows=5, nrows=1)
                # print(f"  - Tipo: Excel (eLAW)")
            else:
                df = pd.read_excel(caminho_arquivo, nrows=1)
                # print(f"  - Tipo: Excel (Outro)")
        elif nome_arquivo.lower().endswith('.csv'):
            # print(f"  - Tipo: CSV. Tentando ler com delimitador ';'")
            try:
                df = pd.read_csv(caminho_arquivo, nrows=1, sep=';', encoding='utf-8')
                # print(f"  - CSV lido com sucesso (UTF-8, delimitador ';')")
            except UnicodeDecodeError:
                # print(f"  - Erro UTF-8, tentando Latin-1 para {nome_arquivo}")
                df = pd.read_csv(caminho_arquivo, nrows=1, sep=';', encoding='latin1')
                # print(f"  - CSV lido com sucesso (Latin-1, delimitador ';')")
            except Exception as csv_e:
                # print(f"  - ERRO ao ler CSV {nome_arquivo}: {csv_e}")
                continue
        else:
            # print(f"  - Ignorando arquivo não suportado: {nome_arquivo}")
            continue

        if df is not None:
            # print(f"  - DataFrame carregado. Primeiras colunas brutas: {df.columns.tolist()}")
            colunas = [str(col).strip() for col in df.columns if str(col).strip() != ""]
            colunas_por_arquivo[nome_arquivo] = colunas
            # print(f"  - Colunas limpas para {nome_arquivo}: {colunas}")
        # else:
            # print(f"  - DataFrame não foi criado para {nome_arquivo}. Possível problema de leitura.")

    except Exception as e:
        print(f"Erro geral ao ler {nome_arquivo}: {e}")

# --- Lógica para Ordenação ---
arquivos_elaw = []
arquivos_outros = []

for nome_arquivo in colunas_por_arquivo.keys():
    if "eLAW" in nome_arquivo:
        arquivos_elaw.append(nome_arquivo)
    else:
        arquivos_outros.append(nome_arquivo)

arquivos_elaw.sort()
arquivos_outros.sort()

ordem_final_colunas = arquivos_elaw + arquivos_outros

# Descobre o maior número de colunas em qualquer arquivo
if colunas_por_arquivo:
    max_linhas = max(len(colunas) for colunas in colunas_por_arquivo.values())
else:
    max_linhas = 0

# Monta DataFrame: cada coluna é um arquivo, seguindo a ordem definida
df_resultado = pd.DataFrame({
    arquivo: colunas_por_arquivo[arquivo] + [""] * (max_linhas - len(colunas_por_arquivo[arquivo]))
    for arquivo in ordem_final_colunas
})

# Salva o resultado
df_resultado.to_excel(caminho_saida, index=False)
print(f"✅ Mapa de colunas padrão gerado em: {caminho_saida}")