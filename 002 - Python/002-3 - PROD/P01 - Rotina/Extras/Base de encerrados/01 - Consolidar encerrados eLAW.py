import pandas as pd
import glob
import os
import unicodedata
from concurrent.futures import ProcessPoolExecutor, as_completed

# Para leitura ainda mais rápida dos xlsx: pip install python-calamine
# Diretórios com os arquivos xlsx (entrada) – Encerrados e Entradas
diretorio_encerrados = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Extras\Histórico Contencioso\Encerrados"
diretorio_entradas = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Extras\Histórico Contencioso\Entradas"
# Diretório onde o resultado consolidado será salvo (parquet + amostra xlsx)
diretorio_saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Extras\Histórico Contencioso\Consolidado"
# Cópia do parquet para Legado_eLAW (usado em demais processos)
diretorio_legado_parquet = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Legado_eLAW\Parquet"


def normalizar_nome_coluna(nome: str) -> str:
    """Remove acentos e substitui espaços por underscore para encaixar em banco de dados."""
    if not isinstance(nome, str):
        return str(nome)
    # Remove acentos (NFD decompõe, depois remove caracteres de combinação)
    nfkd = unicodedata.normalize("NFKD", nome)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Substitui espaços por underscore e remove outros caracteres problemáticos
    sem_acento = sem_acento.strip().replace(" ", "_").replace("-", "_")
    # Remove caracteres que não são alfanuméricos ou underscore
    return "".join(c for c in sem_acento if c.isalnum() or c == "_") or "coluna"


def _ler_um_excel(arquivo: str):
    """Lê um arquivo xlsx (uso em processo paralelo). Tenta calamine (rápido), depois openpyxl."""
    try:
        try:
            df = pd.read_excel(arquivo, skiprows=5, engine="calamine")
        except Exception:
            df = pd.read_excel(arquivo, skiprows=5)
        df["arquivo_origem"] = os.path.basename(arquivo)
        return (arquivo, df, len(df))
    except Exception as e:
        return (arquivo, None, str(e))


