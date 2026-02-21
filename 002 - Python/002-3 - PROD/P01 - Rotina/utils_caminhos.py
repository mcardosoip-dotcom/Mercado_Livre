# ================================================
# UTILITÁRIO DE CAMINHOS CROSS-PLATFORM
# ================================================
# Autor     : Marcelo Cardoso
# Data      : 2026-01-06
# Atualizado: 2026-02-20 — suporte Mac/Windows completo
#
# PROPÓSITO:
#   Centraliza a adaptação de caminhos para diferentes sistemas operacionais.
#   Pode ser importado por qualquer script que precise de caminhos adaptados.
# ================================================

import os
import platform


def _get_base_path():
    """
    Retorna o caminho base do projeto adaptado ao SO.

    Returns:
        str: Caminho base do projeto (Legales_Analytics)
    """
    sistema = platform.system()

    if sistema == "Darwin":  # macOS
        return "/Users/mcardoso/Library/CloudStorage/GoogleDrive-marcelo.cardoso@mercadolivre.com/Drives compartilhados/Legales_Analytics"
    else:  # Windows ou outros
        return r"G:\Drives compartilhados\Legales_Analytics"


# ================================================
# CAMINHOS DE REDE / SHARED DRIVE
# ================================================

def get_caminho_base_rotina():
    """Retorna o caminho base da pasta P01 - Rotina."""
    return os.path.join(_get_base_path(), "002 - Python", "002-3 - PROD", "P01 - Rotina")


def get_caminho_prod():
    """Retorna o caminho do diretório 002-3 - PROD."""
    return os.path.join(_get_base_path(), "002 - Python", "002-3 - PROD")


def get_caminho_stage():
    """Retorna o caminho do diretório STAGE."""
    return os.path.join(_get_base_path(), "001 - Base", "STAGE")


def get_caminho_bases_locais():
    """Retorna o caminho das bases principais locais (destino do bucket)."""
    return os.path.join(_get_base_path(), "000 - Bases Principais locais")


def get_caminho_mapeamento_excel():
    """Retorna o caminho do arquivo de mapeamento de disponibilidade de bases."""
    return os.path.join(_get_base_path(), "001 - Base", "Mapeamento_do_que_esperamos.xlsx")


def get_caminho_status_validacao():
    """Retorna o caminho do arquivo de status de validação de colunas."""
    return os.path.join(
        _get_base_path(),
        "001 - Base", "STAGE", "Padrão de bases e colunas", "status_validacao.txt"
    )


# ================================================
# SCRIPTS FINAIS (PBD)
# ================================================

def get_caminho_script_pbd():
    """Retorna o caminho do script PBD principal (Legal Spend - Processo Completo)."""
    return os.path.join(
        _get_base_path(),
        "007 - Legal Spend and Overheads",
        "Controles gerais de financas",
        "Pagamentos",
        "000 - Processo completo pagamento.py"
    )


def get_caminho_script_pbd_m5():
    """Retorna o caminho do script PBD M5 (Arquivos tratados)."""
    return os.path.join(
        _get_base_path(),
        "003 - Dashboards",
        "LA PBD - Controle de pagamentos",
        "Arquivos tratados",
        "000 - Processo completo.py"
    )


# ================================================
# CAMINHOS DO DESKTOP (BASES LOCAIS DO USUÁRIO)
# ================================================

def get_desktop():
    """
    Retorna o caminho do Desktop do usuário (cross-platform).

    Windows: C:\\Users\\<usuario>\\Desktop
    macOS  : /Users/<usuario>/Desktop
    """
    return os.path.join(os.path.expanduser("~"), "Desktop")


def get_pastas_desktop_bases():
    """
    Retorna dicionário com os caminhos das pastas de bases no Desktop.

    Returns:
        dict com chaves: 'elaw', 'elaw_d1', 'salesforce'
    """
    desktop = get_desktop()
    return {
        "elaw":       os.path.join(desktop, "eLAW Bases"),
        "elaw_d1":    os.path.join(desktop, "eLAW Bases D-1"),
        "salesforce": os.path.join(desktop, "Salesforce Bases"),
    }


def get_pastas_limpar_desktop():
    """
    Retorna lista de pastas do Desktop que devem ser limpas após ETL bem-sucedido.

    Returns:
        list de caminhos absolutos
    """
    desktop = get_desktop()
    return [
        os.path.join(desktop, "Salesforce Bases"),
        os.path.join(desktop, "eLAW Bases"),
        os.path.join(desktop, "eLAW Bases D-1"),
    ]


# ================================================
# CAMINHOS DAS BASES DE DADOS (PARQUETS)
# ================================================

def get_caminho_bases_sf():
    """Retorna o caminho da pasta de bases Salesforce (001-02 - SF)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-02 - SF")


def get_caminho_bases_elaw():
    """Retorna o caminho da pasta de bases eLAW (001-01 - eLAW)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-01 - eLAW")


def get_caminho_bases_dimensoes():
    """Retorna o caminho da pasta de bases Dimensões (001-00 - Dimensões)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-00 - Dimensões")


def get_caminho_bases_quebra_sigilo():
    """Retorna o caminho da pasta de bases Quebra de Sigilo (001-03 - Quebra de Sigilo)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-03 - Quebra de Sigilo")


def get_caminho_bases_quebra_sigilo_entrada():
    """Retorna o caminho da pasta de entrada Quebra de Sigilo (001-99 - Outras Fontes/Quebra de sigilo)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-99 - Outras Fontes", "Quebra de sigilo")


def get_caminho_bases_consumidor_gov():
    """Retorna o caminho da pasta de bases Consumidor.gov (001-99 - Outras Fontes/Consumidor.gov)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-99 - Outras Fontes", "Consumidor.gov")


def get_caminho_bases_clm_docusign():
    """Retorna o caminho da pasta de bases CLM_DocuSign (001-99 - Outras Fontes/CLM_DocuSign)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-99 - Outras Fontes", "CLM_DocuSign")


# ================================================
# CAMINHOS STAGE ESPECÍFICOS
# ================================================

def get_caminho_stage_clm():
    """Retorna o caminho da pasta STAGE/CLM Database."""
    return os.path.join(_get_base_path(), "001 - Base", "STAGE", "CLM Database")


def get_caminho_dimensoes_stage():
    """Retorna o caminho da pasta Stage das Dimensões (001-00 - Dimensões/Stage)."""
    return os.path.join(_get_base_path(), "001 - Base", "001-00 - Dimensões", "Stage")


# ================================================
# CAMINHOS MESA DE ENTRADA
# ================================================

def get_caminho_mesa_entrada_buffer():
    """Retorna o caminho da pasta Buffer da Mesa de entrada."""
    return os.path.join(
        get_caminho_base_rotina(),
        "MAIN", "CARGA DE TABELAS", "Mesa de entrada", "Buffer"
    )


def get_caminho_mesa_entrada_log():
    """Retorna o caminho do arquivo de log da Mesa de entrada."""
    return os.path.join(
        get_caminho_base_rotina(),
        "MAIN", "CARGA DE TABELAS", "Mesa de entrada", "LOG_execucao_mesa_entrada.txt"
    )