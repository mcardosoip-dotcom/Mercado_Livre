# ================================================
# Descrição :  Faz a conversão de arquivos em Excel para o formato CSV 
#              a serem carregados no ambiente Meli
# Autor : Marcelo Cardoso
# ================================================

import os
import re
import pandas as pd
import logging
import time
from datetime import datetime
from coda_processo_geral import inserir_dados    

data_atual = datetime.now().date().strftime("%Y-%m-%d")
hora_inicio = datetime.now().strftime("%H:%M:%S")

# Configurar o log
caminho_log = r'G:\Drives compartilhados\Legales_Analytics_Legado\Projetos Python\Update de reports\LOGS do processo\LOG_Conversão_em_CSV_Bucket_Entradas e desfechos.log'
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
    # Definir a quantidade de linhas a serem lidas (0 para ler todas)
    quantidade_linhas = 0

    # Caminho do arquivo Excel atualizado
    caminho_xlsx = r"G:\Drives compartilhados\Legales_Analytics_Legado\006 - Reports e Acompanhamentos\006 - Dashboard Entradas Brasil e CORP\Versão 2\Data Self Information - Entradas e desfechos.xlsx"

    # Carregar os dados do Excel, ignorando a coluna "Processo - CustID MeLi"
    try:
        if quantidade_linhas == 0:
            dados = pd.read_excel(caminho_xlsx, usecols=lambda x: x != 'Processo - CustID MeLi')
        else:
            dados = pd.read_excel(caminho_xlsx, nrows=quantidade_linhas, usecols=lambda x: x != 'Processo - CustID MeLi')
        logging.info("Dados do Excel carregados com sucesso.")
    except Exception as e:
        logging.error("Erro ao carregar o arquivo Excel: " + str(e))
        raise

    # Renomear colunas
    rename_columns = {
        'Data de Citação': 'data_citacao',
        '(Processo) ID': 'processo_id',
        'Pasta': 'pasta',
        'País': 'pais',
        'Número do Processo': 'numero_processo',
        'Status': 'status',
        'Área do Direito': 'area_direito',
        'Sub-área do Direito': 'sub_area_direito',
        'Cliente': 'cliente',
        'Parte Contrária Nome': 'parte_contraria_nome',
        'Cust ID Autor': 'cust_id_autor',
        'Outras Partes / Não-Clientes': 'outras_partes_nao_clientes',
        'page.report.escritorioResponsavel': 'escritorio_responsavel',
        'Data Audiencia Inicial': 'data_audiencia_inicial',
        'Advogado Responsável': 'advogado_responsavel',
        '(Processo) Estado': 'processo_estado',
        '(Processo) Comarca': 'processo_comarca',
        '(Processo) Vara/Órgão': 'processo_vara_orgao',
        'Ação': 'acao',
        'Tipo de Contingência': 'tipo_contingencia',
        'Risco': 'risco',
        'Valor da Causa': 'valor_causa',
        'Modalidade': 'modalidade',
        'Data Registrado': 'data_registrado',
        'Parte Contrária CPF': 'parte_contraria_cpf',
        'Data de encerramento': 'data_encerramento',
        'Data de registro do encerramento': 'data_registro_encerramento',
        'Procedimento Judicial': 'procedimento_judicial',
        'Resumo do Subsídio': 'resumo_subsidio',
        'Advogado da Parte Contrária Nome': 'advogado_parte_contraria_nome',
        'ID Mediação': 'id_mediacao',
        'Valor do Risco': 'valor_risco',
        'ID do Pagamento': 'id_pagamento',
        'Fase/Estado': 'fase_estado',
        'Fase/Estado_4': 'fase_estado_4',
        'Advogado Parte Contrária Contumaz': 'advogado_parte_contraria_contumaz',
        'Usuário': 'usuario',
        'Motivo de Encerramento ': 'motivo_encerramento',
        'Caratula': 'caratula',
        'Indica Menoridade?': 'indica_menoridade',
        '(Processo) Classificação': 'processo_classificacao',
        'Invoca hipervulnerabilidad?': 'invoca_hipervulnerabilidade',
        'Causas Raízes': 'causas_raizes',
        'Causas Raízes_1': 'causas_raizes_1',
        'Causas Raízes_2': 'causas_raizes_2',
        'Modelo de contratação': 'modelo_contratacao',
        'Proceso Crítico?': 'processo_critico',
        'Unidade de Negócio Impactada': 'unidade_negocio_impactada',
        'Cust ID Contraparte': 'cust_id_contraparte',
        'Valor 1° Instância': 'valor_primeira_instancia',
        'Empresa Responsável': 'empresa_responsavel',
        'Processo - Empresa Demandada': 'processo_empresa_demandada',
        # 'Processo - CustID MeLi': 'processo_custid_meli',  # Coluna removida conforme necessidade
        'Processo - Revisado por DRE?': 'processo_revisado_dre',
        'Processo - Escritório do advogado da parte contrária': 'processo_escritorio_advogado_parte_contraria',
        'Processo - Matéria': 'processo_materia',
        'Processo - Objeto revisado?': 'processo_objeto_revisado',
        'Forma de Participação': 'forma_participacao',
        'Pedido': 'pedido',
        'Data de reativação': 'data_reativacao',
        'Motivo de reativação': 'motivo_reativacao',
        'Valor Objeto': 'valor_objeto',
        'Processo - Condenação em Má Fé': 'processo_condenacao_ma_fe',
        'Processo - Valor Associado a Má Fé': 'processo_valor_associado_ma_fe',
        'Processo - PRAZO': 'processo_prazo',
        'Objeto_Tratado': 'objeto_tratado',
        'Database.UNIDADE': 'database_unidade',
        'Empresa_Tratada': 'empresa_tratada',
        'Fase_Desfecho': 'fase_desfecho',
        'Multa.Data': 'multa_data',
        'Multa.Tipo ajustado': 'multa_tipo_ajustado',
        'Decisão - Análise de responsabilidade': 'decisao_analise_de_responsabilidade',
        'Superendividamento': 'superendividamento',
        'Região': 'regiao',
        'Mundo': 'mundo'
    }
    dados.rename(columns=rename_columns, inplace=True)
    logging.info("Colunas renomeadas com sucesso.")

    # Converter colunas para datas
    def converter_para_nat(dados, colunas):
        for coluna in colunas:
            dados[coluna] = pd.to_datetime(dados[coluna], errors='coerce')
        return dados

    dados = converter_para_nat(dados, [
        'data_citacao', 'data_audiencia_inicial', 'data_registrado',
        'data_encerramento', 'data_registro_encerramento', 'data_reativacao'
    ])
    logging.info("Conversão de colunas de data realizada.")

    # Converter colunas numéricas para NaN se houver erro
    def converter_para_nan(dados, colunas):
        for coluna in colunas:
            dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')
        return dados

    dados = converter_para_nan(dados, [
        'processo_id', 'cust_id_autor', 'id_mediacao', 'valor_risco',
        'id_pagamento', 'cust_id_contraparte', 'valor_primeira_instancia', 'valor_objeto'
    ])
    logging.info("Conversão de colunas numéricas realizada.")

    # Conversão de tipos de colunas corrigida
    try:
        dados = dados.astype({
            'processo_id': pd.Int64Dtype(),
            'cust_id_autor': 'float',
            'id_mediacao': pd.Int64Dtype(),
            'valor_risco': 'float',
            'id_pagamento': pd.Int64Dtype(),
            'cust_id_contraparte': 'float',
            'valor_primeira_instancia': 'float',
            'valor_objeto': 'float'
        }, errors='ignore')
        logging.info("Conversão de tipos de colunas realizada com sucesso.")
    except Exception as e:
        logging.error("Erro na conversão de tipos de colunas: " + str(e))
        raise

    # Função para remover caracteres indesejados
    def remover_caracteres_indesejados(texto):
        if isinstance(texto, str):
            texto_limpo = re.sub(r'\t+', '', texto)  # Remover tabs
            texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()  # Remover espaços extras
            return texto_limpo
        return texto

    # Aplicar a limpeza apenas em colunas de texto utilizando Series.map
    try:
        colunas_texto = dados.select_dtypes(include=['object']).columns
        for col in colunas_texto:
            dados[col] = dados[col].map(remover_caracteres_indesejados)
        logging.info("Limpeza de caracteres em colunas de texto realizada.")
    except Exception as e:
        logging.error("Erro na limpeza de caracteres: " + str(e))
        raise

    # Coluna 'resumo_subsidio' em branco
    dados['resumo_subsidio'] = ''
    logging.info("Coluna 'resumo_subsidio' definida como vazia.")

    # Definir o caminho base do arquivo CSV de saída
    caminho_base = r"G:\Drives compartilhados\Legales_Analytics_Legado\001 - Databases_e_dimensões\Python - Extrações eLAW e Salesforce\Upload Bucket\Data Self Information - Entradas e desfechos"
    if quantidade_linhas == 0:
        caminho_csv = f"{caminho_base}.csv"
    else:
        caminho_csv = f"{caminho_base}_{quantidade_linhas}.csv"

    # Salvar o novo arquivo CSV
    try:
        dados.to_csv(caminho_csv, index=False, sep='|', encoding='utf-8-sig')
        logging.info(f"Arquivo CSV salvo com sucesso em {caminho_csv}")
        print(f"Arquivo salvo com sucesso em {caminho_csv}")
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
    inserir_dados(data_atual, "Criaçao de arquivo CSV | Entradas e desfechos", hora_inicio, hora_fim, status_do_processo, "Diário")
