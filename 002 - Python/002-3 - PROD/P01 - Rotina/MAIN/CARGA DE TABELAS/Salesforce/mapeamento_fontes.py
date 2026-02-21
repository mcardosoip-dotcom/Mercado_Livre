# ================================================
# Descrição :  Mapeamento de fontes para conversão de CSV para Parquet
#              Define o mapeamento entre arquivos CSV de origem e 
#              arquivos Parquet de destino.
# Autor : Marcelo Cardoso
# ================================================

# Lista de mapeamentos: cada item contém:
# - "Endereco": caminho da pasta onde está o arquivo CSV
# - "Arquivo": nome do arquivo CSV (sem extensão .csv)
# - "Arquivo final": nome do arquivo Parquet final (sem extensão .parquet)

MAPEAMENTO_FONTES = [
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_BCRA_OE_ISSUE",
        "Arquivo final": "Salesforce_BCRA_OE_ISSUE"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Incoming_Embargos",
        "Arquivo final": "Salesforce_Incoming_Embargos"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Incoming_Oficios",
        "Arquivo final": "Salesforce_Incoming_Oficios"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Outcoming_Ofícios",
        "Arquivo final": "Salesforce_Outcoming_Ofícios"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Outgoing_Embargos",
        "Arquivo final": "Salesforce_Outgoing_Embargos"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Pending_Embargos_BCRA_e_não_BCRA",
        "Arquivo final": "Salesforce_Pending_Embargos_BCRA_e_não_BCRA"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Pending_Informativos",
        "Arquivo final": "Salesforce_Pending_Informativos"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE",
        "Arquivo": "Salesforce_Report_Embargos_Revisao",
        "Arquivo final": "Salesforce_Report_Embargos_Revisao"
    }
]
