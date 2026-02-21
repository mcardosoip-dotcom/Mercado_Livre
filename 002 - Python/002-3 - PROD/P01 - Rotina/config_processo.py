# ================================================
# CONFIGURAÇÃO CENTRAL DO PROCESSO COMPLETO
# ================================================
# Autor     : Marcelo Cardoso
# Data      : 2026-01-06
# 
# PROPÓSITO:
#   Este arquivo centraliza TODAS as configurações do processo de ETL/rotina,
#   incluindo caminhos, sequência de execução e scripts auxiliares.
#
# USO:
#   - Importado por: 000 - Processo completo.py (orquestrador principal)
#   - Importado por: LA Processos.py (interface gráfica GUI)
#
# FLUXO DO PROCESSO COMPLETO (Máquina Local):
#   1. Backup → 2. Carga Stage → 3. Extras (Amélia) → 4. Confronto 
#   → 5. Validação → 6. Limpeza (parquets) → 7. ETL → 8. Download Bucket 
#   → 9. CODA Input → (se ETL OK) Limpeza Desktop + Legal Spend Consolidado (009)
# ================================================

import os


# ================================================
# SEÇÃO 1: CAMINHOS BASE DO PROJETO
# ================================================

# Diretório principal onde estão os scripts da rotina
CAMINHO_BASE = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina"

# Diretório pai (002-3 - PROD) - usado para scripts em outras pastas do mesmo nível
CAMINHO_PROD = os.path.dirname(CAMINHO_BASE)


# ================================================
# SEÇÃO 2: ARQUIVOS DE CONTROLE E STATUS
# ================================================

# Arquivo de status criado pela etapa de Validação (Passador)
# O orquestrador lê este arquivo para verificar se a validação passou (deve conter "OK")
CAMINHO_STATUS_VALIDACAO = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Padrão de bases e colunas\status_validacao.txt"


# ================================================
# SEÇÃO 3: SCRIPTS FINAIS (EXECUTADOS APÓS ETL)
# ================================================

# Script Legal Spend - Consolidado executado ao final do processo completo (após ETL bem-sucedido)
# Orquestra: Contingências, Honorários e Pagamentos (009)
SCRIPT_FINAL_PBD = r"G:\Drives compartilhados\Legales_Analytics\009 - Legal Spend and Overheads\Controles gerais de financas\000 - Processo Completo Consolidado.py"

# Script PBD alternativo (usado em outros contextos, ex.: Máquina 5 - Arquivos tratados)
SCRIPT_FINAL_PBD_M5 = r"G:\Drives compartilhados\Legales_Analytics\003 - Dashboards\LA PBD - Controle de pagamentos\Arquivos tratados\000 - Processo completo.py"


# ================================================
# SEÇÃO 4: DEFINIÇÃO DA SEQUÊNCIA DE EXECUÇÃO
# ================================================
# 
# STEPS_PROCESSO_COMPLETO: Define a ordem e configuração de cada etapa do processo
#
# Estrutura de cada step:
#   - nome: Descrição legível da etapa (exibida no console)
#   - script: Caminho do script Python (relativo a CAMINHO_BASE ou absoluto)
#   - checkpoint: Tipo de validação após execução
#       * None = sem validação
#       * "validacao" = exige que status_validacao.txt contenha "OK"
#       * "etl_sucesso" = marca que o ETL principal foi concluído
#   - skip_in_loop: Se True, não executa no loop principal (será tratado depois)
#       * False = executa normalmente na sequência
#       * True = será executado separadamente (ex.: limpeza ao final)
#
# IMPORTANTE: A ordem dos steps define a sequência de execução!
# ================================================

