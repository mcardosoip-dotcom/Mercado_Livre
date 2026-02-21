-- ================================
-- Tabela: LK_MESA_BASE_VISTA_ENTRADAS
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_BASE_VISTA_ENTRADAS` AS
SELECT
    CAST(fecha AS STRING) AS FECHA,
    CAST(numero_semana_ingreso AS STRING) AS NUMERO_SEMANA_INGRESO,
    CAST(fecha_clasificado AS STRING) AS FECHA_CLASSIFICADO,
    CAST(tiempo_espera_en_segundos AS STRING) AS TIEMPO_ESPERA_EN_SEGUNDOS,
    CAST(rol AS STRING) AS ROL,
    CAST(estado_nombre AS STRING) AS ESTADO_NOMBRE,
    CAST(tipo_estado AS STRING) AS TIPO_ESTADO,
    CAST(origen AS STRING) AS ORIGEN,
    CAST(tematica AS STRING) AS TEMATICA,
    CAST(tematica_clasificacion AS STRING) AS TEMATICA_CLASSIFICACAO,
    CAST(anulado AS STRING) AS ANULADO,
    CAST(id AS STRING) AS ID,
    CAST(dia_semana AS STRING) AS DIA_SEMANA,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_VISTA_ENTRADAS`;

-- ================================
-- Tabela: LK_MESA_DW_HIST_CASOS_X_ESTADO
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_DW_HIST_CASOS_X_ESTADO` AS
SELECT
    CAST(fecha AS STRING) AS FECHA,
    CAST(tipo AS STRING) AS TIPO,
    CAST(ORDEN AS STRING) AS ORDEN,
    CAST(total AS STRING) AS TOTAL,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_HIST_CASOS_X_ESTADO`;

-- ================================
-- Tabela: LK_MESA_VISTA_CANTIDAD_CASOS_USUARIOS
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_VISTA_CANTIDAD_CASOS_USUARIOS` AS
SELECT
    CAST(fecha AS STRING) AS FECHA,
    CAST(numero_semana AS STRING) AS NUMERO_SEMANA,
    CAST(rol AS STRING) AS ROL,
    CAST(nombre_usuario AS STRING) AS NOME_USUARIO,
    CAST(cantidad_casos AS STRING) AS QUANTIDADE_CASOS,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_VISTA_CANTIDAD_CASOS_USUARIOS`;

-- ================================
-- Tabela: LK_MESA_VISTA_USUARIOS
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_VISTA_USUARIOS` AS
SELECT
    CAST(id_caso AS STRING) AS ID_CASO,
    CAST(id_estado_caso AS STRING) AS ID_ESTADO_CASO,
    CAST(nombre AS STRING) AS NOME,
    CAST(rol AS STRING) AS ROL,
    CAST(fecha_inicial AS STRING) AS FECHA_INICIAL,
    CAST(fecha_final AS STRING) AS FECHA_FINAL,
    CAST(tiempo_estado_en_segundos AS STRING) AS TIEMPO_ESTADO_EN_SEGUNDOS,
    CAST(tiempo_estado_en_min AS STRING) AS TIEMPO_ESTADO_EN_MIN,
    CAST(tiempo_estado_en_hora AS STRING) AS TIEMPO_ESTADO_EN_HORA,
    CAST(tiempo_estado_en_dias AS STRING) AS TIEMPO_ESTADO_EN_DIAS,
    CAST(numero_semana_inicio AS STRING) AS NUMERO_SEMANA_INICIO,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_VISTA_USUARIOS`;

-- ================================
-- Tabela: LK_MESA_ENTRADA_V_METRICAS_QA
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_ENTRADA_V_METRICAS_QA` AS
SELECT
    CAST(estado_qa AS STRING) AS ESTADO_QA,
    CAST(fecha_qa AS STRING) AS FECHA_QA,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_V_METRICAS_QA`;

-- ================================
-- Tabela: LK_MESA_ENTRADA_METRICAS_BIG_QUERY
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_ENTRADA_METRICAS_BIG_QUERY` AS
SELECT
    CAST(fecha AS STRING) AS FECHA,
    CAST(numero_semana AS STRING) AS NUMERO_SEMANA,
    CAST(estado_consulta AS STRING) AS ESTADO_CONSULTA,
    CAST(estado_consultas AS STRING) AS ESTADO_CONSULTAS,
    CAST(incompleta AS STRING) AS INCOMPLETA,
    CAST(tipo AS STRING) AS TIPO,
    CAST(total AS STRING) AS TOTAL,
    CAST(ciudad AS STRING) AS CIUDAD,
    CAST(pais AS STRING) AS PAIS,
    CAST(destinatario AS STRING) AS DESTINATARIO,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_METRICAS_BIG_QUERY`;

-- ================================
-- Tabela: LK_MESA_BASE_TAB_ESTADOS
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_BASE_TAB_ESTADOS` AS
SELECT
    CAST(id AS STRING) AS ID,
    CAST(estado_nombre AS STRING) AS ESTADO_NOMBRE,
    CAST(causa_id AS STRING) AS CAUSA_ID,
    CAST(id_estado_siguiente AS STRING) AS ID_ESTADO_SEGUINTE,
    CAST(tipo_estado AS STRING) AS TIPO_ESTADO,
    CAST(tipo_rol AS STRING) AS TIPO_ROL,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_TAB_ESTADOS`;

-- ================================
-- Tabela: LK_MESA_BASE_TIPO_DOCUMENTOS
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_BASE_TIPO_DOCUMENTOS` AS
SELECT
    CAST(id AS STRING) AS ID,
    CAST(tipo_documento_nombre AS STRING) AS NOME,
    CAST(interviene_cap AS STRING) AS CODIGO,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_TIPO_DOCUMENTOS`;

    
-- ================================
-- Tabela: LK_MESA_BASE_ENTRADA_ESTADOS
-- ================================
-- ================================
CREATE OR REPLACE TABLE
    `<ENV>.STG.LK_MESA_BASE_ENTRADA_ESTADOS` AS
SELECT
    CAST(id AS STRING) AS ID,
    CAST(entrada_id AS STRING) AS ENTRADA_ID,
    -- CORRIGIDO: O resultado da divisão (FLOAT64) é explicitamente convertido para INT64
    DATETIME(
        TIMESTAMP_MICROS(
            CAST(
                CAST(fechahora_inicio AS INT64) / 1000 
            AS INT64)
        ), 
        'America/Sao_Paulo'
    ) AS FECHAHORA_INICIO,
    CAST(entrada_estado_id AS STRING) AS ENTRADA_ESTADO_ID,
    CAST(entrada_usuario_id AS STRING) AS ENTRADA_USUARIO_ID,
    -- CORRIGIDO: O resultado da divisão (FLOAT64) é explicitamente convertido para INT64
    DATETIME(
        TIMESTAMP_MICROS(
            CAST(
                CAST(fechahora_fin AS INT64) / 1000 
            AS INT64)
        ), 
        'America/Sao_Paulo'
    ) AS FECHAHORA_FIN,
    CAST(entrada_tiempo_estado AS STRING) AS ENTRADA_TIEMPO_ESTADO,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_ins_dttm,
    DATETIME(CURRENT_TIMESTAMP()) AS aud_upd_dttm
FROM
    `<ENV>.STG.INPUT_MESA_BASE_ENTRADA_ESTADOS`;