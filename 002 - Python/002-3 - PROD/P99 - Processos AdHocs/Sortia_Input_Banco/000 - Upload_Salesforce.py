# ============================================================
# PROCESSO AD-HOC - CARGA SALESFORCE
# ============================================================
# Descrição: Processa bases do Salesforce de forma pontual
#            Executa o pipeline completo: conversão, upload e geração de SQL
# Autor: Marcelo Cardoso
# ============================================================

import os
import shutil
import subprocess
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES E CAMINHOS
# ============================================================

# Caminhos Base
pasta_salesforce = r"C:\Users\mcard\Desktop\Salesforce Bases"
pasta_stage_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"
pasta_destino_salesforce = pasta_stage_base
pasta_congelados = os.path.join(pasta_stage_base, "Congelados")

# Caminhos Histórico (BCRA)
PASTA_HISTORICO_BCRA = (
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD"
    r"\P99 - Processos AdHocs\Sortia_Input_Banco\Histórico"
)
NOME_BASE_ARQUIVO_BCRA = "Salesforce_BCRA_OE_ISSUE"

# Caminhos dos Scripts Salesforce
CAMINHO_SCRIPTS_SALESFORCE = (
    r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD"
    r"\P01 - Rotina\MAIN\CARGA DE TABELAS\Salesforce"
)

# Mapeamento de Arquivos Salesforce
mapeamento_prefixo = {
    "Incoming Embargos_": "Salesforce_Incoming_Embargos",
    "Incoming Oficios_": "Salesforce_Incoming_Oficios",
    "Out oficios (NO BCRA)_": "Salesforce_Outcoming_Ofícios",
    "Outgoing embargos_": "Salesforce_Outgoing_Embargos",
    "Pending Embargos (BCRA e não BCRA)_": "Salesforce_Pending_Embargos_BCRA_e_não_BCRA",
    "Backlog Informativos HSP_": "Salesforce_Pending_Informativos",
    "BCRA - OE x ISSUE_": NOME_BASE_ARQUIVO_BCRA,
    "Report Embargos": "Salesforce_Report_Embargos_Revisao",
}

# ============================================================
# CONFIGURAÇÃO DE EXECUÇÃO
# ============================================================
# Defina quais etapas do pipeline executar (True/False)
EXECUTAR_PREPARACAO_ARQUIVOS = True  # ETAPAS 0-3: Backup, limpeza, cópia e congelados
EXECUTAR_CONVERSAO = True            # ETAPA 4.1: Conversão CSV → Parquet
EXECUTAR_UPLOAD_BUCKET = True        # ETAPA 4.2: Upload para GCS Bucket
EXECUTAR_GERACAO_SQL = True          # ETAPA 4.3: Geração de comandos SQL

# ============================================================
# ETAPA 0 – CÓPIA PARA HISTÓRICO BCRA (CRÍTICO: RODAR PRIMEIRO)
# ============================================================
def executar_historico_bcra():
    """
    Busca o arquivo 'Salesforce_BCRA_OE_ISSUE' na pasta STAGE (sobra do dia anterior),
    cria uma cópia datada na pasta de Histórico.
    """
    print("\n" + "="*60)
    print("ETAPA 0 - BACKUP HISTÓRICO BCRA")
    print("="*60)

    # Garante que as pastas existem para evitar erro de leitura
    os.makedirs(pasta_destino_salesforce, exist_ok=True)
    os.makedirs(PASTA_HISTORICO_BCRA, exist_ok=True)

    # Procura arquivos na STAGE que comecem com o nome base
    arquivos_encontrados = [
        f for f in os.listdir(pasta_destino_salesforce)
        if f.startswith(NOME_BASE_ARQUIVO_BCRA) and os.path.isfile(os.path.join(pasta_destino_salesforce, f))
    ]

    if not arquivos_encontrados:
        print(f"⚠ Aviso: Nenhum arquivo '{NOME_BASE_ARQUIVO_BCRA}' encontrado na STAGE para gerar histórico.")
        print("   (Isso é normal na primeira execução ou se a pasta foi limpa manualmente).")
        return

    # Pega o primeiro arquivo encontrado (geralmente só deve haver um)
    nome_atual = arquivos_encontrados[0]
    caminho_origem = os.path.join(pasta_destino_salesforce, nome_atual)
    
    # Define extensão e timestamp
    _, ext = os.path.splitext(nome_atual)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    
    # Nome final: Salesforce_BCRA_OE_ISSUE_2025-12-12_210438.xlsx
    novo_nome = f"{NOME_BASE_ARQUIVO_BCRA}_{timestamp}{ext}"
    caminho_destino = os.path.join(PASTA_HISTORICO_BCRA, novo_nome)

    try:
        shutil.copy2(caminho_origem, caminho_destino)
        print(f"✅ SUCESSO: Arquivo copiado para histórico.")
        print(f"   📂 Origem: {nome_atual}")
        print(f"   📂 Destino: {novo_nome}")
    except Exception as e:
        print(f"❌ ERRO ao copiar para histórico: {e}")