STEPS_PROCESSO_COMPLETO = [
    # Etapa 1: Backup das bases extraídas
    {
        "nome": "Backup",
        "script": r"Backup de bases extraidas\Backup.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
    
    # Etapa 2: Carrega bases em stage
    {
        "nome": "Carga Stage",
        "script": "001 - Carga de bases em stage.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
    
    # Etapa 3: Processa extras (Summary Amélia)
    {
        "nome": "Extras (Summary Amélia)",
        "script": r"Extras\Summary_Amelia.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
    
    # Etapa 4: Confronta disponibilidade de dados
    {
        "nome": "Confronto disponibilidade",
        "script": "002 - Confronto_de_disponibilidade.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
    
    # Etapa 5: Validação de processo (gera status_validacao.txt)
    {
        "nome": "Validação de processo",
        "script": r"Passador\002 - Validação de processo.py",
        "checkpoint": "validacao",  # Exige que status_validacao.txt contenha "OK"
        "skip_in_loop": False
    },
    
    # Etapa 6: Limpeza de parquets (executada separadamente ao final)
    {
        "nome": "Limpeza (parquets)",
        "script": "003 - Limpeza de pastas.py",
        "checkpoint": None,
        "skip_in_loop": True  # Não executa no loop, será chamada via função ao final
    },
    
    # Etapa 7: ETL principal (transformação e carga dos dados)
    {
        "nome": "ETL principal",
        "script": "004 - ETL de arquivos.py",
        "checkpoint": "etl_sucesso",  # Marca que ETL foi concluído com sucesso
        "skip_in_loop": False
    },
    
    # Etapa 8: Download do bucket (sincronização com nuvem)
    {
        "nome": "Download Bucket",
        "script": r"..\Download de banco\002 - Download Bucket.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
    
    # Etapa 9: CODA Input (processamento adicional)
    {
        "nome": "CODA Input",
        "script": r"CODA - Input.py",
        "checkpoint": None,
        "skip_in_loop": False
    },
]


# ================================================
# SEÇÃO 5: CONFIGURAÇÕES DE LIMPEZA
# ================================================

# Pastas do Desktop que serão limpas (arquivos deletados) após o ETL bem-sucedido
# A limpeza ocorre ANTES da execução do script PBD final
PASTAS_PARA_LIMPAR_DESKTOP = [
    r"C:\Users\mcard\Desktop\Salesforce Bases",
    r"C:\Users\mcard\Desktop\eLAW Bases",
    r"C:\Users\mcard\Desktop\eLAW Bases D-1",
]


# ================================================
# SEÇÃO 6: FUNÇÕES AUXILIARES PARA CAMINHOS
# ================================================

def _path(*parts):
    """
    Constrói caminho absoluto a partir de CAMINHO_BASE.
    
    Exemplo:
        _path("MAIN", "Salesforce", "script.py")
        → "G:\...\P01 - Rotina\MAIN\Salesforce\script.py"
    """
    return os.path.normpath(os.path.join(CAMINHO_BASE, *parts))


def _path_prod(*parts):
    """
    Constrói caminho absoluto a partir de CAMINHO_PROD (002-3 - PROD).
    
    Exemplo:
        _path_prod("Download de banco", "script.py")
        → "G:\...\002-3 - PROD\Download de banco\script.py"
    """
    return os.path.normpath(os.path.join(CAMINHO_PROD, *parts))


# ================================================
# SEÇÃO 7: SCRIPTS PARA INTERFACE GRÁFICA (GUI)
# ================================================
# Estes caminhos são usados pela interface gráfica LA Processos.py
# ================================================

# Script orquestrador principal (este é o processo completo)
SCRIPT_PROCESSO_COMPLETO = os.path.join(CAMINHO_BASE, "000 - Processo completo.py")

# Processos pontuais: cargas individuais de tabelas específicas
# Formato: (nome_exibido_na_gui, caminho_do_script)
PROCESSOS_PONTUAIS = [
    ("Carga Dimensões", _path("DIM", "000 - Carga de dados dimensoes.py")),
    ("eLAW atual", _path("MAIN", "CARGA DE TABELAS", "eLAW", "000 - Carga de dados eLAW.py")),
    ("eLAW Legado", _path("MAIN", "CARGA DE TABELAS", "eLAW", "Legado", "001 - Executa_conversão_em_massa.py")),
    ("Carga CLM", _path("MAIN", "CARGA DE TABELAS", "CLM_DocuSign", "000 - Processo completo.py")),
    ("Salesforce", _path("MAIN", "CARGA DE TABELAS", "Salesforce", "000 - Carga de dados Salesforce.py")),
    ("Salesforce Full", _path("MAIN", "CARGA DE TABELAS", "Salesforce", "XXX_Salesforce_Full.py")),
    ("Quebra de Sigilo", _path("MAIN", "CARGA DE TABELAS", "Quebra de sigilo", "000 - Carga de dados QS.py")),
    ("Consumidor.gov", _path("MAIN", "CARGA DE TABELAS", "Consumidor.gov", "000 - Carga de dados Gov.py")),
    ("Mesa de entrada", _path("MAIN", "CARGA DE TABELAS", "Mesa de entrada", "000_Push_e_carga_mesa_de_entrada.py")),
]

# Scripts específicos da Máquina 5
SCRIPT_M5P1_TRANSF_BASES = _path(".M5p1 - Transf bases.py")
SCRIPT_M5P2_PROCESSO_COMPLETO = _path(".M5p2 - Processo completo.py")

# Script de download de bucket (usado em outros contextos além do processo completo)
SCRIPT_DOWNLOAD_BUCKET = _path_prod("Download de banco", "002 - Download Bucket.py")
