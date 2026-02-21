import os
import glob
import pandas as pd
from unidecode import unidecode
import re

# --- 1. Definição dos Caminhos ---
SOURCE_DIR = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\CLM Database"
TARGET_DIR = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-99 - Outras Fontes\CLM_DocuSign"

# DICIONÁRIO DE MAPEAMENTO FINAL
FILENAME_MAP = {
    "Control de contratos": "CLM_control_de_contratos",
    "Métricas de contratos": "CLM_metricas_de_contrato",
    "Métricas de flujos activos": "CLM_metricas_de_flujos_activos"
}

# --- 2. Funções Auxiliares (Sem Alterações) ---

def normalize_column_name(col_name: str) -> str:
    """Normaliza o nome da coluna para o padrão de banco de dados."""
    name = col_name.strip().lower()
    name = unidecode(name)
    name = re.sub(r'[^\w]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name

def find_latest_folder(directory: str) -> str:
    """Encontra o caminho completo da subpasta modificada mais recentemente."""
    try:
        list_of_subdirs = [
            os.path.join(directory, d) 
            for d in os.listdir(directory) 
            if os.path.isdir(os.path.join(directory, d))
        ]
        if not list_of_subdirs:
            print(f"Erro: Nenhuma subpasta encontrada em {directory}")
            return None
        latest_folder = max(list_of_subdirs, key=os.path.getmtime)
        print(f"Pasta mais recente encontrada: {latest_folder}")
        return latest_folder
    except FileNotFoundError:
        print(f"Erro: O diretório de origem não foi encontrado: {directory}")
        return None
    except Exception as e:
        print(f"Um erro ocorreu ao encontrar a pasta mais recente: {e}")
        return None

# --- 3. Processamento Principal (COM VERIFICAÇÃO DE DUPLICIDADE) ---
def process_latest_files_to_parquet():
    """Executa o fluxo de trabalho com controle de duplicidade no nome de destino."""
    
    latest_folder_path = find_latest_folder(SOURCE_DIR)
    
    if not latest_folder_path:
        return

    file_pattern = os.path.join(latest_folder_path, '*.csv')
    files_to_process = glob.glob(file_pattern)
    
    if not files_to_process:
        print(f"Aviso: Nenhúm arquivo .csv encontrado em {latest_folder_path}")
        return
        
    os.makedirs(TARGET_DIR, exist_ok=True)

    print(f"\nIniciando a conversão de {len(files_to_process)} arquivos...")

    # Conjunto para rastrear nomes de arquivos Parquet de destino já utilizados
    processed_targets = set()

    for file_path in files_to_process:
        file_name = os.path.basename(file_path)
        print(f"  Processando: {file_name}")

        try:
            # 1. Tentar ler o arquivo
            df = pd.read_csv(file_path, sep=',') 
        except Exception as e:
            print(f"    ERRO ao ler {file_name}: {e}. Pulando este arquivo.")
            continue

        # 2. Renomeação do Arquivo de Destino
        new_file_base_name = None
        normalized_file_name = unidecode(file_name.lower())
        
        for original_key, target_value in FILENAME_MAP.items():
            normalized_key = unidecode(original_key.lower())
            
            if normalized_key in normalized_file_name:
                new_file_base_name = target_value
                break
        
        if new_file_base_name is None:
            # Fallback para arquivos não mapeados (ainda gera o prefixo "unmapped_")
            clean_name = normalize_column_name(file_name.split('.')[0])
            new_file_base_name = f"unmapped_{clean_name}"
        
        target_parquet_name = f"{new_file_base_name}.parquet"
        
        # 3. VERIFICAÇÃO DE DUPLICIDADE (A nova lógica)
        if target_parquet_name in processed_targets:
            print(f"    AVISO: O arquivo {file_name} mapeia para o destino {target_parquet_name}, que JÁ FOI PROCESSADO nesta execução. O arquivo duplicado será IGNORADO.")
            continue # Pula para o próximo arquivo de origem
        
        # Marca o nome de destino como processado
        processed_targets.add(target_parquet_name)

        target_parquet_path = os.path.join(TARGET_DIR, target_parquet_name)

        # 4. Normalização dos Nomes das Colunas
        df.columns = [normalize_column_name(col) for col in df.columns]

        # 5. Salvar como Parquet (Sobrescrevendo o arquivo anterior no destino se ele existir)
        df.to_parquet(target_parquet_path, engine='pyarrow', index=False)
        
        print(f"  SUCESSO: Salvo como: {target_parquet_path}")

    print("\nProcesso concluído! 🎉")

# --- 4. Execução do Código ---
if __name__ == "__main__":
    process_latest_files_to_parquet()