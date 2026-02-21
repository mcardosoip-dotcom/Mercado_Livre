import os
import shutil
import time

# ==============================================================================
# CONFIGURAÇÃO DOS ENDEREÇOS
# ==============================================================================
pasta_origem = r"C:\Users\SeuUsuario\Caminho\Origem"
pasta_destino = r"G:\Drives compartilhados\Caminho\Destino"

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

def mover_com_detalhes():
    print("\n" + "="*60)
    print("🤖 INICIANDO O ROBÔ DE TRANSFERÊNCIA")
    print("="*60 + "\n")

    # 1. Validação das pastas
    print("🔍 Verificando pastas...")
    if not os.path.exists(pasta_origem):
        print(f"❌ ERRO CRÍTICO: Pasta de origem não existe:\n   -> {pasta_origem}")
        return
    if not os.path.exists(pasta_destino):
        print(f"❌ ERRO CRÍTICO: Pasta de destino (GDrive) não encontrada:\n   -> {pasta_destino}")
        return
    print("✅ Pastas localizadas com sucesso!\n")

    # 2. Listagem
    print(f"📂 Lendo conteúdo da pasta local: {os.path.basename(pasta_origem)}...")
    lista_itens = os.listdir(pasta_origem)
    total_itens = len(lista_itens)
    
    if total_itens == 0:
        print("🤷‍♂️ A pasta de origem está vazia. Nada a fazer.")
        return

    print(f"🔢 Total de itens encontrados: {total_itens}\n")
    print("-" * 60)

    movidos = 0
    erros = 0
    ignorados = 0

    # 3. Loop de Transferência
    for i, item in enumerate(lista_itens, 1):
        caminho_origem = os.path.join(pasta_origem, item)
        caminho_destino = os.path.join(pasta_destino, item)

        # Barra visual de separação entre arquivos
        print(f"\nProcessando item {i}/{total_itens}: '{item}'")

        if os.path.isfile(caminho_origem):
            print(f"Tipo: Arquivo identificado.")
            
            try:
                print(f"   🚀 Iniciando transferência para o GDrive...")
                # O comando move faz a cópia e depois deleta o original
                shutil.move(caminho_origem, caminho_destino)
                
                print(f"   🏁 Upload/Movimentação finalizada.")
                print(f"   ✅ STATUS: Sucesso! Arquivo está na pasta 2.")
                movidos += 1
                
            except Exception as e:
                print(f"   ❌ STATUS: Falha ao mover.")
                print(f"   ⚠️ Detalhe do erro: {e}")
                erros += 1
        else:
            print(f"   📂 Tipo: Pasta (Diretório).")
            print(f"   ⏭️ Ação: Ignorado (o script move apenas arquivos soltos).")
            ignorados += 1
            
        # Pequena pausa para você conseguir ler o log (opcional, pode remover se quiser rapidez máxima)
        time.sleep(0.5) 

    # 4. Relatório Final
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print(f"✅ Arquivos movidos: {movidos}")
    print(f"⏭️ Pastas ignoradas: {ignorados}")
    print(f"❌ Erros encontrados: {erros}")
    print("="*60)
    print("👋 Processo encerrado.")

if __name__ == "__main__":
    mover_com_detalhes()