if __name__ == "__main__":
    # Buscar todos os arquivos xlsx nos dois diretórios (Encerrados + Entradas)
    arquivos_xlsx = []
    for d in (diretorio_encerrados, diretorio_entradas):
        if os.path.isdir(d):
            arquivos_xlsx.extend(glob.glob(os.path.join(d, "*.xlsx")))
    arquivos_xlsx = sorted(set(arquivos_xlsx))  # sem repetir caminho
    print(f"Encontrados {len(arquivos_xlsx)} arquivos para consolidar (Encerrados + Entradas).")

    # Ler arquivos em paralelo (acelera bastante quando há vários xlsx)
    lista_dfs = []
    n_workers = min(8, max(1, (os.cpu_count() or 4)))
    print(f"Lendo em paralelo com {n_workers} processos...")
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futuras = {executor.submit(_ler_um_excel, arq): arq for arq in arquivos_xlsx}
        for fut in as_completed(futuras):
            arq, df, info = fut.result()
            nome = os.path.basename(arq)
            if df is not None:
                lista_dfs.append(df)
                print(f"  OK: {nome} ({info} linhas)")
            else:
                print(f"  ERRO em {nome}: {info}")

    # Consolidar todos os DataFrames
    if lista_dfs:
        print(f"\n{'='*60}")
        print("Consolidando todos os arquivos...")
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)

        print(f"\nBase consolidada criada com sucesso!")
        print(f"  - Total de registros: {len(df_consolidado)}")
        print(f"  - Total de colunas: {len(df_consolidado.columns)}")
        # Normalizar nomes das colunas (sem acentos, espaços -> underscore)
        nomes_originais = list(df_consolidado.columns)
        nomes_novos = [normalizar_nome_coluna(c) for c in nomes_originais]
        vistos = {}
        nomes_unicos = []
        for n in nomes_novos:
            if n in vistos:
                vistos[n] += 1
                nomes_unicos.append(f"{n}_{vistos[n]}")
            else:
                vistos[n] = 0
                nomes_unicos.append(n)
        df_consolidado.columns = nomes_unicos
        print(f"\nColunas após normalização (sem acentos, espaços -> underscore):")
        for i, (antigo, novo) in enumerate(zip(nomes_originais, nomes_unicos), 1):
            print(f"  {i}. {antigo!r} -> {novo!r}" if antigo != novo else f"  {i}. {novo}")

        # Regras pós-consolidação: 1) apenas um registro por ID; 2) remover Status = Ativo
        if "ID" in df_consolidado.columns:
            n_antes = len(df_consolidado)
            df_consolidado = df_consolidado.drop_duplicates(subset=["ID"], keep="first")
            print(f"\nDuplicatas por ID removidas: {n_antes - len(df_consolidado)} (restam {len(df_consolidado)} registros).")
        if "Status" in df_consolidado.columns:
            n_antes = len(df_consolidado)
            # Comparar como string, ignorando maiúsculas e espaços
            status_str = df_consolidado["Status"].astype(str).str.strip().str.lower()
            df_consolidado = df_consolidado[status_str != "ativo"]
            print(f"Registros com Status = Ativo removidos: {n_antes - len(df_consolidado)} (restam {len(df_consolidado)} registros).")

        os.makedirs(diretorio_saida, exist_ok=True)

        # Colunas de data: padronizar no formato DD/MM/YYYY
        for col in df_consolidado.columns:
            if pd.api.types.is_datetime64_any_dtype(df_consolidado[col]):
                # Já é datetime -> formatar e tratar NaT
                df_consolidado[col] = pd.to_datetime(df_consolidado[col], errors="coerce").dt.strftime("%d/%m/%Y")
                df_consolidado[col] = df_consolidado[col].fillna("")
            elif df_consolidado[col].dtype == object:
                # Object: tentar interpretar como data (dayfirst=True = DD/MM/YYYY)
                s = pd.to_datetime(df_consolidado[col], dayfirst=True, errors="coerce", utc=True)
                mask = s.notna()
                if mask.any():
                    if pd.api.types.is_datetime64_any_dtype(s):
                        df_consolidado.loc[mask, col] = s.loc[mask].dt.strftime("%d/%m/%Y").values
                    else:
                        # Série object (ex.: timezones mistos): formatar valor a valor
                        df_consolidado.loc[mask, col] = s.loc[mask].apply(
                            lambda x: x.strftime("%d/%m/%Y") if hasattr(x, "strftime") else str(x)
                        ).values

        # Colunas object com tipos mistos quebram o PyArrow; converter para string.
        obj_cols = df_consolidado.select_dtypes(include=["object"]).columns.tolist()
        if obj_cols:
            df_consolidado[obj_cols] = df_consolidado[obj_cols].fillna("").astype(str)

        # Base COMPLETA apenas em parquet (não salvar xlsx da base inteira - fica lento)
        nome_parquet = "Base_Consolidada_Encerrados_eLAW.parquet"
        arquivo_parquet = os.path.join(diretorio_saida, nome_parquet)
        print(f"\nSalvando base completa (PARQUET apenas): {arquivo_parquet}")
        df_consolidado.to_parquet(arquivo_parquet, index=False)

        # Cópia do parquet em Legado_eLAW/Parquet para uso em demais processos
        os.makedirs(diretorio_legado_parquet, exist_ok=True)
        arquivo_parquet_legado = os.path.join(diretorio_legado_parquet, nome_parquet)
        print(f"Salvando cópia em Legado_eLAW/Parquet: {arquivo_parquet_legado}")
        df_consolidado.to_parquet(arquivo_parquet_legado, index=False)

        # Apenas amostra de 1000 linhas em xlsx (exemplo do conteúdo do parquet)
        n_amostra = min(1000, len(df_consolidado))
        arquivo_amostra = os.path.join(diretorio_saida, "Base_Consolidada_Encerrados_eLAW_amostra_1000.xlsx")
        print(f"Salvando amostra de {n_amostra} linhas (xlsx): {arquivo_amostra}")
        df_consolidado.head(n_amostra).to_excel(arquivo_amostra, index=False, engine='openpyxl')

        print(f"\n{'='*60}")
        print("Consolidação concluída com sucesso!")
        print(f"  Base completa: .parquet | Amostra: .xlsx ({n_amostra} linhas)")

        # Exibir primeiras linhas como preview
        print(f"\nPreview das primeiras 5 linhas:")
        print(df_consolidado.head())

    else:
        print("\nNenhum arquivo foi lido com sucesso. Verifique os arquivos.")
