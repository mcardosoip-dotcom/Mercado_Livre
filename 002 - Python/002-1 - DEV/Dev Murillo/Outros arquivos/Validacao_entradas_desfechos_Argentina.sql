-- ================================================
-- Validação: quantidade de processo_id distintos por mês - Argentina (base final no banco)
-- Período: 09/2024 a 12/2025
-- Projeto/dataset: pdme000426-c1s7scatwm0-furyid.STG
-- Se a base final for uma única tabela de entradas e desfechos, use a "Opção B" (uma tabela).
-- ================================================

-- --- Opção A: União das 3 tabelas STG de Contencioso Hispanos (eLAW) ---
-- Reflete as mesmas fontes que os parquets Database_eLAW_Contencioso_Hispanos_*.parquet

WITH base_argentina AS (
  SELECT
    SAFE_CAST(processo_id AS INT64) AS processo_id,
    PARSE_DATE('%d/%m/%Y', data_registrado) AS data_reg
  FROM `pdme000426-c1s7scatwm0-furyid.STG.DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING`
  WHERE LOWER(TRIM(SAFE_CAST(pais AS STRING))) = 'argentina'
    AND REGEXP_CONTAINS(TRIM(SAFE_CAST(data_registrado AS STRING)), r'^\d{1,2}/\d{1,2}/\d{4}$')

  UNION ALL

  SELECT
    SAFE_CAST(processo_id AS INT64),
    PARSE_DATE('%d/%m/%Y', data_registrado)
  FROM `pdme000426-c1s7scatwm0-furyid.STG.DATABASE_ELAW_CONTENCIOSO_HISPANOS_ONGOING`
  WHERE LOWER(TRIM(SAFE_CAST(pais AS STRING))) = 'argentina'
    AND REGEXP_CONTAINS(TRIM(SAFE_CAST(data_registrado AS STRING)), r'^\d{1,2}/\d{1,2}/\d{4}$')

  UNION ALL

  SELECT
    SAFE_CAST(processo_id AS INT64),
    PARSE_DATE('%d/%m/%Y', data_registrado)
  FROM `pdme000426-c1s7scatwm0-furyid.STG.DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING`
  WHERE LOWER(TRIM(SAFE_CAST(pais AS STRING))) = 'argentina'
    AND REGEXP_CONTAINS(TRIM(SAFE_CAST(data_registrado AS STRING)), r'^\d{1,2}/\d{1,2}/\d{4}$')
),

filtrado AS (
  SELECT processo_id, data_reg
  FROM base_argentina
  WHERE data_reg BETWEEN DATE(2024, 9, 1) AND DATE(2025, 12, 31)
    AND processo_id IS NOT NULL
)

SELECT
  FORMAT_DATE('%Y-%m', data_reg) AS ano_mes,
  COUNT(DISTINCT processo_id) AS processo_id_distintos
FROM filtrado
GROUP BY ano_mes
ORDER BY ano_mes;


-- ================================================
-- --- Opção B: Uma única tabela de entradas e desfechos ---
-- Use se no banco existir tabela consolidada (ex: entradas_desfechos, data_self_information_entradas_desfechos).
-- Ajuste o nome da tabela e colunas (processo_id, pais, data_registrado) se necessário.
-- ================================================
/*
WITH filtrado AS (
  SELECT
    SAFE_CAST(processo_id AS INT64) AS processo_id,
    PARSE_DATE('%d/%m/%Y', data_registrado) AS data_reg
  FROM `pdme000426-c1s7scatwm0-furyid.STG.SUA_TABELA_ENTRADAS_DESFECHOS`
  WHERE LOWER(TRIM(SAFE_CAST(pais AS STRING))) = 'argentina'
    AND REGEXP_CONTAINS(TRIM(SAFE_CAST(data_registrado AS STRING)), r'^\d{1,2}/\d{1,2}/\d{4}$')
    AND PARSE_DATE('%d/%m/%Y', data_registrado) BETWEEN DATE(2024, 9, 1) AND DATE(2025, 12, 31)
    AND processo_id IS NOT NULL
)
SELECT
  FORMAT_DATE('%Y-%m', data_reg) AS ano_mes,
  COUNT(DISTINCT processo_id) AS processo_id_distintos
FROM filtrado
GROUP BY ano_mes
ORDER BY ano_mes;
*/
