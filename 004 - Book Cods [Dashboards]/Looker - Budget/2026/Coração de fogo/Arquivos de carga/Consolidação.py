import pandas as pd
import os

# --- Configurações ---
# Use o prefixo 'r' para evitar problemas com barras invertidas em caminhos do Windows
diretorio_base = r"G:\Drives compartilhados\Legales_Analytics\009 - Book de Querys\P00-2 - Dashboards\Looker - Budget\2026\Coração de fogo\Arquivos de carga"
arquivos_entrada = ["Input_Budget_2025.xlsx", "Input_Budget_2026.xlsx"]
nome_aba = "Budget"
arquivo_saida = "Consolidado_Budget.xlsx"

# Lista para armazenar os DataFrames lidos
dataframes_lista = []
colunas_para_maiusculas = []

# --- 1. Leitura e Identificação das Colunas ---
print(f"Iniciando a leitura e identificação dos cabeçalhos no diretório: {diretorio_base}")

for nome_arquivo in arquivos_entrada:
    caminho_completo = os.path.join(diretorio_base, nome_arquivo)
    
    if os.path.exists(caminho_completo):
        try:
            # Lendo apenas a aba especificada
            df = pd.read_excel(caminho_completo, sheet_name=nome_aba)
            
            # --- IDENTIFICAÇÃO DINÂMICA (COLUNAS A e B) ---
            # Identifica os nomes dos cabeçalhos das colunas A (índice 0) e B (índice 1) apenas na primeira iteração
            if not colunas_para_maiusculas and df.shape[1] >= 2:
                todos_os_nomes = df.columns.tolist()
                nome_coluna_a = todos_os_nomes[0] 
                nome_coluna_b = todos_os_nomes[1]
                
                colunas_para_maiusculas = [nome_coluna_a, nome_coluna_b]
                print(f"  - Cabeçalhos identificados: Coluna A é '{nome_coluna_a}' e Coluna B é '{nome_coluna_b}'.")
            
            # Adiciona uma coluna de origem para identificação
            df['Arquivo_Origem'] = nome_arquivo
            dataframes_lista.append(df)
            print(f"  - Arquivo lido com sucesso: {nome_arquivo}")
            
        except Exception as e:
            print(f"  - ERRO ao ler o arquivo {nome_arquivo} (Verifique se a aba '{nome_aba}' existe): {e}")
    else:
        print(f"  - ARQUIVO NÃO ENCONTRADO NO CAMINHO: {caminho_completo}")

if not dataframes_lista:
    print("\nNenhum arquivo foi lido. O processo de consolidação foi interrompido.")
    exit()

# Consolida todos os DataFrames em um único
df_consolidado = pd.concat(dataframes_lista, ignore_index=True)
print("\nArquivos consolidados com sucesso.")

# --- 2. Padronização para Maiúsculas ---
print("Iniciando a padronização para MAIÚSCULAS nas colunas identificadas...")

if colunas_para_maiusculas:
    for coluna in colunas_para_maiusculas:
        if coluna in df_consolidado.columns:
            # Converte para string antes de aplicar .upper()
            df_consolidado[coluna] = df_consolidado[coluna].astype(str).str.upper()
            print(f"  - Coluna '{coluna}' padronizada para MAIÚSCULAS.")
        else:
             print(f"  - ⚠️ AVISO: Coluna '{coluna}' não encontrada após consolidação.")
else:
    print("  - AVISO: Não foi possível identificar os nomes das colunas. Nenhuma padronização realizada.")

# --- 3. Criação/Atualização do Novo Arquivo Excel ---
caminho_saida = os.path.join(diretorio_base, arquivo_saida)

try:
    # Cria um ExcelWriter para gerenciar a escrita do arquivo
    # mode='a' (append) permite que o arquivo exista e não seja apagado
    with pd.ExcelWriter(
        caminho_saida, 
        engine='openpyxl', 
        mode='a', # Permite adicionar ou modificar em um arquivo existente
        if_sheet_exists='replace' # *** SUBSTITUI A ABA 'Budget' se ela existir ***
    ) as writer:
        
        # Escreve o DataFrame consolidado na aba 'Budget'
        df_consolidado.to_excel(writer, sheet_name=nome_aba, index=False)
        
    print(f"\n✅ Consolidação concluída! A aba '{nome_aba}' foi atualizada em: **{caminho_saida}**")

except FileNotFoundError:
    # Se o modo 'a' falhar, significa que o arquivo de destino não existe. 
    # Tentamos criar um novo arquivo.
    try:
         df_consolidado.to_excel(caminho_saida, sheet_name=nome_aba, index=False)
         print(f"\n✅ Consolidação concluída! Arquivo criado com a aba '{nome_aba}' em: **{caminho_saida}**")
    except Exception as e:
         print(f"\n❌ ERRO FATAL ao criar o arquivo de saída: {e}")

except Exception as e:
    print(f"\n❌ ERRO ao atualizar/criar o arquivo de saída: {e}")