# ============================================================
# ETAPA 1 – LIMPAR STAGE (APENAS ARQUIVOS SALESFORCE)
# ============================================================
def limpar_stage_salesforce():
    """
    Limpa apenas arquivos Salesforce da STAGE.
    Mantém arquivos de outras origens (eLAW, etc).
    """
    print("\n" + "="*60)
    print("ETAPA 1 - LIMPEZA STAGE (SALESFORCE)")
    print("="*60)
    
    if not os.path.exists(pasta_destino_salesforce):
        print(f"⚠ Pasta STAGE não encontrada: {pasta_destino_salesforce}")
        return
    
    arquivos_removidos = 0
    for arquivo in os.listdir(pasta_destino_salesforce):
        caminho = os.path.join(pasta_destino_salesforce, arquivo)
        
        # Evita deletar a pasta Congelados
        if caminho == pasta_congelados:
            continue
        
        # Remove apenas arquivos que começam com "Salesforce_"
        if os.path.isfile(caminho) and arquivo.startswith("Salesforce_"):
            try:
                os.remove(caminho)
                arquivos_removidos += 1
            except PermissionError:
                print(f"⚠ Não foi possível deletar (arquivo aberto?): {arquivo}")
            except Exception as e:
                print(f"⚠ Erro ao deletar {arquivo}: {e}")
    
    print(f"🧹 STAGE limpa: {arquivos_removidos} arquivo(s) Salesforce removido(s)")

# ============================================================
# ETAPA 2 – PROCESSAR NOVOS ARQUIVOS (DO DESKTOP PARA STAGE)
# ============================================================
def buscar_arquivos_por_prefixo(prefixo):
    """Busca arquivos na pasta Salesforce Desktop por prefixo."""
    if not os.path.exists(pasta_salesforce):
        return []
    return [os.path.join(pasta_salesforce, nome) for nome in os.listdir(pasta_salesforce) 
            if nome.startswith(prefixo) and os.path.isfile(os.path.join(pasta_salesforce, nome))]

def processar_arquivos_salesforce():
    """
    Copia arquivos do Desktop para STAGE com nomes padronizados.
    """
    print("\n" + "="*60)
    print("ETAPA 2 - MOVIMENTAÇÃO DE ARQUIVOS SALESFORCE")
    print("="*60)
    
    if not os.path.exists(pasta_salesforce):
        print(f"⚠ Pasta Salesforce não encontrada: {pasta_salesforce}")
        return
    
    arquivos_processados = 0
    for prefixo, novo_nome_base in mapeamento_prefixo.items():
        arquivos = buscar_arquivos_por_prefixo(prefixo)

        if not arquivos:
            print(f"⚠ Arquivo não encontrado na origem: {prefixo}")
            continue

        for caminho_arquivo in arquivos:
            ext = os.path.splitext(caminho_arquivo)[1]
            novo_nome = f"{novo_nome_base}{ext}"

            destino_stage = os.path.join(pasta_destino_salesforce, novo_nome)
            
            # Copia para Stage (usando o novo nome padronizado)
            try:
                shutil.copy2(caminho_arquivo, destino_stage)
                print(f"✔ Copiado para STAGE: {novo_nome}")
                arquivos_processados += 1

                # Renomeia na origem (Desktop) para manter organização
                destino_origem_renomeado = os.path.join(pasta_salesforce, novo_nome)
                if os.path.exists(destino_origem_renomeado) and destino_origem_renomeado != caminho_arquivo:
                    os.remove(destino_origem_renomeado)
                
                if caminho_arquivo != destino_origem_renomeado:
                    try:
                        os.rename(caminho_arquivo, destino_origem_renomeado)
                    except Exception as e:
                        print(f"⚠ Erro ao renomear na origem: {e}")
            except Exception as e:
                print(f"❌ Erro ao copiar {caminho_arquivo}: {e}")
    
    print(f"✅ Total de arquivos processados: {arquivos_processados}")

# ============================================================
# ETAPA 3 – RESTAURAR CONGELADOS
# ============================================================
def restaurar_congelados():
    """
    Restaura arquivos da pasta Congelados para STAGE.
    """
    print("\n" + "="*60)
    print("ETAPA 3 - RESTAURAR CONGELADOS")
    print("="*60)
    
    if not os.path.exists(pasta_congelados):
        print("⚠ Pasta 'Congelados' não encontrada ou vazia.")
        return
    
    arquivos_restaurados = 0
    for nome in os.listdir(pasta_congelados):
        origem = os.path.join(pasta_congelados, nome)
        destino = os.path.join(pasta_destino_salesforce, nome)
        if os.path.isfile(origem):
            try:
                shutil.copy2(origem, destino)
                print(f"📥 Congelado restaurado: {nome}")
                arquivos_restaurados += 1
            except Exception as e:
                print(f"⚠ Erro ao restaurar {nome}: {e}")
    
    print(f"✅ Total de congelados restaurados: {arquivos_restaurados}")

