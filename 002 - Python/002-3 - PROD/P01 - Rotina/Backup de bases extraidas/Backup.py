import os
import shutil

# Pastas a copiar
pastas_origem = ["eLAW Bases", "eLAW Bases D-1", "Salesforce Bases"]

# Caminhos
usuario = os.getlogin()
desktop = os.path.join("C:\\Users", usuario, "Desktop")
destino_base = os.path.join(desktop, "Backup Bases")

# Garante que a pasta destino existe
os.makedirs(destino_base, exist_ok=True)

for nome_pasta in pastas_origem:
    origem = os.path.join(desktop, nome_pasta)
    destino = os.path.join(destino_base, nome_pasta)

    if not os.path.exists(origem):
        print(f"⚠️ Pasta de origem não encontrada: {origem}")
        continue

    # Remove a pasta de destino se já existir
    if os.path.exists(destino):
        shutil.rmtree(destino)
        print(f"🗑️ Pasta existente removida: {destino}")

    # Copia a pasta
    try:
        shutil.copytree(origem, destino)
        print(f"✅ Pasta copiada com sucesso: {nome_pasta}")
    except Exception as e:
        print(f"❌ Erro ao copiar a pasta '{nome_pasta}': {e}")
