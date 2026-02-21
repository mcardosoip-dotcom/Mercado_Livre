import pandas as pd

# Caminho do arquivo parquet
path = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW\Database_eLAW_Obrigacoes_de_Fazer_Com_Multas.parquet"

# Lê o parquet (carrega apenas algumas linhas para evitar lentidão)
df = pd.read_parquet(path)

# Verifica as colunas relevantes
cols = ['tem_multa_fixada', 'valor_da_multa_r', 'periodicidade_da_multa', 'teto_multa', 'prazo_para_cumprimento']

# Mostra amostra de dados
print(df[cols].head(10))

# Mostra informações de tipo e nulos
print("\nTipos de dados:")
print(df[cols].dtypes)

print("\nPercentual de preenchimento:")
print((df[cols].notnull().mean() * 100).round(2))

print("\nExemplos onde valor_da_multa_r = 0, vazio ou nulo:")
print(df[df['valor_da_multa_r'].isin([0, '0', '', None])][cols].head(10))
