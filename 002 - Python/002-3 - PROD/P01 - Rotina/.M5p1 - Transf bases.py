import os
import shutil
import subprocess
import sys
import pandas as pd
from datetime import datetime

# ==========================================
# DEFINIÇÃO DE CAMINHOS
# ==========================================
caminho_desktop = r"C:\Users\Administrator\Desktop"

pasta_elaw = os.path.join(caminho_desktop, "eLAW Bases")
pasta_elaw_d1 = os.path.join(caminho_desktop, "eLAW Bases D-1")
pasta_salesforce = os.path.join(caminho_desktop, "Salesforce Bases")
pasta_backup = os.path.join(caminho_desktop, "Backup Bases")

pasta_stage_base = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE"
pasta_destino_elaw = pasta_stage_base
pasta_destino_salesforce = pasta_stage_base
pasta_congelados = os.path.join(pasta_stage_base, "Congelados")

# ==========================================
# ETAPA 0: BACKUP DAS PASTAS
# ==========================================
print("--- INICIANDO BACKUP ---")

# Garante que a pasta de backup existe
os.makedirs(pasta_backup, exist_ok=True)

pastas_para_backup = [
    (pasta_salesforce, "Salesforce Bases"),
    (pasta_elaw, "eLAW Bases"),
    (pasta_elaw_d1, "eLAW Bases D-1")
]

for pasta_origem, nome_pasta in pastas_para_backup:
    destino_backup = os.path.join(pasta_backup, nome_pasta)
    
    # Remove a pasta de backup específica se existir (mantém estrutura)
    if os.path.exists(destino_backup):
        try:
            shutil.rmtree(destino_backup)
            print(f"Backup antigo removido: {nome_pasta}")
        except Exception as e:
            print(f"Erro ao remover backup antigo de {nome_pasta}: {e}")
    
    # Realiza o backup se a pasta de origem existir
    if os.path.exists(pasta_origem):
        try:
            shutil.copytree(pasta_origem, destino_backup)
            print(f"Backup realizado: {nome_pasta}")
        except Exception as e:
            print(f"Erro ao copiar {nome_pasta}: {e}")
    else:
        print(f"Pasta de origem não encontrada para backup: {pasta_origem}")

# ==========================================
# ETAPA 1: LIMPEZA DAS PASTAS DE DESTINO (STAGE)
# ==========================================
for pasta in [pasta_destino_elaw, pasta_destino_salesforce]:
    os.makedirs(pasta, exist_ok=True)
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            try:
                os.remove(caminho)
            except PermissionError:
                print(f"Arquivo não removido (em uso?): {arquivo}")
    print(f"Pasta STAGE limpa: {pasta}")

# ==========================================
# MAPEAMENTO E LÓGICA DE PROCESSAMENTO
# ==========================================
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
    "Tarefas_Agendamento_Clean_-_Confirmados_2025": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados",
    "Tarefas_Agendamento_Clean_-_Pendentes_2025": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes",
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


def buscar_arquivos_por_prefixo(prefixo, pastas):
    for pasta in pastas:
        if os.path.exists(pasta):
            for nome in os.listdir(pasta):
                if nome.startswith(prefixo):
                    return os.path.join(pasta, nome)
    return None

# ==========================================
# ETAPA 2: PROCESSAMENTO (MOVE + RENAME PARA STAGE)
# ==========================================
print("--- MOVENDO E RENOMEANDO ARQUIVOS PARA STAGE ---")

for prefixo, novo_nome_base in mapeamento_prefixo.items():
    if novo_nome_base.startswith("Salesforce_"):
        pastas_busca = [pasta_salesforce]
        pasta_destino = pasta_destino_salesforce
    else:
        pastas_busca = [pasta_elaw, pasta_elaw_d1]
        pasta_destino = pasta_destino_elaw

    caminho_arquivo = buscar_arquivos_por_prefixo(prefixo, pastas_busca)

    if not caminho_arquivo:
        print(f"Arquivo não encontrado para prefixo: {prefixo}")
        continue

    ext = os.path.splitext(caminho_arquivo)[1]
    novo_nome = f"{novo_nome_base}{ext}"
    destino_stage = os.path.join(pasta_destino, novo_nome)

    try:
        shutil.move(caminho_arquivo, destino_stage)
        print(f"Movido para STAGE: {novo_nome}")
    except Exception as e:
        print(f"Erro ao mover {caminho_arquivo}: {e}")

