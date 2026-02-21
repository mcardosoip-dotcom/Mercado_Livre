-- ============================
-- DIM_1_DIMENSAO_ADVOGADOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_1_DIMENSAO_ADVOGADOS` AS
SELECT
  CAST(advogado_responsavel AS STRING) AS advogado_responsavel
FROM
  `<ENV>.STG.DIM_1_DIMENSAO_ADVOGADOS`;

-- ============================
-- DIM_2_DIMENSAO_DE_PARA_ESCRITORIOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_2_DIMENSAO_DE_PARA_ESCRITORIOS` AS
SELECT
  CAST(nome_do_escritorio AS STRING) AS nome_do_escritorio,
  CAST(alias AS STRING) AS alias
FROM
  `<ENV>.STG.DIM_2_DIMENSAO_DE_PARA_ESCRITORIOS`;

-- ============================
-- DIM_3_DIMENSAO_EMPRESAS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_3_DIMENSAO_EMPRESAS` AS
SELECT
  CAST(cliente AS STRING) AS cliente,
  CAST(empresa AS STRING) AS empresa,
  CAST(empresa_modelo_2 AS STRING) AS empresa_modelo_2
FROM
  `<ENV>.STG.DIM_3_DIMENSAO_EMPRESAS`;

-- ============================
-- DIM_4_DIMENSAO_ESCRITORIOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_4_DIMENSAO_ESCRITORIOS` AS
SELECT
  CAST(escritorio AS STRING) AS escritorio,
  CAST(pais AS STRING) AS pais
FROM
  `<ENV>.STG.DIM_4_DIMENSAO_ESCRITORIOS`;

-- ============================
-- DIM_5_DIMENSAO_ESFERAS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_5_DIMENSAO_ESFERAS` AS
SELECT
  CAST(area_do_direito AS STRING) AS area_do_direito,
  CAST(sub_area_do_direito AS STRING) AS sub_area_do_direito,
  CAST(tipo AS STRING) AS tipo,
  CAST(validador AS STRING) AS validador
FROM
  `<ENV>.STG.DIM_5_DIMENSAO_ESFERAS`;

-- ============================
-- DIM_6_DIMENSAO_ESTADOS_UF
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_6_DIMENSAO_ESTADOS_UF` AS
SELECT
  CAST(estado AS STRING) AS estado,
  CAST(regiao AS STRING) AS regiao,
  CAST(onda AS STRING) AS onda
FROM
  `<ENV>.STG.DIM_6_DIMENSAO_ESTADOS_UF`;

-- ============================
-- DIM_7_DIMENSAO_FASES
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_7_DIMENSAO_FASES` AS
SELECT
  CAST(modelo AS STRING) AS modelo,
  CAST(fase AS STRING) AS fase,
  CAST(estado AS STRING) AS estado,
  CAST(tipo AS STRING) AS tipo,
  CAST(subtipo AS STRING) AS subtipo,
  CAST(status_fase AS STRING) AS status_fase,
  CAST(chave AS STRING) AS chave
FROM
  `<ENV>.STG.DIM_7_DIMENSAO_FASES`;

-- ============================
-- DIM_8_DIMENSAO_GRUPO_ADVOGADOS_DR
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_8_DIMENSAO_GRUPO_ADVOGADOS_DR` AS
SELECT
  CAST(advogado_responsavel AS STRING) AS advogado_responsavel,
  CAST(area_responsavel AS STRING) AS area_responsavel
FROM
  `<ENV>.STG.DIM_8_DIMENSAO_GRUPO_ADVOGADOS_DR`;

-- ============================
-- DIM_9_DIMENSAO_MES
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_9_DIMENSAO_MES` AS
SELECT
  CAST(id_mes AS STRING) AS id_mes,
  CAST(mes_br AS STRING) AS mes_br,
  CAST(mes_arg AS STRING) AS mes_arg,
  CAST(mes_ing AS STRING) AS mes_ing
FROM
  `<ENV>.STG.DIM_9_DIMENSAO_MES`;

-- ============================
-- DIM_10_DIMENSAO_OBJETOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS` AS
SELECT
  CAST(area_de_negocio AS STRING) AS area_de_negocio,
  CAST(objeto AS STRING) AS objeto,
  CAST(pais AS STRING) AS pais,
  CAST(empresa AS STRING) AS empresa
