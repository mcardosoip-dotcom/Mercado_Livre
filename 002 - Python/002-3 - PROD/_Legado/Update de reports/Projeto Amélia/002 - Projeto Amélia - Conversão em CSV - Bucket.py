# ================================================
# Descrição :  Faz a conversão de arquivos em Excel para o formato CSV 
#              a serem carregados no ambiente Meli
# Autor : Marcelo Cardoso
# ================================================

# ================================================
# Descrição :  Faz a conversão de arquivos em Excel para o formato CSV 
#              a serem carregados no ambiente Meli
# Autor : Marcelo Cardoso
# ================================================

import pandas as pd
import argparse
import re
from datetime import datetime
import sys
sys.path.append(r"G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports")
from coda_processo_geral import inserir_dados


# Data e hora atuais
data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Dicionário para renomear colunas
rename_columns = {
    'Pais': 'pais',
    'Processo - Procedimento Judicial': 'processo_procedimento_judicial',
    'Processo - Objeto - Objeto': 'processo_objeto_objeto',
    'Data Audiencia Inicial': 'data_audiencia_inicial',
    'Processo - Audiência fictícia?': 'processo_audiencia_ficticia',
    'Processo - Invoca hipervulnerabilidad?.': 'processo_invoca_hypervulnerabilidad',
    'Advogado da Parte Contrária': 'advogado_da_parte_contraria_nome',
    'Processo - O usuário reclama por dois ou mais produtos diferentes?': 'processo_o_usuario_reclama_por_dois_ou_mais_produtos_diferentes',
    'Processo - O documento de identidade da reclamação corresponde ao da compra?': 'processo_o_documento_de_identidade_da_reclamacao_corresponde_ao_da_compra',
    'Processo - É High Risk confirmado pelo PF?': 'processo_e_high_risk_confirmado_pelo_pf',
    'Processo - Cust ID Autor': 'processo_cust_id_autor',
    'Processo - ID da Operação MP': 'processo_id_da_operacao_mp',
    'Processo - ID do Anúncio': 'processo_id_do_anuncio',
    'Parte Contrária Nome': 'parte_contraria_nome',
    'Parte Contrária CPF/CNPJ': 'parte_contraria_cpf_cnpj',
    'Número do Processo': 'numero_do_processo',
    'Processo - ID': 'processo_id',
    'Área do Direito': 'area_do_direito',
    'Sub-área do Direito': 'sub_area_do_direito',
    'Status': 'status',
    'Valor da Causa': 'valor_da_causa',
    'Data Registrado': 'data_registrado',
    'Processo - O objeto da reclamação é PDD ON ou PNR ON?:': 'processo_objeto_PDDON_OU_PNRON',
    'Processo - Fase/Estado - Fase':'processo_fase',
    'Processo - Fase/Estado - Estado':'processo_estado'
}

# Função para extrair o primeiro grupo de 11 dígitos
def extrair_primeiro_id(valor):
    if pd.isna(valor):
        return None
    texto = str(valor)
    partes = re.split(r"[,\s\/\\\-\.;:\|\_\.\(\)\[\]]+", texto)
    # Filtra strings não vazias
    partes = [p for p in partes if p]
    if not partes:
        return None
    primeiro = partes[0]
    # Mantém só dígitos
    numeros = re.sub(r"\D+", "", primeiro)
    return numeros or None

# Função para manter apenas números
def manter_apenas_numeros(valor):
    if pd.isna(valor):
        return None
    valor = str(valor)
    apenas_numeros = re.sub(r'\D', '', valor)
    return apenas_numeros if apenas_numeros else None

def main(mostrar):
    # Define caminhos dos arquivos
    input_excel = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Database_2_Report_eLAW_Amelia.xlsx"
    output_csv = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket\CSV Amélia.csv"
    
    # Lê a aba do Excel, pulando as primeiras 5 linhas
    df = pd.read_excel(input_excel, sheet_name=0, skiprows=range(5))
    
    if mostrar:
        print("Colunas originais (as is):")
        print(df.columns.tolist())
    
    # Renomeia colunas
    df.rename(columns=rename_columns, inplace=True)
    
    # Converte data_audiencia_inicial para o formato que o BigQuery aceita
    if 'data_audiencia_inicial' in df.columns:
        df['data_audiencia_inicial'] = (
            pd.to_datetime(
                df['data_audiencia_inicial'],
                dayfirst=True,
                errors='coerce'
            )
            .dt.strftime('%Y-%m-%d %H:%M:%S')
        )
    
    if mostrar:
        print("\nColunas após renomeação:")
        print(df.columns.tolist())
    
    # Tratamento do campo processo_id_da_operacao_mp
    if 'processo_id_da_operacao_mp' in df.columns:
        df['processo_id_da_operacao_mp'] = df['processo_id_da_operacao_mp'].apply(extrair_primeiro_id)

    # Tratamento do campo processo_cust_id_autor (mantendo apenas números)
    if 'processo_cust_id_autor' in df.columns:
        df['processo_cust_id_autor'] = df['processo_cust_id_autor'].apply(manter_apenas_numeros)
    
    # Salva o DataFrame em CSV
    df.to_csv(output_csv, sep='|', index=False, encoding='utf-8-sig')
    print("\nCSV salvo em:", output_csv)

if __name__ == "__main__":
    erro_encontrado = False
    try:
        parser = argparse.ArgumentParser(
            description="Script para ler Excel, renomear colunas, tratar campos e gerar CSV."
        )
        parser.add_argument(
            '--mostrar',
            action='store_true',
            help="Exibe as colunas antes e depois da renomeação."
        )
        args = parser.parse_args()
        main(args.mostrar)
    except Exception as e:
        print("Ocorreu um erro:", e)
        erro_encontrado = True
    finally:
        hora_fim = datetime.now().strftime("%H:%M:%S")
        status_do_processo = "Falha no processamento" if erro_encontrado else "Processamento Ok"
        inserir_dados(
            data_atual,
            "Criação de arquivo CSV | CSV Amélia",
            hora_inicio,
            hora_fim,
            status_do_processo,
            "Diário"
        )