# ==========================================
# ETAPA 3: COPIA CONGELADOS
# ==========================================
if os.path.exists(pasta_congelados):
    for nome in os.listdir(pasta_congelados):
        origem = os.path.join(pasta_congelados, nome)
        destino = os.path.join(pasta_stage_base, nome)
        if os.path.isfile(origem):
            shutil.copy2(origem, destino)
            print(f"Congelado copiado: {nome}")
else:
    print("Pasta 'Congelados' não encontrada.")

# ==========================================
# ETAPA 4: LIMPEZA DO DESKTOP
# ==========================================
for arquivo in os.listdir(caminho_desktop):
    if arquivo.startswith("Relatorio_") and arquivo.endswith(".xlsx"):
        try:
            os.remove(os.path.join(caminho_desktop, arquivo))
            print(f"Deletado do Desktop: {arquivo}")
        except Exception as e:
            print(f"Erro ao deletar {arquivo}: {e}")

# ==========================================
# ETAPA 5: CHAMADA DE PROCESSO EXTERNO (COM LOG)
# ==========================================
print("--- INICIANDO PROCESSO EXTERNO: Summary_Amelia ---")

summary_script = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\Extras\Summary_Amelia.py"

if os.path.exists(summary_script):
    try:
        resultado = subprocess.run(
            [sys.executable, summary_script],
            capture_output=True,
            text=True
        )

        print("---- STDOUT ----")
        if resultado.stdout:
            print(resultado.stdout)
        else:
            print("(sem saída)")

        print("---- STDERR ----")
        if resultado.stderr:
            print(resultado.stderr)
        else:
            print("(sem erros)")

        if resultado.returncode == 0:
            print("Summary_Amelia finalizado com sucesso")
        else:
            print(f"Summary_Amelia finalizou com erro. Código: {resultado.returncode}")

    except Exception as e:
        print(f"Erro inesperado ao executar Summary_Amelia: {e}")
else:
    print(f"Script não encontrado: {summary_script}")

# ==========================================
# ETAPA 6: CONFRONTO DE DISPONIBILIDADE
# ==========================================
print("--- EXECUTANDO CONFRONTO DE DISPONIBILIDADE ---")

caminho_excel = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\Mapeamento_do_que_esperamos.xlsx"

df_base = pd.read_excel(caminho_excel, sheet_name="Database")
nome_coluna = df_base.columns[0]
lista_mestra = df_base[nome_coluna].astype(str)

arquivos_stage = {
    os.path.splitext(f)[0]
    for f in os.listdir(pasta_stage_base)
    if os.path.isfile(os.path.join(pasta_stage_base, f))
}

status = {x: ("OK" if x in arquivos_stage else "PENDENTE") for x in lista_mestra}
df_base["Status_Arquivo"] = lista_mestra.map(status)

df_hist = pd.read_excel(caminho_excel, sheet_name="Historico")
coluna_data = datetime.now().strftime("%d/%m/%Y %H:%M")
df_hist[coluna_data] = df_hist.iloc[:, 0].astype(str).map(status)

with pd.ExcelWriter(caminho_excel, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    df_base.to_excel(writer, sheet_name="Database", index=False)
    df_hist.to_excel(writer, sheet_name="Historico", index=False)

# ==========================================
# ETAPA 7: LIMPEZA DAS PASTAS DE ORIGEM
# ==========================================
# NOTA: As pastas "Salesforce Bases", "eLAW Bases" e "eLAW Bases D-1" 
# não são limpas para preservar os arquivos originais no desktop
print("--- LIMPEZA FINAL DAS PASTAS DE ORIGEM ---")
print("(Pastas do desktop preservadas: Salesforce Bases, eLAW Bases, eLAW Bases D-1)")

print("Fluxo finalizado.")