FROM
  `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS`;

-- ============================
-- DIM_12_DIMENSAO_PARCEIROS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_12_DIMENSAO_PARCEIROS` AS
SELECT
  CAST(usuario AS STRING) AS usuario,
  CAST(empresa AS STRING) AS empresa
FROM
  `<ENV>.STG.DIM_12_DIMENSAO_PARCEIROS`;

-- ============================
-- DIM_13_DIMENSAO_REGIAO
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_13_DIMENSAO_REGIAO` AS
SELECT
  CAST(estado AS STRING) AS estado,
  CAST(regiao AS STRING) AS regiao
FROM
  `<ENV>.STG.DIM_13_DIMENSAO_REGIAO`;

-- ============================
-- DIM_14_DIMENSAO_FASES_REVISADA
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_14_DIMENSAO_FASES_REVISADA` AS
SELECT
  CAST(fase AS STRING) AS fase,
  CAST(estado AS STRING) AS estado,
  CAST(tipo AS STRING) AS tipo
FROM
  `<ENV>.STG.DIM_14_DIMENSAO_FASES_REVISADA`;

-- ============================
-- DIM_15_DIMENSAO_WORKFLOW
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_15_DIMENSAO_WORKFLOW` AS
SELECT
  CAST(workflow AS STRING) AS workflow,
  CAST(fase_de_workflow AS STRING) AS fase_de_workflow,
  CAST(considerar AS STRING) AS considerar,
  CAST(grupo AS STRING) AS grupo,
  CAST(status_fase_workflow AS STRING) AS status_fase_workflow
FROM
  `<ENV>.STG.DIM_15_DIMENSAO_WORKFLOW`;

-- ============================
-- DIM_16_DIMENSAO_MULTA
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_16_DIMENSAO_MULTA` AS
SELECT
  CAST(tipo AS STRING) AS tipo,
  CAST(tipo_ajustado AS STRING) AS tipo_ajustado
FROM
  `<ENV>.STG.DIM_16_DIMENSAO_MULTA`;

-- ============================
-- DIM_17_DIMENSAO_SIGLA_PAIS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_17_DIMENSAO_SIGLA_PAIS` AS
SELECT
  CAST(sigla AS STRING) AS sigla,
  CAST(pais AS STRING) AS pais
FROM
  `<ENV>.STG.DIM_17_DIMENSAO_SIGLA_PAIS`;

-- ============================
-- DIM_10_DIMENSAO_OBJETOS_2
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS_2` AS
SELECT
  CAST(objeto AS STRING) AS objeto,
  CAST(objeto_novo AS STRING) AS objeto_novo,
  CAST(unidade AS STRING) AS unidade,
  CAST(empresa AS STRING) AS empresa,
  CAST(cruzar_com AS STRING) AS cruzar_com,
  CAST(tipo AS STRING) AS tipo,
  CAST(pais AS STRING) AS pais,
  CAST(empresa_code AS STRING) AS empresa_code,
  CAST(empresa_responsavel AS STRING) AS empresa_responsavel
FROM
  `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS_2`;

-- ============================
-- DIM_36_TPN_E_SI
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.DIM_36_TPN_E_SI` AS
SELECT
  CAST(ANO_REF AS STRING) AS ANO_REF,
  CAST(MES_REF_TXT AS STRING) AS MES_REF_TXT,
  CAST(SIGLA AS STRING) AS SIGLA,
  CAST(PAIS_REF AS STRING) AS PAIS_REF,
  CAST(TPN AS STRING) AS TPN,
  CAST(SI AS STRING) AS SI
FROM
  `<ENV>.STG.DIM_36_TPN_E_SI`;
