TRUNCATE TABLE `<ENV>.TBL.LK_BASE_ATIVA`;

INSERT INTO `<ENV>.TBL.LK_BASE_ATIVA` (
    PROCESSO_ID,
    PAIS,
    NUMERO_DO_PROCESSO,
    STATUS,
    AREA_DO_DIREITO,
    SUB_AREA_DO_DIREITO,
    PARTE_CONTRARIA_NOME,
    CUST_ID_AUTOR,
    PAGE_REPORT_ESCRITORIO_RESPONSAVEL,
    ADVOGADO_RESPONSAVEL,
    PROCESSO_ESTADO,
    PROCESSO_COMARCA,
    PROCESSO_FORO_TRIBUNAL_ORGAO,
    PROCESSO_VARA_ORGAO,
    ACAO,
    OBJETO,
    OBJETO_1,
    TIPO_DE_CONTINGENCIA,
    RISCO,
    VALOR_DA_CAUSA,
    DATA_REGISTRADO,
    PARTE_CONTRARIA_CPF,
    DATA_DE_ENCERRAMENTO,
    PROCEDIMENTO_JUDICIAL,
    ADVOGADO_DA_PARTE_CONTRARIA_NOME,
    CUST_ID_CONTRAPARTE,
    VALOR_DO_RISCO,
    FASE_ESTADO,
    FASE_ESTADO_4,
    PROCESSO_CLASSIFICACAO,
    CAUSAS_RAIZES,
    CAUSAS_RAIZES_1,
    CAUSAS_RAIZES_2,
    PROCESSO_EMPRESA_DEMANDADA,
    REGIAO,
    FLAG_COM_SUBS,
    OBJETO_REVISADO,
    superendividamento,
    
    AUD_INS_DTTM,
    AUD_UPD_DTTM
)
SELECT
    CAST(processo_id AS STRING) AS processo_id,  -- Conversão de INT64 para STRING
    pais,
    numero_do_processo,
    status,
    area_do_direito,
    sub_area_do_direito,
    parte_contraria_nome,
    CAST(cust_id_autor AS STRING) AS cust_id_autor,  -- Conversão de FLOAT64 para STRING
    PAGE_REPORT_ESCRITORIORESPONSAVEL,
    advogado_responsavel,
    processo_estado,
    processo_comarca,
    processo_foro_tribunal_orgao,
    processo_vara_orgao,
    acao,
    objeto,
    objeto_1,
    tipo_de_contingencia,
    risco,
    CAST(valor_da_causa AS STRING) AS valor_da_causa,  -- Conversão de FLOAT64 para STRING
    CAST(data_registrado AS STRING) AS data_registrado,  -- Conversão de DATE para STRING
    CAST(parte_contraria_cpf AS STRING) AS parte_contraria_cpf,  -- Conversão de FLOAT64 para STRING
    CAST(data_de_encerramento AS STRING) AS data_de_encerramento,  -- Conversão de DATE para STRING, se necessário
    procedimento_judicial,
    advogado_da_parte_contraria_nome,
    CAST(cust_id_contraparte AS STRING) AS cust_id_contraparte,  -- Conversão de FLOAT64 para STRING
    CAST(valor_do_risco AS STRING) AS valor_do_risco,  -- Conversão de FLOAT64 para STRING
    fase_estado,
    fase_estado_4,
    processo_classificacao,
    causas_raizes,
    causas_raizes_1,
    causas_raizes_2,
    processo_empresa_demandada,
    regiao,
    CAST(1 AS STRING) AS flag_subs,
    CAST(processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
    processo_superendividamento,
    
    
    CAST(CURRENT_TIMESTAMP AS DATETIME) AS AUD_INS_DTTM,
    CAST(CURRENT_TIMESTAMP AS DATETIME) AS AUD_UPD_DTTM
FROM `<ENV>.STG.LK_PBD_LA_BASE_BASE_ATIVA`
