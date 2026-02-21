import os
import pandas as pd

# Caminhos
pasta_stage = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"
pasta_saida = os.path.join(pasta_stage, "Padrão de bases e colunas")
os.makedirs(pasta_saida, exist_ok=True)

# O mapa de colunas agora é o "Mapa_de_colunas_padrão.xlsx"
caminho_mapa = os.path.join(pasta_saida, "Mapa_de_colunas_padrão.xlsx")
caminho_saida_diferencas = os.path.join(pasta_saida, "Diferencas_de_colunas_padrão.xlsx") # Nome mais genérico

# Verifica se o arquivo de mapa existe antes de tentar ler
if not os.path.exists(caminho_mapa):
    print(f"Erro: O arquivo do mapa de colunas '{caminho_mapa}' não foi encontrado.")
    print("Por favor, execute o script de geração do mapa de colunas primeiro.")
    exit() # Sai do script se o mapa não existir

# Leitura do mapa de colunas original
try:
    df_mapa = pd.read_excel(caminho_mapa)
    # Transforma o mapa: colunas = arquivos, valores = colunas dos arquivos
    mapa_colunas = {
        col: [str(c).strip() for c in df_mapa[col].dropna() if str(c).strip()]
        for col in df_mapa.columns
    }
    print(f"Mapa de colunas '{os.path.basename(caminho_mapa)}' carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o mapa de colunas '{caminho_mapa}': {e}")
    exit()

# Lista para armazenar diferenças
diferencas_lista = []

# Percorre todos os arquivos Excel e CSV na pasta_stage
for nome_arquivo in os.listdir(pasta_stage):
    caminho_arquivo = os.path.join(pasta_stage, nome_arquivo)
    
    # Ignora o próprio arquivo de mapa e o de diferenças
    if nome_arquivo == os.path.basename(caminho_mapa) or \
       nome_arquivo == os.path.basename(caminho_saida_diferencas):
        continue

    df = None # Inicializa df como None para cada iteração
    colunas_atuais = set() # Inicializa set vazio

    try:
        if nome_arquivo.lower().endswith(".xlsx"):
            if "eLAW" in nome_arquivo:
                # Para eLAW, ignora 5 linhas
                df = pd.read_excel(caminho_arquivo, skiprows=5, nrows=1)
            else:
                # Para outros Excels, lê a primeira linha
                df = pd.read_excel(caminho_arquivo, nrows=1)
            # print(f"Lendo Excel: {nome_arquivo}") # Debug
        elif nome_arquivo.lower().endswith(".csv"):
            try:
                # Para CSVs, usa delimitador ';' e tenta encodings
                df = pd.read_csv(caminho_arquivo, nrows=1, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(caminho_arquivo, nrows=1, sep=';', encoding='latin1')
            # print(f"Lendo CSV: {nome_arquivo}") # Debug
        else:
            # Ignora arquivos que não são Excel ou CSV
            continue

        if df is not None:
            # Limpa colunas: remove espaços, vazias e "Unnamed: X"
            colunas_atuais = set([str(c).strip() for c in df.columns if str(c).strip() and not str(c).startswith("Unnamed:")])
            
            # Obtém as colunas esperadas do mapa
            # É crucial que o nome do arquivo no mapa seja EXATAMENTE o mesmo do arquivo na pasta
            colunas_mapeadas = set(mapa_colunas.get(nome_arquivo, []))

            colunas_adicionadas = sorted(list(colunas_atuais - colunas_mapeadas))
            colunas_removidas = sorted(list(colunas_mapeadas - colunas_atuais))

            if colunas_adicionadas or colunas_removidas:
                diferencas_lista.append({
                    "arquivo": nome_arquivo,
                    "colunas_adicionadas": ", ".join(colunas_adicionadas) if colunas_adicionadas else "Nenhuma",
                    "colunas_removidas": ", ".join(colunas_removidas) if colunas_removidas else "Nenhuma",
                })
        # else:
            # print(f"Aviso: Não foi possível carregar DataFrame para {nome_arquivo}.")

    except Exception as e:
        print(f"Erro ao processar {nome_arquivo}: {e}")

# Gera DataFrame de saída das diferenças
df_diferencas = pd.DataFrame(diferencas_lista)

# Define status com base no resultado e salva se houver diferenças
if df_diferencas.empty:
    status_validacao = "OK"
    print("\n✅ Status da validação de colunas: OK. Nenhuma diferença encontrada.")
else:
    status_validacao = "Erro"
    df_diferencas.to_excel(caminho_saida_diferencas, index=False)
    print(f"\n⚠️ Status da validação de colunas: Erro. Diferenças encontradas e salvas em: {caminho_saida_diferencas}")




    # Caminho do arquivo de status
caminho_status = os.path.join(pasta_saida, "status_validacao.txt")

with open(caminho_status, "w") as f:
    f.write(status_validacao)