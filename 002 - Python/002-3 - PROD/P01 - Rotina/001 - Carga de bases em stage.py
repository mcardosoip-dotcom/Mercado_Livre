import os
import shutil

# Caminhos de pastas
pasta_elaw = r"C:\Users\mcard\Desktop\eLAW Bases"
pasta_elaw_d1 = r"C:\Users\mcard\Desktop\eLAW Bases D-1"
pasta_salesforce = r"C:\Users\mcard\Desktop\Salesforce Bases"
pasta_stage_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"

# MODIFICAÇÃO AQUI: Altere pasta_destino_elaw para ser igual a pasta_stage_base
pasta_destino_elaw = pasta_stage_base
pasta_destino_salesforce = pasta_stage_base
pasta_congelados = os.path.join(pasta_stage_base, "Congelados")

# Etapa 0: Verifica se as pastas de origem existem
print("🔍 Verificando pastas de origem...")
for pasta, nome in [(pasta_elaw, "eLAW Bases"), (pasta_elaw_d1, "eLAW Bases D-1"), (pasta_salesforce, "Salesforce Bases")]:
    if os.path.exists(pasta):
        try:
            num_arquivos = len([f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))])
            print(f"✔ {nome}: {num_arquivos} arquivo(s) encontrado(s)")
        except:
            print(f"⚠ {nome}: Erro ao acessar pasta")
    else:
        print(f"⚠ {nome}: Pasta não encontrada em {pasta}")

# Etapa 1: Prepara pastas de destino
print("\n🧹 Preparando pastas de destino...")

# Limpa pastas de destino (STAGE)
for pasta in [pasta_destino_elaw, pasta_destino_salesforce]:
    os.makedirs(pasta, exist_ok=True)
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)
    print(f"🧹 Pasta limpa: {pasta}")

# Mapeamento prefixos → nome final
mapeamento_prefixo = {

    # === eLAW - Dedicado Amélia ===
    "Audiencia_-_Amelia": "Database_eLAW_Amelia",
    "Seguimiento_RPA_-_Amelia_New":"Database_eLAW_Seguimiento_RPA_Tarefas",
    "Seguimiento_RPA_-_Amelia_Pagos":"Database_eLAW_Seguimiento_RPA_Pagos",


    # === eLAW - Audiências e Tarefas ===
    "Tarefas_Agendadas_-_Subsidios_Hispanos_CAP_(Operacao_Hisp)": "Database_eLAW_Acompanhamento_de_tarefas_CORP_CX",
    "Tarefas_Agendadas_-_Subsidios_Hispanos_CAP-": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP",
    "Tarefas_Agendadas_-_Subsidios_Hispanos_DR": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR",
    "Tarefas_Agendadas_-_Subsidios_Hispanos_OPS": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS",
    "Tarefas_Agendadas_-_Divergencia_de_Empresas": "Database_eLAW_Divergencia_empresas",
    "Tarefas_Agendadas_-_Aguardando_informacoes": "Database_eLAW_Tarefas_Agendadas_Aguardando_Informações",
    # Nomes canônicos em STAGE: Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados | _Pendentes
    "Tarefas_Agendamento_Clean_-_Confirmados": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados",
    "Tarefas_Agendamento_Clean_-_Pendentes": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes",
    "Tarefas_Agendamento_Clean_(Audiencia)":"Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias",
    "Tarefas_Agendamento_Clean_-_Garantias":"Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias",

     # === eLAW -Outras extrações ===
    "Relatorio_de_Garantia_-_Veiculo":"Relatorio_de_Garantia_Veiculo",

    # === eLAW - Contencioso ===
    "Brasil_Parcial_Outgoing": "Database_eLAW_Contencioso_Brasil_Outgoing",
    "Hispanos_Parcial_Outgoing": "Database_eLAW_Contencioso_Hispanos_Outgoing",

    "Contencioso_-_Base_Ativa_Brasil": "Database_eLAW_Contencioso_Brasil_Ongoing",
    "Contencioso_-_Base_Ativa_Hispanos": "Database_eLAW_Contencioso_Hispanos_Ongoing",

    "Hispanos_Parcial_Incoming": "Database_eLAW_Contencioso_Hispanos_Incoming",
    "Brasil_Parcial_Incoming": "Database_eLAW_Contencioso_Brasil_Incoming",

    # === eLAW - Outros relatórios ===
    #"Extracao_de_informacoes_garantia_DR": "Database_eLAW_Pagamentos_e_garantia",
    "Extracao_de_Informacoes_Multas_Procon_(Ativos)": "Database_eLAW_Extracao_multas",
    "Obrigacoes_de_Fazer_-_Relatorio_Automatico": "Database_eLAW_Obrigacoes_de_Fazer",

    # === Salesforce ===
    "Incoming Embargos_": "Salesforce_Incoming_Embargos",
    "Incoming Oficios_": "Salesforce_Incoming_Oficios",
    "Out oficios (NO BCRA)_": "Salesforce_Outcoming_Ofícios",
    "Outgoing embargos_": "Salesforce_Outgoing_Embargos",
    "Pending Embargos (BCRA e não BCRA)_": "Salesforce_Pending_Embargos_BCRA_e_não_BCRA",
    "Backlog Informativos HSP_": "Salesforce_Pending_Informativos",
    "BCRA - OE x ISSUE_": "Salesforce_BCRA_OE_ISSUE",
    "Report Embargos": "Salesforce_Report_Embargos_Revisao"
}

