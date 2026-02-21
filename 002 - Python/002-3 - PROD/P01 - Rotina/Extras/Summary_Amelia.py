import pandas as pd
from datetime import datetime, timedelta

# Definição dos caminhos dos arquivos
path_entrada = r'G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Database_eLAW_Amelia.xlsx'
path_saida = r'G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Extras\Summary_Amelia.xlsx'

# Lê o arquivo XLSX, pulando as 5 primeiras linhas
try:
    df = pd.read_excel(path_entrada, skiprows=5, engine='openpyxl')
except FileNotFoundError:
    print(f"Erro: O arquivo não foi encontrado em '{path_entrada}'. Verifique o caminho e o nome do arquivo.")
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")
    exit()

# Renomeia a coluna 'v' para 'Data Registrado' para clareza
# Nota: o nome da coluna pode variar dependendo do cabeçalho que sobrou após pular as linhas
df.rename(columns={'v': 'Data Registrado'}, inplace=True)

# Converte a coluna 'Data Registrado' para o formato de data
try:
    df['Data Registrado'] = pd.to_datetime(df['Data Registrado'], errors='coerce')
except KeyError:
    print("Erro: A coluna 'Data Registrado' não foi encontrada. Verifique o cabeçalho do arquivo.")
    exit()

# Calcula a data de 5 dias atrás
data_limite = datetime.now() - timedelta(days=5)

# Filtra os dados para os últimos 5 dias e remove linhas com datas inválidas
df_filtrado = df[df['Data Registrado'] >= data_limite].dropna(subset=['Data Registrado'])

# Agrupa e conta a quantidade de casos por data (apenas a parte da data)
df_sumario = df_filtrado.groupby(df_filtrado['Data Registrado'].dt.date).size().reset_index(name='Quantidade de Casos')

# Renomeia a coluna de data para melhor visualização
df_sumario.rename(columns={'Data Registrado': 'Data'}, inplace=True)

# Ordena os resultados por data de forma decrescente
df_sumario.sort_values(by='Data', ascending=False, inplace=True)

# Salva o resultado em um novo arquivo XLSX com o nome da aba especificado
try:
    with pd.ExcelWriter(path_saida, engine='openpyxl') as writer:
        df_sumario.to_excel(writer, sheet_name='Database', index=False)
    print(f"Resumo salvo com sucesso em '{path_saida}', na aba 'Database'.")
except Exception as e:
    print(f"Ocorreu um erro ao salvar o arquivo: {e}")