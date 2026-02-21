"""
Step 5 – Processo CLM por FTP: converte os CSVs baixados (04) em Parquet.
Lê da pasta mais recente em STAGE/CLM Database e grava em 001-99 - Outras Fontes/CLM_DocuSign.
Baseado em CLM_DocuSign/001 - Conversao em parquet.py
"""
import os
import glob
import pandas as pd
from unidecode import unidecode
import re

SOURCE_DIR = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\CLM Database"
TARGET_DIR = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\CLM_DocuSign"

FILENAME_MAP = {
    "Control de contratos": "CLM_control_de_contratos",
    "Métricas de contratos": "CLM_metricas_de_contrato",
    "Métricas de flujos activos": "CLM_metricas_de_flujos_activos",
}


def normalize_column_name(col_name: str) -> str:
    """Normaliza o nome da coluna para o padrão de banco de dados."""
    name = col_name.strip().lower()
    name = unidecode(name)
    name = re.sub(r"[^\w]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def find_latest_folder(directory: str) -> str:
    """Retorna o caminho completo da subpasta modificada mais recentemente."""
    try:
        subdirs = [
            os.path.join(directory, d)
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
        if not subdirs:
            print(f"Erro: Nenhuma subpasta em {directory}")
            return None
        latest = max(subdirs, key=os.path.getmtime)
        print(f"Pasta mais recente: {latest}")
        return latest
    except FileNotFoundError:
        print(f"Erro: Diretório não encontrado: {directory}")
        return None
    except Exception as e:
        print(f"Erro ao buscar pasta mais recente: {e}")
        return None


def process_latest_files_to_parquet():
    """Converte CSVs da pasta mais recente em STAGE/CLM Database para Parquet em CLM_DocuSign."""
    latest_folder_path = find_latest_folder(SOURCE_DIR)
    if not latest_folder_path:
        return

    file_pattern = os.path.join(latest_folder_path, "*.csv")
    files_to_process = glob.glob(file_pattern)
    if not files_to_process:
        print(f"Aviso: Nenhum .csv em {latest_folder_path}")
        return

    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"\nConvertendo {len(files_to_process)} arquivo(s)...")
    processed_targets = set()

    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        print(f"  Processando: {file_name}")

        try:
            df = pd.read_csv(file_path, sep=",")
        except Exception as e:
            print(f"    ERRO ao ler {file_name}: {e}. Pulando.")
            continue

        normalized_file_name = unidecode(file_name.lower())
        new_file_base_name = None
        for original_key, target_value in FILENAME_MAP.items():
            normalized_key = unidecode(original_key.lower())
            if normalized_key in normalized_file_name:
                new_file_base_name = target_value
                break
        if new_file_base_name is None:
            clean_name = normalize_column_name(file_name.split(".")[0])
            new_file_base_name = f"unmapped_{clean_name}"

        target_parquet_name = f"{new_file_base_name}.parquet"
        if target_parquet_name in processed_targets:
            print(f"    AVISO: Destino {target_parquet_name} já processado. Ignorando duplicata.")
            continue
        processed_targets.add(target_parquet_name)

        target_parquet_path = os.path.join(TARGET_DIR, target_parquet_name)
        df.columns = [normalize_column_name(col) for col in df.columns]
        df.to_parquet(target_parquet_path, engine="pyarrow", index=False)
        print(f"  SUCESSO: {target_parquet_path}")

    print("\nStep 5 concluído.")


if __name__ == "__main__":
    process_latest_files_to_parquet()
