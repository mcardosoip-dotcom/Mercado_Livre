from google.cloud import storage
import os
import sys

# Adiciona o diretório da rotina ao path para importar utils_caminhos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "P01 - Rotina"))

from utils_caminhos import get_caminho_bases_locais

# === Parâmetros ===
bucket_name = "pdme000426"
gcs_folder_path = "Projeto banco de dados/Exports_csvs/"
local_folder_path = get_caminho_bases_locais()

# === Garante que a pasta de destino existe ===
os.makedirs(local_folder_path, exist_ok=True)

# === Conexão com GCS ===
print(f"📂 Listando arquivos em: gs://{bucket_name}/{gcs_folder_path}")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

blobs = bucket.list_blobs(prefix=gcs_folder_path)

# === Itera e baixa cada arquivo ===
for blob in blobs:
    if blob.name.endswith("/"):  # pula "pastas" vazias
        continue
    local_filename = os.path.join(local_folder_path, os.path.basename(blob.name))
    print(f"⬇ Baixando {blob.name} para {local_filename}")
    blob.download_to_filename(local_filename)

print("✅ Todos os arquivos foram baixados com sucesso.")