# Prefixos alternativos para match quando o export gera nome ligeiramente diferente (ex.: sem "_-_").
# Destino em STAGE deve permanecer: Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados / _Pendentes
prefixos_alternativos = {
    "Tarefas_Agendamento_Clean_-_Confirmados": ["Tarefas_Agendamento_Clean_Confirmados"],
    "Tarefas_Agendamento_Clean_-_Pendentes": ["Tarefas_Agendamento_Clean_Pendentes"],
}

# ---
# CORREÇÃO AQUI: Função para buscar arquivos com prioridade
# ---

def _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
    """Retorna True se o arquivo corresponde ao prefixo principal ou a algum alternativo."""
    if nome.startswith(prefixo):
        return True
    for alt in prefixos_alt:
        if nome.startswith(alt):
            return True
    return False

# Busca arquivos por prefixo e lista de pastas
def buscar_arquivos_por_prefixo(prefixo, pastas, prefixos_alt=None):
    prefixos_alt = prefixos_alt or []
    arquivos_encontrados = []

    # 1. Tenta encontrar o arquivo na primeira pasta (prioritária)
    if os.path.exists(pastas[0]):
        try:
            for nome in os.listdir(pastas[0]):
                caminho_completo = os.path.join(pastas[0], nome)
                if os.path.isfile(caminho_completo) and _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
                    return [caminho_completo]
        except PermissionError:
            print(f"⚠ Erro de permissão ao acessar: {pastas[0]}")
    else:
        print(f"⚠ Pasta não encontrada: {pastas[0]}")

    # 2. Se não encontrar na primeira pasta, tenta na segunda
    if len(pastas) > 1:
        if os.path.exists(pastas[1]):
            try:
                for nome in os.listdir(pastas[1]):
                    caminho_completo = os.path.join(pastas[1], nome)
                    if os.path.isfile(caminho_completo) and _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
                        arquivos_encontrados.append(caminho_completo)
            except PermissionError:
                print(f"⚠ Erro de permissão ao acessar: {pastas[1]}")
        else:
            if len(pastas) > 1:
                print(f"⚠ Pasta não encontrada: {pastas[1]}")

    return arquivos_encontrados

# ---
# O restante do código não precisa de alterações
# ---

# Etapa 2: Processa os arquivos mapeados
print(f"\n📋 Processando {len(mapeamento_prefixo)} arquivos mapeados...")
for prefixo, novo_nome_base in mapeamento_prefixo.items():
    # Decide tipo de origem pela PASTA associada ao prefixo
    if novo_nome_base.startswith("Salesforce_"):
        pastas_busca = [pasta_salesforce]
        pasta_destino = pasta_destino_salesforce
    else:
        pastas_busca = [pasta_elaw, pasta_elaw_d1]
        pasta_destino = pasta_destino_elaw
    
    prefixos_alt = prefixos_alternativos.get(prefixo, [])
    caminhos_arquivos = buscar_arquivos_por_prefixo(prefixo, pastas_busca, prefixos_alt)

    if caminhos_arquivos:
        for caminho_arquivo in caminhos_arquivos:
            origem_pasta = os.path.dirname(caminho_arquivo)
            nome_original = os.path.basename(caminho_arquivo)
            ext = os.path.splitext(caminho_arquivo)[1]
            novo_nome = f"{novo_nome_base}{ext}"
            
            destino_stage = os.path.join(pasta_destino, novo_nome)

            # Copia para o destino (STAGE) com o novo nome
            # O arquivo original na pasta desktop mantém o nome original
            shutil.copy2(caminho_arquivo, destino_stage)
            print(f"✔ Copiado para STAGE: {nome_original} -> {novo_nome}")
            
            print(f"   Arquivo original mantido na origem: {nome_original}")
    else:
        # Debug: lista arquivos das pastas para identificar o nome exato e ajustar o mapeamento
        arquivos_disponiveis = []
        for pasta in pastas_busca:
            if os.path.exists(pasta):
                try:
                    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
                    if arquivos:
                        prefixo_parts = prefixo.split('_')[:3]  # Primeiras partes do prefixo
                        similares = [f for f in arquivos if any(part in f for part in prefixo_parts if part)][:5]
                        if similares:
                            arquivos_disponiveis.extend([(pasta, s) for s in similares])
                except Exception:
                    pass

        print(f"⚠ Arquivo não encontrado para prefixo: {prefixo}")
        if arquivos_disponiveis:
            # Mostra nomes exatos para conferir caractere a caractere com o mapeamento
            nomes_unicos = list(dict.fromkeys([os.path.basename(a[1]) for a in arquivos_disponiveis]))[:5]
            print(f"   Nomes exatos de arquivos similares (conferir com o mapeamento):")
            for n in nomes_unicos:
                print(f"      {n}")

# Etapa 3: Copia congelados
if os.path.exists(pasta_congelados):
    for nome in os.listdir(pasta_congelados):
        origem = os.path.join(pasta_congelados, nome)
        destino_stage = os.path.join(pasta_destino_elaw, nome) # Também será copiado para pasta_stage_base
        if os.path.isfile(origem):
            shutil.copy2(origem, destino_stage)
            print(f"📥 Congelado copiado para STAGE: {nome}")
else:
    print("⚠ Pasta 'Congelados' não encontrada.")

print("✅ Processo finalizado com sucesso.")