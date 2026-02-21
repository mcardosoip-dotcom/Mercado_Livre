CREATE OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BUDGET_LOOKER_Input` AS
WITH
  -- Primeira parte da união: dados de LK_PBD_LA_BUDGET_REAL_FINAL
  real_final_data AS (
    SELECT
      Versao,
      Ano,
      Mes,
      COUNTRY,
      EQUIPO,
      AGRUPADOR_1,
      AGRUPADOR_2,
      '' AS Account_name, -- Account_name é vazio para esta fonte
      Vendor_Desc,
      Item_Text,
      SAFE_CAST(Valor_Local AS NUMERIC) AS Valor_Local,
      SAFE_CAST(Valor_USD AS NUMERIC) AS Valor_USD
    FROM
      `<ENV>.STG.LK_PBD_LA_BUDGET_REAL_Atualizada`
  ),
  -- Segunda parte da união: dados de LK_PBD_LA_BUDGET_THEMIS_2025_FINAL
  themis_final_data AS (
    SELECT
      Versao,
      Ano,
      Mes,
      COUNTRY,
      EQUIPO,
      AGRUPADOR_1,
      AGRUPADOR_2,
      Account_name,
      supplier_name AS Vendor_Desc, -- Vendor_Desc é vazio para esta fonte
      Item_Text,
      SAFE_CAST(Valor_Local AS NUMERIC) AS Valor_Local,
      SAFE_CAST(Valor_USD AS NUMERIC) AS Valor_USD
    FROM
      `<ENV>.STG.LK_PBD_LA_BUDGET_THEMIS_2025_FINAL`
  ),
  -- União dos dados brutos de ambas as fontes
  raw_union AS (
    SELECT * FROM real_final_data
    UNION ALL
    SELECT * FROM themis_final_data
  )
SELECT
  Versao,
  CAST(Ano AS STRING) AS Ano,
  Mes,
  COUNTRY,
  CASE
    WHEN UPPER(EQUIPO) = 'LEGAL CENTRAL' THEN 'LEGAL OPS'
    WHEN UPPER(EQUIPO) IN ('LEGAL CREDITS', 'LEGAL PAYMENTS') THEN 'LEGAL FINTECH'
    WHEN EQUIPO IS NULL
    OR UPPER(EQUIPO) = '#VALUE!' THEN 'Outros'
    ELSE UPPER(EQUIPO)
  END AS AREA,
  AGRUPADOR_1,
  AGRUPADOR_2,
  Account_name,
  Vendor_Desc,
  Item_Text,
  Valor_Local,
  Valor_USD
FROM
  raw_union;

