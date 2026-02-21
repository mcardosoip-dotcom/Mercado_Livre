# ================================================
# Descrição :  Mapeamento de fontes para conversão de Excel para Parquet
#              Define o mapeamento entre arquivos Excel de origem e 
#              arquivos Parquet de destino, incluindo a aba do Excel.
# Autor : Marcelo Cardoso
# ================================================

# Lista de mapeamentos: cada item contém:
# - "Endereco": caminho da pasta onde está o arquivo Excel
# - "Arquivo": nome do arquivo Excel (sem extensão .xlsx)
# - "Aba": nome da aba do Excel a ser processada
# - "Arquivo final": nome do arquivo Parquet final (sem extensão .parquet)

MAPEAMENTO_FONTES = [
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Acompanhamento_de_tarefas_CORP_CX",
        "Aba": "Tarefas (Agendamentos)",
        "Arquivo final": "Database_eLAW_Acompanhamento_de_tarefas_CORP_CX"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Amelia",
        "Aba": "Audiencia - Amelia 2",
        "Arquivo final": "Database_eLAW_Amelia"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Brasil_Incoming",
        "Aba": "Extração Marcelo (Contencioso2)",
        "Arquivo final": "Database_eLAW_Contencioso_Brasil_Incoming"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Brasil_Ongoing",
        "Aba": "Extração Marcelo (contencioso2)",
        "Arquivo final": "Database_eLAW_Contencioso_Brasil_Ongoing"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Brasil_Outgoing",
        "Aba": "Marcelo Contencioso 2",
        "Arquivo final": "Database_eLAW_Contencioso_Brasil_Outgoing"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Hispanos_Incoming",
        "Aba": "Extração Marcelo (contencioso2)",
        "Arquivo final": "Database_eLAW_Contencioso_Hispanos_Incoming"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Hispanos_Ongoing",
        "Aba": "Ativa - Hispanos",
        "Arquivo final": "Database_eLAW_Contencioso_Hispanos_Ongoing"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Contencioso_Hispanos_Outgoing",
        "Aba": "Hispanos - Encerrados",
        "Arquivo final": "Database_eLAW_Contencioso_Hispanos_Outgoing"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Divergencia_empresas",
        "Aba": "Tarefas em divergência II",
        "Arquivo final": "Database_eLAW_Divergencia_empresas"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Extracao_multas",
        "Aba": "Multa",
        "Arquivo final": "Database_eLAW_Extracao_multas"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Obrigacoes_de_Fazer",
        "Aba": "Obrigações de Fazer",
        "Arquivo final": "Database_eLAW_Obrigacoes_de_Fazer"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Pagamentos_e_garantia",
        "Aba": "Relatório Pagamentos e Garantia",
        "Arquivo final": "Database_eLAW_Pagamentos_e_garantia"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Seguimiento_RPA_Pagos",
        "Aba": "Pagamentos",
        "Arquivo final": "Database_eLAW_Seguimiento_RPA_Pagos"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Seguimiento_RPA_Tarefas",
        "Aba": "Tarefas",
        "Arquivo final": "Database_eLAW_Seguimiento_RPA_Tarefas"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Aguardando_Informações",
        "Aba": "Tarefas - Vic",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Aguardando_Informações"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP",
        "Aba": "Tarefas (Agendamentos) CAP",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP",
        "Aba": "Tarefas (Agendamentos) CAP CX",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP_CX"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR",
        "Aba": "Tarefas (Agendamentos)",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS",
        "Aba": "Tarefas (Agendamentos) - Enligh",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Enli"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS",
        "Aba": "Tarefas (Agendamentos) - Interv",
        "Arquivo final": "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Inter"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias",
        "Aba": "Tarefas Agendamento Clean",
        "Arquivo final": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados",
        "Aba": "Tarefas Agendamento Clean",
        "Arquivo final": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias",
        "Aba": "Tarefas Agendamento Garantias",
        "Arquivo final": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Legado",
        "Aba": "Tarefas Agendamento Clean",
        "Arquivo final": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Legado"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes",
        "Aba": "Tarefas Agendamento Clean",
        "Arquivo final": "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Relatorio_de_Garantia_Veiculo",
        "Aba": "Relatório de Garantia - Veículo",
        "Arquivo final": "Relatorio_de_Garantia_Veiculo"
    }
]
