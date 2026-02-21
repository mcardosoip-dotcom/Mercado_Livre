import os
import pandas as pd

# Pasta base onde estão os diretórios por ano
pasta_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\Consumidor.gov"

# Anos a processar
anos = list(range(2017, 2026))

# Lista de codificações a testar
codificacoes = ['utf-8', 'latin1', 'windows-1252']

for ano in anos:
    pasta_ano = os.path.join(pasta_base, str(ano))
    lista_df = []

    for subpasta in ["Mercado Livre", "Mercado Pago"]:
        caminho_subpasta = os.path.join(pasta_ano, subpasta)
        if not os.path.isdir(caminho_subpasta):
            print(f"⚠️ Subpasta não encontrada: {caminho_subpasta}")
            continue

        for arquivo in os.listdir(caminho_subpasta):
            if arquivo.lower().endswith(".csv"):
                caminho_arquivo = os.path.join(caminho_subpasta, arquivo)

                # Tentativa de leitura com múltiplas codificações
                for cod in codificacoes:
                    try:
                        df = pd.read_csv(caminho_arquivo, encoding=cod, sep=';', low_memory=False)
                        lista_df.append(df)
                        break  # Sucesso, sai do loop de codificações
                    except Exception as e:
                        if cod == codificacoes[-1]:
                            print(f"❌ Falha ao ler {caminho_arquivo}: {e}")

    if lista_df:
        df_consolidado = pd.concat(lista_df, ignore_index=True)
        caminho_saida = os.path.join(pasta_ano, f"Consolidado {ano}.csv")
        df_consolidado.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
        print(f"✅ Consolidado {ano} salvo com sucesso.")
    else:
        print(f"⚠️ Nenhum arquivo CSV válido encontrado para o ano {ano}.")
