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
caminho_log = r'G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo\Base Ativa.log'
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
    # BASE DE PROCESSOS ATIVOS

    # Definir quantidade de linhas a serem carregadas
    quantidade_linhas = 0

    # Caminho do arquivo Excel (origem) - atualizado para novo endereço
    caminho_xlsx = r'G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\006 - Dashboard Entradas Brasil e CORP\Versão 2\Data Self Information - Base ativa.xlsx'

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
        '(Processo) ID': 'processo_id',
        'País': 'pais',
        'Número do Processo': 'numero_do_processo',
        'Status': 'status',
        'Área do Direito': 'area_do_direito',
        'Sub-área do Direito': 'sub_area_do_direito',
        'Parte Contrária Nome': 'parte_contraria_nome',
        'Cust ID Autor': 'cust_id_autor',
        'page.report.escritorioResponsavel': 'page_report_escritorio_responsavel',
        'Advogado Responsável': 'advogado_responsavel',
        '(Processo) Estado': 'processo_estado',
        '(Processo) Comarca': 'processo_comarca',
        '(Processo) Foro/Tribunal/Órgão': 'processo_foro_tribunal_orgao',
        '(Processo) Vara/Órgão': 'processo_vara_orgao',
        'Ação': 'acao',
        'Objeto': 'objeto',
        'Objeto_1': 'objeto_1',
        'Tipo de Contingência': 'tipo_de_contingencia',
        'Risco': 'risco',
        'Valor da Causa': 'valor_da_causa',
        'Data Registrado': 'data_registrado',
        'Parte Contrária CPF': 'parte_contraria_cpf',
        'Data de encerramento': 'data_de_encerramento',
        'Procedimento Judicial': 'procedimento_judicial',
        'Advogado da Parte Contrária Nome': 'advogado_da_parte_contraria_nome',
        'Cust ID Contraparte': 'cust_id_contraparte',
        'Valor do Risco': 'valor_do_risco',
        'Fase/Estado': 'fase_estado',
        'Fase/Estado_4': 'fase_estado_4',
        '(Processo) Classificação': 'processo_classificacao',
        'Causas Raízes': 'causas_raizes',
        'Causas Raízes_1': 'causas_raizes_1',
        'Causas Raízes_2': 'causas_raizes_2',
        'Processo - Empresa Demandada': 'processo_empresa_demandada',
        'Processo - Revisado por DRE?': 'processo_revisado_por_dre',
        'Processo - Objeto revisado?': 'processo_objeto_revisado',
        'Data de reativação': 'data_de_reativacao',
        'Motivo de reativação': 'motivo_de_reativacao',
        'Processo - Condenação em Má Fé': 'processo_condenacao_em_ma_fe',
        'Processo - Valor Associado a Má Fé': 'processo_valor_associado_a_ma_fe',
        'Processo - Superendividamento?': 'processo_superendividamento',
        'Objeto_Cross': 'objeto_cross',
        'Objeto_Novo': 'objeto_novo',
        'Unidade_Nova': 'unidade_nova',
        'Empresa_Nova': 'empresa_nova',
        'Aging': 'aging',
        'Flag_subs': 'flag_subs',
        'Multas.Data_Multa': 'multas_data_multa',
        'Multas.Tipo ajustado': 'multas_tipo_ajustado',
        'Fase Desfecho': 'fase_desfecho',
        'O valor da causa é maior que R$200k?': 'valor_da_causa_maior_que_200k',
        'O valor do risco é maior que R$200k?': 'valor_do_risco_maior_que_200k',
        'O valor do risco é maior que R$100k e menor que R$200k?': 'valor_do_risco_entre_100k_200k',
        'O valor do causa é maior que R$100k e menor que R$200k?': 'valor_da_causa_entre_100k_200k',
        'Região': 'regiao',
        'Mundo': 'Mundo'
    }

    # Renomear colunas
    dados.rename(columns=rename_columns, inplace=True)
    logging.info("Colunas renomeadas com sucesso.")

    # Funções de conversão
    def converter_para_nat(dados, colunas):
        for coluna in colunas:
            dados[coluna] = pd.to_datetime(dados[coluna], errors='coerce', format='%Y-%m-%d')
        return dados

    def converter_para_nan(dados, colunas):
        for coluna in colunas:
            dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')
        return dados

    def remover_caracteres_indesejados(texto):
        if isinstance(texto, str):
            texto_limpo = re.sub(r'\s+', ' ', texto.strip())  # Remove espaços extras
            return texto_limpo
        return texto

    def limpar_cpf(cpf):
        if pd.notna(cpf):
            return re.sub(r'\D', '', str(cpf))  # Remove tudo que não for número
        return ""

    # Converter colunas de data
    dados = converter_para_nat(dados, ['data_registrado', 'data_de_encerramento', 'data_de_reativacao', 'multas_data_multa'])
    logging.info("Conversão de colunas de data realizada.")

    # Converter colunas numéricas (exceto CPF)
    dados = converter_para_nan(dados, ['processo_id', 'cust_id_autor', 'valor_da_causa', 'valor_do_risco', 'processo_valor_associado_a_ma_fe'])
    logging.info("Conversão de colunas numéricas realizada.")

    # Aplicar limpeza de caracteres apenas em colunas de texto
    colunas_texto = ['parte_contraria_nome', 'advogado_da_parte_contraria_nome', 'acao', 'objeto']
    for coluna in colunas_texto:
        if coluna in dados.columns:
            dados[coluna] = dados[coluna].map(remover_caracteres_indesejados)
    logging.info("Limpeza de caracteres em colunas de texto realizada.")

    # Tratar CPFs como string e remover caracteres indesejados
    if 'parte_contraria_cpf' in dados.columns:
        dados['parte_contraria_cpf'] = dados['parte_contraria_cpf'].astype(str).map(limpar_cpf)
    logging.info("Tratamento de CPFs realizado.")

    # Caminho de destino para salvar o arquivo final - atualizado para novo endereço
    caminho_base = r'G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket\Data Self Information - Base ativa'
    if quantidade_linhas == 0:
        caminho_csv = f"{caminho_base}.csv"
    else:
        caminho_csv = f"{caminho_base}_{quantidade_linhas}.csv"

    try:
        # Salvar o arquivo CSV garantindo que os CPFs sejam preservados corretamente
        dados.to_csv(caminho_csv, index=False, sep='|', encoding='utf-8-sig')
        logging.info(f"Arquivo CSV salvo com sucesso em {caminho_csv}")
        print(f"Arquivo renomeado salvo com sucesso em {caminho_csv}")
    except Exception as e:
        logging.error("Erro ao salvar o arquivo CSV: " + str(e))
        raise

    logging.info("Processamento finalizado com sucesso.")

except Exception as e:
    # Se ocorrer alguma exceção durante o processamento global, marca erro_encontrado como True.
    logging.error("Erro geral no processamento: " + str(e))
    erro_encontrado = True

finally:
    hora_fim = datetime.now().strftime("%H:%M:%S")
    status_do_processo = "Falha no processamento" if erro_encontrado else "Processamento Ok"

    inserir_dados(data_atual, "Criaçao de arquivo CSV | Base Ativa", hora_inicio, hora_fim, status_do_processo,"Diário")
