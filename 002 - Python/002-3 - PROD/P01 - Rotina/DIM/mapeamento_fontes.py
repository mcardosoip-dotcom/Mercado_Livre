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
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_1_Dimensão_Advogados",
        "Aba": "Database",
        "Arquivo final": "Dim_1_Dimensão_Advogados"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_2_Dimensão_De_Para_Escritórios",
        "Aba": "Source",
        "Arquivo final": "Dim_2_Dimensão_De_Para_Escritórios"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_3_Dimensão_Empresas",
        "Aba": "Database",
        "Arquivo final": "Dim_3_Dimensão_Empresas"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_4_Dimensão_Escritórios",
        "Aba": "Database",
        "Arquivo final": "Dim_4_Dimensão_Escritórios"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_5_Dimensão_Esferas",
        "Aba": "Source",
        "Arquivo final": "Dim_5_Dimensão_Esferas"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_6_Dimensão_Estados_UF",
        "Aba": "Planilha1",
        "Arquivo final": "Dim_6_Dimensão_Estados_UF"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_7_Dimensão_Fases",
        "Aba": "Dim_Fases",
        "Arquivo final": "Dim_7_Dimensão_Fases"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_8_Dimensão_Grupo_Advogados_DR",
        "Aba": "Tabela",
        "Arquivo final": "Dim_8_Dimensão_Grupo_Advogados_DR"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_9_Dimensão_Mês",
        "Aba": "Database",
        "Arquivo final": "Dim_9_Dimensão_Mês"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_10_Dimensão_Objetos",
        "Aba": "Tab_RPA",
        "Arquivo final": "Dim_10_Dimensão_Objetos"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_12_Dimensão_Parceiros",
        "Aba": "Database",
        "Arquivo final": "Dim_12_Dimensão_Parceiros"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_13_Dimensão_Região",
        "Aba": "Planilha1",
        "Arquivo final": "Dim_13_Dimensão_Região"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_14_Dimensão_Fases_Revisada",
        "Aba": "Dim_Fases",
        "Arquivo final": "Dim_14_Dimensão_Fases_Revisada"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_15_Dimensão_Workflow",
        "Aba": "Database",
        "Arquivo final": "Dim_15_Dimensão_Workflow"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_16_Dimensão_Multa",
        "Aba": "Multa",
        "Arquivo final": "Dim_16_Dimensão_Multa"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_17_Dimensão_Sigla_País",
        "Aba": "Database",
        "Arquivo final": "Dim_17_Dimensão_Sigla_País"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_10_Dimensão_Objetos",
        "Aba": "Database",
        "Arquivo final": "Dim_10_Dimensão_Objetos_2"
    },
    {
        "Endereco": r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-00 - Dimensões\Stage",
        "Arquivo": "Dim_36_TPN_e_SI",
        "Aba": "Database",
        "Arquivo final": "Dim_36_TPN_e_SI"
    }
]
