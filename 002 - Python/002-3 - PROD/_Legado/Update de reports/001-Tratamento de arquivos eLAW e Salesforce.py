# ================================================
# Descrição :  Considerando que as bases estão devidamente baixadas (eLAW e Salesforce) 
#              pelo processo de RPA, este processo faz a movimentação dos arquivos para 
#              a pasta correta e também a padronização de nomes
# Autor : Marcelo Cardoso
# ================================================

import os
import re
import shutil
import difflib
from datetime import datetime
from coda_processo_geral import inserir_dados

# === INICIALIZAÇÃO DE VARIÁVEIS ===
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio_execucao = datetime.now()
status_execucao = "Processamento Ok"

try:
    # === PARTE 1: Salesforce ===
    origem_salesforce = r"C:\Users\mcard\Desktop\Salesforce Bases"
    destino_salesforce = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download Salesforce"

    mapa_renomeacao = {
        "Backlog Informativos HSP": "Pending Informativos",
        "Incoming Embargos": "Incoming Embargos",
        "Incoming Oficios": "Incoming Oficios",
        "Out oficios (NO BCRA)": "Outcoming Ofícios",
        "Outgoing embargos": "Outgoing Embargos",
        "Pending Embargos (BCRA e não BCRA)": "Pending Embargos (BCRA e não BCRA)"
    }

    print("Iniciando tratamento de arquivos Salesforce...")

    for nome_arquivo in os.listdir(origem_salesforce):
        if nome_arquivo.endswith(".csv"):
            caminho_antigo = os.path.join(origem_salesforce, nome_arquivo)
            nome_base = nome_arquivo.split("_")[0].strip() + ".csv"
            novo_nome = mapa_renomeacao.get(nome_base.replace(".csv", ""), nome_base.replace(".csv", "")) + ".csv"
            caminho_novo = os.path.join(destino_salesforce, novo_nome)
            shutil.move(caminho_antigo, caminho_novo)
            print(f"Salesforce - Renomeado e movido: {nome_arquivo} -> {novo_nome}")

    # === PARTE 2: eLAW ===
    pasta_origem_elaw = r"C:\Users\mcard\Desktop\eLAW Bases"
    pasta_destino_elaw = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Download eLAW"

    log_dir = r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo"
    os.makedirs(log_dir, exist_ok=True)
    LOG_FILE = os.path.join(log_dir, "LOG_Ajustar_arquivos_corrompidos_eLAW.txt")

    def logar(mensagem):
        print(mensagem)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(mensagem + "\n")

    hora_inicio_log = datetime.now()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"### LOG INICIADO - {hora_inicio_log.strftime('%Y-%m-%d %H:%M:%S')} ###\n\n")

    logar("Step 1 - Início da limpeza e ajuste de nomes de arquivos...")

    depara = {
        "Brasil_Parcial_Incoming": "Temp_Database_8_Report_eLAW_Contencioso_Brasil_Parcial",
        "Brasil_Parcial_Outgoing": "Temp_Database_4_Report_eLAW_Contencioso_Brasil_Parcial_Outgoing",
        "Contencioso_-_Base_Ativa.": "Temp_Database_16_Report_eLAW_Base_Ativa",
        "Contencioso_-_Hispanos_Completo.": "Temp_Database_10_Report_eLAW_Contencioso_Hispanos_Completa",
        "Extracao_de_informacoes_garantia_DR.": "Temp_Database_20_Report_eLAW_Pagamentos_e_garantia",
        "Extracao_de_Informacoes_Multas_Procon": "Temp_Database_23_Report_eLAW_Extracao_multas",
        "Obrigacoes_de_Fazer_-_Relatorio_Automatico": "Temp_Database_26_Report_eLAW_Obrigacoes_de_Fazer",
        "Tarefas_Agendadas_-_Aguardando_informacoes": "Temp_Database_22_Report_eLAW_Tarefas_Agendadas_Aguardando_Informações",
        "Tarefas_Agendadas_-_Subsidios_Hispanos_CAP": "Temp_Database_17_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_CAP",
        "Tarefas_Agendadas_-_Subsidios_Hispanos_CAP_(Operacao_Hisp)": "Temp_Database_3_Report_eLAW_Acompanhamento_de_tarefas_CORP_CX",
        "Tarefas_Agendadas_-_Subsidios_Hispanos_DR": "Temp_Database_18_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_DR",
        "Tarefas_Agendadas_-_Subsidios_Hispanos_OPS": "Temp_Database_19_Report_eLAW_Tarefas_Agendadas_-_Subsidios_Hispanos_OPS",
        "Tarefas_Agendamento_Clean_-_Confirmados_2025": "Temp_Database_25_Report_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados",
        "Tarefas_Agendamento_Clean_-_Pendentes_2025": "Temp_Database_25_Report_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes"
    }

    remover_se_parecido = [
        "Tarefas_Agendadas_-_Complementacao_de_Cadastro",
        "Tarefas_Agendadas_-_Divergencia_de_Empresas",
        "Audiencia_-_Amelia"
    ]

    arquivos_para_mover = []

    for nome_arquivo in os.listdir(pasta_origem_elaw):
        caminho_completo = os.path.join(pasta_origem_elaw, nome_arquivo)
        if os.path.isfile(caminho_completo) and nome_arquivo.endswith(".xlsx"):
            nome_base = re.sub(r'-\d+(?=\.xlsx$)', '', nome_arquivo)

            if any(nome_base.startswith(remover) for remover in remover_se_parecido):
                os.remove(caminho_completo)
                logar(f"Removido por descarte automático: {nome_arquivo}")
                continue

            match = difflib.get_close_matches(nome_base, depara.keys(), n=1, cutoff=0.7)
            if match:
                novo_nome = depara[match[0]] + ".xlsx"
                caminho_renomeado = os.path.join(pasta_origem_elaw, novo_nome)

                if os.path.exists(caminho_renomeado):
                    if os.path.getmtime(caminho_completo) > os.path.getmtime(caminho_renomeado):
                        os.remove(caminho_renomeado)
                        os.rename(caminho_completo, caminho_renomeado)
                        logar(f"Substituído arquivo (novo mais recente): {nome_arquivo} -> {novo_nome}")
                        arquivos_para_mover.append(caminho_renomeado)
                    else:
                        os.remove(caminho_completo)
                        logar(f"Removido arquivo (antigo descartado): {nome_arquivo}")
                else:
                    os.rename(caminho_completo, caminho_renomeado)
                    logar(f"Renomeado: {nome_arquivo} -> {novo_nome}")
                    arquivos_para_mover.append(caminho_renomeado)
            else:
                logar(f"[AVISO] Sem correspondência de renomeação: {nome_arquivo}")

    logar("\nStep 1 concluído.\n")

    logar("Step 2 - Início da movimentação de arquivos para pasta destino...")
    for caminho_arquivo in arquivos_para_mover:
        if not os.path.exists(caminho_arquivo):
            logar(f"[AVISO] Arquivo não encontrado para mover: {os.path.basename(caminho_arquivo)}")
            continue
        try:
            destino_final = os.path.join(pasta_destino_elaw, os.path.basename(caminho_arquivo))
            if os.path.exists(destino_final):
                os.remove(destino_final)
            shutil.move(caminho_arquivo, destino_final)
            logar(f"Movido para destino: {os.path.basename(caminho_arquivo)}")
        except Exception as e:
            logar(f"[ERRO] Falha ao mover {os.path.basename(caminho_arquivo)}: {str(e)}")
    logar("\nStep 2 concluído.\n")

    logar("Step 3 - Início da remoção de arquivos residuais não tratados...")
    for nome_arquivo in os.listdir(pasta_origem_elaw):
        caminho_completo = os.path.join(pasta_origem_elaw, nome_arquivo)
        if os.path.isfile(caminho_completo) and nome_arquivo.endswith(".xlsx"):
            os.remove(caminho_completo)
            logar(f"Removido residual: {nome_arquivo}")
    logar("\nStep 3 concluído.\n")

except Exception as e:
    status_execucao = "Falha no processamento"
    logar(f"[ERRO FATAL] {str(e)}")

finally:
    hora_fim_execucao = datetime.now()
    logar(f"### LOG FINALIZADO - {hora_fim_execucao.strftime('%Y-%m-%d %H:%M:%S')} ###")
    logar(f"Duração total do processo: {str(hora_fim_execucao - hora_inicio_execucao)}")
    inserir_dados(
        data_atual,
        "Movimentação de arquivos baixados por RPA",
        hora_inicio_execucao.strftime("%H:%M:%S"),
        hora_fim_execucao.strftime("%H:%M:%S"),
        status_execucao,
        "Diário"
    )
