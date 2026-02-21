# ================================================
# Descrição :  Faz a conversão de arquivos em Excel para o formato CSV 
#              a serem carregados no ambiente Meli
# Autor : Marcelo Cardoso
# ================================================

import pandas as pd
import re
import logging
import time
from datetime import datetime
from coda_processo_geral import inserir_dados

data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Configurar o log
caminho_log = r'G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo\LOG_Conversão_em_CSV_Bucket_Pagamentos_em_garantia.log'
logging.basicConfig(
    filename=caminho_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("Início do processamento - Script iniciado.")

# Flag para controle de erro
erro_encontrado = False

try:
    # BASE DE PAGAMENTOS EM GARANTIA
    # Definir quantidade de linhas a serem carregadas
    quantidade_linhas = 0

    # Caminho do arquivo Excel (origem) - atualizado para novo endereço
    caminho_xlsx = r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\046 - Pagamentos e garantia\Push Pagamentos em Garantia.xlsx'

    try:
        # Carregar os dados do Excel
        if quantidade_linhas == 0:
            dados = pd.read_excel(caminho_xlsx)
        else:
            dados = pd.read_excel(caminho_xlsx, nrows=quantidade_linhas)
        logging.info("Dados do Excel carregados com sucesso.")
    except Exception as e:
        logging.error("Erro ao carregar o arquivo Excel: " + str(e))
        raise

    # Dicionário para renomear colunas
    rename_columns = {
        'Empresa pertinente': 'empresa_pertinente',
        'Tipo de Transferência': 'tipo_de_transferencia',
        'Nro. Legales': 'nro_legales',
        'IMPORTE': 'importe',
        'Prazo Fatal': 'prazo_fatal',
        'Número da Conta.....': 'numero_da_conta',
        'Beneficiário (nome)': 'beneficiario_nome',
        'Estado': 'estado',
        'Banco': 'banco',
        'Agência': 'agencia',
        'Tipo de Conta': 'tipo_de_conta',
        'CPF/CNPJ': 'cpf_cnpj',
        'Fecha Estado': 'fecha_estado',
        'Provedor': 'provedor',
        'FACTURA': 'factura',
        'Centro de Costo Materia': 'centro_de_costo_materia',
        'ACORDO': 'acordo',
        'Tipo de Procedimento': 'tipo_de_procedimento',
        'Conta contábil': 'conta_contabil',
        'Centro de Custo': 'centro_de_custo',
        'FECHA': 'fecha',
        'Código de Barras': 'codigo_de_barras',
        'Parte Contrária Nome': 'parte_contraria_nome',
        'Advogado Responsável': 'advogado_responsavel',
        'Processo - ID': 'processo_id',
        'Sub Tipo': 'sub_tipo',
        'Escritório Externo': 'escritorio_externo',
        '(Processo) Classificação': 'processo_classificacao',
        'Status': 'status',
        'Área do Direito': 'area_do_direito',
        'Sub-área do Direito': 'sub_area_do_direito',
        'Valor Levantado (Empresa)': 'valor_levantado_empresa',
        'Valor Levantado (Parte Contrária)': 'valor_levantado_parte_contraria',
        'Valor Total Garantias': 'valor_total_garantias',
        'Valor': 'valor',
        'Tipo': 'tipo',
        'Sub Tipo_1': 'sub_tipo_1',
        'Objeto': 'objeto',
        'Objeto revisado?': 'objeto_revisado',
        'Fase': 'fase',
        'Estado_2': 'estado_2',
	'Tipo de Contingência':'tipo_de_contingencia'
    }

    try:
        # Renomear colunas
        dados.rename(columns=rename_columns, inplace=True)
        logging.info("Colunas renomeadas com sucesso.")
    except Exception as e:
        logging.error("Erro ao renomear as colunas: " + str(e))
        raise

    # Definir o caminho base do arquivo CSV de saída
    caminho_base = r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket\Pagamentos em garantia'
    if quantidade_linhas == 0:
        caminho_csv = f"{caminho_base}.csv"
    else:
        caminho_csv = f"{caminho_base}_{quantidade_linhas}.csv"

    try:
        # Salvar o arquivo CSV garantindo a codificação e separador especificados
        dados.to_csv(caminho_csv, index=False, sep='|', encoding='utf-8-sig')
        logging.info(f"Arquivo CSV salvo com sucesso em {caminho_csv}")
        print(f"Arquivo renomeado salvo com sucesso em {caminho_csv}")
    except Exception as e:
        logging.error("Erro ao salvar o arquivo CSV: " + str(e))
        raise

    logging.info("Processamento finalizado com sucesso.")

except Exception as e:
    logging.error("Erro geral no processamento: " + str(e))
    erro_encontrado = True

finally:
    hora_fim = datetime.now().strftime("%H:%M:%S")
    status_do_processo = "Falha no processamento" if erro_encontrado else "Processamento Ok"
    inserir_dados(data_atual, "Criaçao de arquivo CSV | Pagamentos em garantia", hora_inicio, hora_fim, status_do_processo,"Diário")