# ============================================================
# ETAPA 4 – PIPELINE DE PROCESSAMENTO SALESFORCE
# ============================================================
def executar_script_salesforce(nome_script, descricao):
    """
    Executa um script do pipeline Salesforce.
    
    Args:
        nome_script: Nome do arquivo Python a ser executado
        descricao: Descrição da etapa para exibição
    """
    caminho_script = os.path.join(CAMINHO_SCRIPTS_SALESFORCE, nome_script)
    
    if not os.path.exists(caminho_script):
        print(f"❌ Script não encontrado: {caminho_script}")
        return False
    
    print(f"\n🔄 {descricao}")
    print(f"   Script: {nome_script}")
    
    try:
        resultado = subprocess.run(
            ["python", caminho_script], 
            check=True,
            capture_output=False
        )
        print(f"✅ {descricao} concluída com sucesso.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na execução de {nome_script}")
        print(f"   Detalhes: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def executar_pipeline_salesforce():
    """
    Executa o pipeline completo de processamento Salesforce:
    1. Conversão CSV → Parquet
    2. Upload para GCS Bucket
    3. Geração de comandos SQL
    """
    print("\n" + "="*60)
    print("ETAPA 4 - PIPELINE DE PROCESSAMENTO SALESFORCE")
    print("="*60)
    
    sucesso_geral = True
    
    # 4.1 - Conversão CSV → Parquet
    if EXECUTAR_CONVERSAO:
        print("\n" + "-"*60)
        sucesso = executar_script_salesforce(
            "001 - Executa_conversão_em_massa.py",
            "Conversão CSV → Parquet"
        )
        if not sucesso:
            sucesso_geral = False
            if not EXECUTAR_UPLOAD_BUCKET and not EXECUTAR_GERACAO_SQL:
                return  # Para se houver erro e não houver mais etapas
    
    # 4.2 - Upload para GCS Bucket
    if EXECUTAR_UPLOAD_BUCKET:
        print("\n" + "-"*60)
        sucesso = executar_script_salesforce(
            "002 - Carga_em_Bucket.py",
            "Upload para GCS Bucket"
        )
        if not sucesso:
            sucesso_geral = False
    
    # 4.3 - Geração de comandos SQL
    if EXECUTAR_GERACAO_SQL:
        print("\n" + "-"*60)
        sucesso = executar_script_salesforce(
            "003 - Criação_de_tabelas.py",
            "Geração de comandos SQL"
        )
        if not sucesso:
            sucesso_geral = False
    
    if sucesso_geral:
        print("\n" + "="*60)
        print("✅ PIPELINE SALESFORCE CONCLUÍDO COM SUCESSO!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("⚠ PIPELINE SALESFORCE CONCLUÍDO COM AVISOS/ERROS")
        print("="*60)
    
    return sucesso_geral

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
def main():
    """
    Função principal que orquestra todo o processo.
    """
    print("\n" + "="*60)
    print("PROCESSO AD-HOC - CARGA SALESFORCE")
    print("="*60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nConfigurações:")
    print(f"  - Preparação de arquivos: {'✅' if EXECUTAR_PREPARACAO_ARQUIVOS else '❌'}")
    print(f"  - Conversão CSV → Parquet: {'✅' if EXECUTAR_CONVERSAO else '❌'}")
    print(f"  - Upload para Bucket: {'✅' if EXECUTAR_UPLOAD_BUCKET else '❌'}")
    print(f"  - Geração SQL: {'✅' if EXECUTAR_GERACAO_SQL else '❌'}")
    
    # ETAPAS 0-3: Preparação de arquivos
    if EXECUTAR_PREPARACAO_ARQUIVOS:
        executar_historico_bcra()
        limpar_stage_salesforce()
        processar_arquivos_salesforce()
        restaurar_congelados()
        print("\n✅ Preparação de arquivos finalizada.")
    else:
        print("\n⚠ Preparação de arquivos desabilitada (configuração).")
    
    # ETAPA 4: Pipeline de processamento
    if EXECUTAR_CONVERSAO or EXECUTAR_UPLOAD_BUCKET or EXECUTAR_GERACAO_SQL:
        executar_pipeline_salesforce()
    else:
        print("\n⚠ Pipeline de processamento desabilitado (configuração).")
    
    print("\n" + "="*60)
    print("PROCESSO FINALIZADO")
    print("="*60)

if __name__ == "__main__":
    main()
