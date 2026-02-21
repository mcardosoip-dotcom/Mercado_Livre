import os
import pandas as pd
from datetime import datetime

# --- 1. Configurações ---
caminho_excel = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\Mapeamento_do_que_esperamos.xlsx"
aba_base = "Database"
aba_hist = "Historico"

# --- Mapeamento de Prefixos (mesmo do arquivo 001 - Carga de bases em stage.py) ---
mapeamento_prefixo = {
    # === eLAW - Dedicado Amélia ===
    "Audiencia_-_Amelia": "Database_eLAW_Amelia",
    "Seguimiento_RPA_-_Amelia_New": "Database_eLAW_Seguimiento_RPA_Tarefas",
    "Seguimiento_RPA_-_Amelia_Pagos": "Database_eLAW_Seguimiento_RPA_Pagos",
    
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
    "Tarefas_Agendamento_Clean_(Audiencia)": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias",
    "Tarefas_Agendamento_Clean_-_Garantias": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias",
    
    # === eLAW - Outras extrações ===
    "Relatorio_de_Garantia_-_Veiculo": "Relatorio_de_Garantia_Veiculo",
    
    # === eLAW - Contencioso ===
    "Brasil_Parcial_Outgoing": "Database_eLAW_Contencioso_Brasil_Outgoing",
    "Hispanos_Parcial_Outgoing": "Database_eLAW_Contencioso_Hispanos_Outgoing",
    "Contencioso_-_Base_Ativa_Brasil": "Database_eLAW_Contencioso_Brasil_Ongoing",
    "Contencioso_-_Base_Ativa_Hispanos": "Database_eLAW_Contencioso_Hispanos_Ongoing",
    "Hispanos_Parcial_Incoming": "Database_eLAW_Contencioso_Hispanos_Incoming",
    "Brasil_Parcial_Incoming": "Database_eLAW_Contencioso_Brasil_Incoming",
    
    # === eLAW - Outros relatórios ===
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

# Cria mapeamento reverso: nome_final -> prefixo (para busca)
mapeamento_reverso = {v: k for k, v in mapeamento_prefixo.items()}

# Pastas onde os arquivos são procurados
pasta_elaw = r"C:\Users\mcard\Desktop\eLAW Bases"
pasta_elaw_d1 = r"C:\Users\mcard\Desktop\eLAW Bases D-1"
pasta_salesforce = r"C:\Users\mcard\Desktop\Salesforce Bases"

# FORMATO AGORA COM HORA (ex: 06/01/2026 14:30)
coluna_agora = datetime.now().strftime("%d/%m/%Y %H:%M")

# --- 2. Leitura da Base (A AUTORIDADE) ---
print("--- Iniciando ---")
print(f"Lendo aba MESTRA '{aba_base}'...")

try:
    df_base = pd.read_excel(caminho_excel, sheet_name=aba_base)
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O arquivo não existe: {caminho_excel}")
    exit()

if df_base.empty:
    print("ERRO CRÍTICO: A aba 'Database' está vazia. Não há o que processar.")
    exit()

# Identifica o nome da primeira coluna (ex: 'Queremos')
nome_coluna_chave = df_base.columns[0]
print(f"Chave de identificação: '{nome_coluna_chave}'")

# Lista limpa de arquivos esperados
lista_mestra = df_base.iloc[:, 0].dropna().unique()

# --- 3. Varredura nas Pastas (mesma lógica do arquivo 001) ---
print("\nVerificando arquivos nas pastas...")

# Função auxiliar para verificar se nome começa com prefixo ou alternativos
def _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
    """Retorna True se o arquivo corresponde ao prefixo principal ou a algum alternativo."""
    if nome.startswith(prefixo):
        return True
    for alt in prefixos_alt:
        if nome.startswith(alt):
            return True
    return False

# Função para buscar arquivos por prefixo (mesma lógica do arquivo 001)
def buscar_arquivo_por_prefixo(prefixo, pastas, prefixos_alt=None):
    """
    Busca arquivo que começa com o prefixo nas pastas (mesma lógica do arquivo 001).
    Considera prefixos alternativos e prioridade de pastas.
    Retorna True se encontrar, False caso contrário.
    """
    prefixos_alt = prefixos_alt or []
    
    # 1. Tenta encontrar o arquivo na primeira pasta (prioritária)
    if len(pastas) > 0 and os.path.exists(pastas[0]):
        try:
            for nome in os.listdir(pastas[0]):
                caminho_completo = os.path.join(pastas[0], nome)
                if os.path.isfile(caminho_completo) and _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
                    return True
        except PermissionError:
            print(f"  [AVISO] Erro de permissão ao acessar: {pastas[0]}")
        except Exception as e:
            print(f"  [AVISO] Erro ao ler pasta {pastas[0]}: {e}")
    
    # 2. Se não encontrar na primeira pasta, tenta na segunda
    if len(pastas) > 1 and os.path.exists(pastas[1]):
        try:
            for nome in os.listdir(pastas[1]):
                caminho_completo = os.path.join(pastas[1], nome)
                if os.path.isfile(caminho_completo) and _nome_comeca_com_prefixo(nome, prefixo, prefixos_alt):
                    return True
        except PermissionError:
            print(f"  [AVISO] Erro de permissão ao acessar: {pastas[1]}")
        except Exception as e:
            print(f"  [AVISO] Erro ao ler pasta {pastas[1]}: {e}")
    
    return False

# Dicionário com o status atual (usando mapeamento como no arquivo 001)
status_hoje = {}
for nome_final_original in lista_mestra:
    # Preserva o valor original e cria uma versão limpa para busca
    nome_final_limpo = str(nome_final_original).strip()
    
    # Busca o prefixo correspondente no mapeamento reverso
    prefixo_original = mapeamento_reverso.get(nome_final_limpo)
    
    if prefixo_original:
        # Decide tipo de origem pela PASTA associada ao prefixo (mesma lógica do arquivo 001)
        if nome_final_limpo.startswith("Salesforce_"):
            pastas_busca = [pasta_salesforce]
        else:
            pastas_busca = [pasta_elaw, pasta_elaw_d1]
        
        # Obtém prefixos alternativos se existirem
        prefixos_alt = prefixos_alternativos.get(prefixo_original, [])
        
        # Se encontrou o prefixo, busca arquivo que começa com esse prefixo (mesma lógica do arquivo 001)
        encontrado = buscar_arquivo_por_prefixo(prefixo_original, pastas_busca, prefixos_alt)
        status_hoje[nome_final_original] = "OK" if encontrado else "PENDENTE"
    else:
        # Se não está no mapeamento, verifica se existe arquivo com o nome exato (sem extensão)
        # Isso cobre casos de arquivos que não estão no mapeamento
        # Tenta primeiro em eLAW, depois em Salesforce
        encontrado = False
        pastas_verificacao = [pasta_elaw, pasta_elaw_d1, pasta_salesforce]
        for pasta in pastas_verificacao:
            if os.path.exists(pasta):
                try:
                    for nome_arquivo in os.listdir(pasta):
                        if os.path.isfile(os.path.join(pasta, nome_arquivo)):
                            nome_sem_ext = os.path.splitext(nome_arquivo)[0]
                            if nome_sem_ext == nome_final_limpo:
                                encontrado = True
                                break
                    if encontrado:
                        break
                except Exception:
                    pass
        status_hoje[nome_final_original] = "OK" if encontrado else "PENDENTE"

# --- 4. ATUALIZAÇÃO DA ABA DATABASE ---
print(f"Atualizando status na aba '{aba_base}'...")
# Cria ou atualiza a coluna 'Status_Arquivo' na própria base
df_base['Status_Arquivo'] = df_base[nome_coluna_chave].map(status_hoje)
df_base['Status_Arquivo'] = df_base['Status_Arquivo'].fillna("PENDENTE")


# --- 5. PREPARAÇÃO DO HISTÓRICO ---
print(f"Atualizando aba '{aba_hist}' com Data e Hora...")
df_historico = pd.DataFrame()
recriar = False

try:
    df_historico = pd.read_excel(caminho_excel, sheet_name=aba_hist)
    
    if df_historico.empty or len(df_historico.columns) == 0:
        recriar = True
    else:
        # Garante nome da coluna chave
        coluna_real = df_historico.columns[0]
        if coluna_real != nome_coluna_chave:
            df_historico.rename(columns={coluna_real: nome_coluna_chave}, inplace=True)
            
except Exception:
    recriar = True

if recriar:
    df_historico = pd.DataFrame({nome_coluna_chave: []})

# --- 6. SINCRONIZAÇÃO E MERGE ---
# Template baseado na lista Mestra atual
df_template = pd.DataFrame({nome_coluna_chave: lista_mestra})
df_template[nome_coluna_chave] = df_template[nome_coluna_chave].astype(str)

if not df_historico.empty:
    df_historico[nome_coluna_chave] = df_historico[nome_coluna_chave].astype(str)

# Mantém histórico antigo alinhado com a lista atual
df_final_hist = pd.merge(df_template, df_historico, on=nome_coluna_chave, how="left")

# Adiciona a coluna NOVA com DATA e HORA
df_final_hist[coluna_agora] = df_final_hist[nome_coluna_chave].map(status_hoje)
df_final_hist[coluna_agora] = df_final_hist[coluna_agora].fillna("PENDENTE")

# --- 7. SALVAMENTO DUPLO (Database e Histórico) ---
print("Salvando as duas abas no Excel...")

try:
    with pd.ExcelWriter(caminho_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        
        # 1. Salva a Database ATUALIZADA (com a coluna de status preenchida)
        df_base.to_excel(writer, sheet_name=aba_base, index=False)
        
        # 2. Salva o Histórico ATUALIZADO (com a nova coluna de hora)
        df_final_hist.to_excel(writer, sheet_name=aba_hist, index=False)
    
    print("-" * 30)
    print(f"✔ SUCESSO!")
    print(f"  1. Aba '{aba_base}': Status atualizado.")
    print(f"  2. Aba '{aba_hist}': Coluna '{coluna_agora}' adicionada.")
    print("-" * 30)

except PermissionError:
    print("\n❌ ERRO: O arquivo Excel está aberto! Feche e tente novamente.")
except Exception as e:
    print(f"\n❌ Erro ao salvar: {e}")