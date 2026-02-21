CREATE OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BUDGET_THEMIS_FINAL` AS

WITH Raw_Data AS (
  SELECT
    *
  FROM
    `<ENV>.STG.LK_PBD_LA_BUDGET_THEMIS_2025_FATO`
  UNION ALL
  SELECT
    *
  FROM
    `<ENV>.STG.LK_PBD_LA_BUDGET_THEMIS_2026_FATO`
),
Base_Budget_Completa AS (
  SELECT
    'Budget' AS Versao,
    CASE 
      WHEN rd.year IS NOT NULL THEN CAST(rd.year AS INT64)
      ELSE 2030
    END AS Ano,
    m.Mes,
    rd.Business_unit AS BU,
    rd.Subarea,
    rd.Society,
    rd.Service,
    rd.Category_name,
    rd.Grouper_name,
    rd.supplier_name,
    rd.Subsegment_name AS COUNTRY,
    rd.BU_AREA AS AREA,
    rd.EQUIPO,
    rd.Agrupador_1,
    rd.Agrupador_2,
    rd.VERTICAL,
    rd.Supplier_unificado AS Item_Text,
    rd.Account_name,
    rd.Currency_code,
    rd.Department_name,
    m.Valor_USD AS Valor_USD,
    m.Valor_Local AS Valor_Local
  FROM
    Raw_Data AS rd
  CROSS JOIN UNNEST([
    STRUCT('January'    AS Mes, rd.january_usd AS Valor_USD, rd.january_local AS Valor_Local),
    STRUCT('February'   AS Mes, rd.february_usd AS Valor_USD, rd.february_local AS Valor_Local),
    STRUCT('March'      AS Mes, rd.march_usd AS Valor_USD, rd.march_local AS Valor_Local),
    STRUCT('April'      AS Mes, rd.april_usd AS Valor_USD, rd.april_local AS Valor_Local),
    STRUCT('May'        AS Mes, rd.may_usd AS Valor_USD, rd.may_local AS Valor_Local),
    STRUCT('June'       AS Mes, rd.june_usd AS Valor_USD, rd.june_local AS Valor_Local),
    STRUCT('July'       AS Mes, rd.july_usd AS Valor_USD, rd.july_local AS Valor_Local),
    STRUCT('August'     AS Mes, rd.august_usd AS Valor_USD, rd.august_local AS Valor_Local),
    STRUCT('September'  AS Mes, rd.september_usd AS Valor_USD, rd.september_local AS Valor_Local),
    STRUCT('October'    AS Mes, rd.october_usd AS Valor_USD, rd.october_local AS Valor_Local),
    STRUCT('November'   AS Mes, rd.november_usd AS Valor_USD, rd.november_local AS Valor_Local),
    STRUCT('December'   AS Mes, rd.december_usd AS Valor_USD, rd.december_local AS Valor_Local)
  ]) AS m
)
SELECT
  *
FROM
  Base_Budget_Completa;
