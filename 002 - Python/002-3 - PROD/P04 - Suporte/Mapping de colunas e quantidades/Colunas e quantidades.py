import os
import pandas as pd

def process_folder_files(folder_path, output_folder):
    """
    Processa arquivos em uma pasta, focando em arquivos com 'eLAW' no nome.
    Para arquivos 'eLAW', desconsidera as primeiras 5 linhas.
    Lista arquivos, colunas e contagem de dados em formato tabular ("longo"),
    salvando o resultado em um arquivo XLSX consolidado.

    Args:
        folder_path (str): Caminho da pasta onde estão os arquivos de origem.
        output_folder (str): Caminho da pasta onde o arquivo de saída será salvo.
    """
    # Validação das pastas
    if not os.path.isdir(folder_path):
        print(f"❌ Erro: A pasta de origem '{folder_path}' não existe.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Pasta de saída criada: {output_folder}")

    # Caminho completo do arquivo final
    output_filepath = os.path.join(output_folder, "Mapping_tabelas_e_colunas.xlsx")

    all_column_records = []  # Lista para armazenar as informações de cada arquivo
    print(f"\n🚀 Iniciando processamento da pasta: {folder_path}\n")

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if not os.path.isfile(filepath):
            continue  # Ignora subpastas

        # Processa apenas arquivos que contenham 'eLAW' no nome (case-insensitive)
        if "elaw" not in filename.lower():
            print(f"⏭️  Pulando arquivo: {filename} (não contém 'eLAW')\n")
            continue

        print(f"📄 Processando: {filename}")
        skip_rows = 5  # Pular 5 linhas para arquivos eLAW
        df = None

        try:
            # --- Leitura do arquivo ---
            if filename.lower().endswith(".csv"):
                try:
                    df = pd.read_csv(filepath, encoding="utf-8", skiprows=skip_rows)
                    print(f"  ✅ CSV lido com sucesso (UTF-8).")
                except UnicodeDecodeError:
                    df = pd.read_csv(filepath, encoding="latin1", skiprows=skip_rows)
                    print(f"  ⚠️ CSV lido com codificação Latin-1.")
            elif filename.lower().endswith(".xlsx"):
                df = pd.read_excel(filepath, skiprows=skip_rows)
                print(f"  ✅ XLSX lido com sucesso.")
            else:
                print(f"  ⚠️ Tipo de arquivo não suportado: {filename}")
                continue

            # --- Análise de colunas e contagem de dados ---
            if df is not None:
                total_rows_after_skip = len(df)

                if len(df.columns) == 0:
                    print(f"  ⚠️ Nenhuma coluna detectada. Verifique o cabeçalho.\n")
                    all_column_records.append({
                        "Arquivo": filename,
                        "Coluna": "N/A (Sem colunas detectadas)",
                        "Quantidade de Registros": 0,
                        "Total de Linhas do Arquivo (após pular)": total_rows_after_skip,
                        "Status": "Aviso: Cabeçalho ausente",
                        "Detalhes do Erro": "Nenhuma coluna encontrada após pular 5 linhas."
                    })
                elif total_rows_after_skip == 0:
                    print(f"  ⚠️ Arquivo vazio após pular 5 linhas.\n")
                    all_column_records.append({
                        "Arquivo": filename,
                        "Coluna": "N/A (Arquivo vazio)",
                        "Quantidade de Registros": 0,
                        "Total de Linhas do Arquivo (após pular)": 0,
                        "Status": "Vazio",
                        "Detalhes do Erro": ""
                    })
                else:
                    print(f"  📊 Linhas após pular 5: {total_rows_after_skip}")
                    for column in df.columns:
                        col_count = df[column].count()
                        all_column_records.append({
                            "Arquivo": filename,
                            "Coluna": column,
                            "Quantidade de Registros": col_count,
                            "Total de Linhas do Arquivo (após pular)": total_rows_after_skip,
                            "Status": "Sucesso",
                            "Detalhes do Erro": ""
                        })
                    print(f"  ✅ {len(df.columns)} colunas processadas.\n")
        except Exception as e:
            print(f"❌ Erro ao processar '{filename}': {e}\n")
            all_column_records.append({
                "Arquivo": filename,
                "Coluna": "N/A (Erro na leitura)",
                "Quantidade de Registros": 0,
                "Total de Linhas do Arquivo (após pular)": 0,
                "Status": "Erro na leitura",
                "Detalhes do Erro": str(e)
            })

    # --- Geração do relatório final ---
    if all_column_records:
        output_df = pd.DataFrame(all_column_records)

        final_cols_order = [
            "Arquivo",
            "Coluna",
            "Quantidade de Registros",
            "Total de Linhas do Arquivo (após pular)",
            "Status",
            "Detalhes do Erro"
        ]
        output_df = output_df.reindex(columns=final_cols_order)

        output_df.to_excel(output_filepath, index=False)
        print(f"\n✅ Processamento concluído com sucesso!")
        print(f"📂 Arquivo salvo em:\n{output_filepath}\n")
    else:
        print("\n⚠️ Nenhum arquivo 'eLAW' foi encontrado ou processado.")


# === CONFIGURAÇÕES ===
source_folder = r'G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE'
destination_folder = r'G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P04 - Suporte\Mapping de colunas e quantidades'

# === EXECUÇÃO ===
process_folder_files(source_folder, destination_folder)
