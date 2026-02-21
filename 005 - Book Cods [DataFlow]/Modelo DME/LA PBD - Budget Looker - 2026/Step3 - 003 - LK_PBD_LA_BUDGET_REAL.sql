CREATE OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BUDGET_REAL` AS

WITH Base_Real_2025 AS (
    SELECT
        'Real' AS Versao,
        2025 AS Ano,
        FORMAT_DATE('%B', PARSE_DATE('%Y%m', CAST(FISCAL_PERIOD AS STRING))) AS Mes,
        COUNTRY,
        AGRUPADOR_1,
        AGRUPADOR_2,
        PL_L8_ID AS Account_name,
        VENDOR_DESC AS Vendor_Desc,
        ITEM_TEXT AS Item_Text,
        AREA,
        SUBAREA,
        BU,
        SUBBU AS SubBU,
        ALLOCATION AS Allocation,
        DOCUMENT_TYPE_DESC AS Document_Type_Desc,
        DOCUMENT_ID AS Document_ID,
        '' AS Supplier_Unificado,
        FORMAT('%0.2f', SAFE_CAST(AMOUNT_LC AS FLOAT64)) AS Valor_Local,
        FORMAT('%0.2f', SAFE_CAST(AMOUNT_LC2_GLOB AS FLOAT64)) AS Valor_USD
    FROM (
        SELECT
            view_opex_s4.COMPANY_ID,
            view_opex_s4.FISCAL_PERIOD,
            view_opex_s4.COUNTRY,
            view_opex_s4.AGRUPADOR_1,
            view_opex_s4.AGRUPADOR_2,
            view_opex_s4.PL_L0_ID,
            view_opex_s4.PL_L8_ID,
            view_opex_s4.VENDOR_ID,
            view_opex_s4.VENDOR_DESC,
            view_opex_s4.ITEM_TEXT,
            view_opex_s4.AREA,
            view_opex_s4.SUBAREA,
            view_opex_s4.BU,
            view_opex_s4.BUSINESS_UNIT_SUBBU AS SUBBU,
            view_opex_s4.BU_AREA,
            view_opex_s4.ALLOCATION,
            view_opex_s4.DOCUMENT_TYPE,
            view_opex_s4.DOCUMENT_TYPE_DESC,
            view_opex_s4.DOCUMENT_ID,
            view_opex_s4.ACCOUNT_ID,
            view_opex_s4.ACCOUNT_DESC,
            view_opex_s4.COST_CENTER,
            COALESCE(SUM(view_opex_s4.AMOUNT_LC), 0) AS AMOUNT_LC,
            COALESCE(SUM(view_opex_s4.AMOUNT_LC2_GLOB), 0) AS AMOUNT_LC2_GLOB
        FROM
            `meli-bi-data.WHOWNER.BT_CRS_FPS_OPEX_SUPLIER_DETAIL_S4` AS view_opex_s4
        WHERE
            view_opex_s4.AGRUPADOR_1 IN ('BU/ Area Expenses', 'Legal Fees', 'Others')
            AND view_opex_s4.BU_AREA = 'Legales'
            AND view_opex_s4.FISCAL_PERIOD IN (
                '202501','202502','202503','202504','202505','202506','202507',
                '202508','202509','202510','202511','202512'
            )
        GROUP BY
            view_opex_s4.COMPANY_ID,
            view_opex_s4.FISCAL_PERIOD,
            view_opex_s4.COUNTRY,
            view_opex_s4.AGRUPADOR_1,
            view_opex_s4.AGRUPADOR_2,
            view_opex_s4.PL_L0_ID,
            view_opex_s4.PL_L8_ID,
            view_opex_s4.VENDOR_ID,
            view_opex_s4.VENDOR_DESC,
            view_opex_s4.ITEM_TEXT,
            view_opex_s4.AREA,
            view_opex_s4.SUBAREA,
            view_opex_s4.BU,
            view_opex_s4.BUSINESS_UNIT_SUBBU,
            view_opex_s4.BU_AREA,
            view_opex_s4.ALLOCATION,
            view_opex_s4.DOCUMENT_TYPE,
            view_opex_s4.DOCUMENT_TYPE_DESC,
            view_opex_s4.DOCUMENT_ID,
            view_opex_s4.ACCOUNT_ID,
            view_opex_s4.ACCOUNT_DESC,
            view_opex_s4.COST_CENTER
    )
),

Base_Real_2026 AS (
    SELECT
        'Real' AS Versao,
        2026 AS Ano,
        FORMAT_DATE('%B', PARSE_DATE('%Y%m', CAST(FISCAL_PERIOD AS STRING))) AS Mes,
        COUNTRY,
        AGRUPADOR_1,
        AGRUPADOR_2,
        PL_L8_ID AS Account_name,
        VENDOR_DESC AS Vendor_Desc,
        ITEM_TEXT AS Item_Text,
        AREA,
        SUBAREA,
        BU,
        SUBBU AS SubBU,
        ALLOCATION AS Allocation,
        DOCUMENT_TYPE_DESC AS Document_Type_Desc,
        DOCUMENT_ID AS Document_ID,
        '' AS Supplier_Unificado,
        FORMAT('%0.2f', SAFE_CAST(AMOUNT_LC AS FLOAT64)) AS Valor_Local,
        FORMAT('%0.2f', SAFE_CAST(AMOUNT_LC2_GLOB AS FLOAT64)) AS Valor_USD
    FROM (
        SELECT
            view_opex_s4.COMPANY_ID,
            view_opex_s4.FISCAL_PERIOD,
            view_opex_s4.COUNTRY,
            view_opex_s4.AGRUPADOR_1,
            view_opex_s4.AGRUPADOR_2,
            view_opex_s4.PL_L0_ID,
            view_opex_s4.PL_L8_ID,
            view_opex_s4.VENDOR_ID,
            view_opex_s4.VENDOR_DESC,
            view_opex_s4.ITEM_TEXT,
            view_opex_s4.AREA,
            view_opex_s4.SUBAREA,
            view_opex_s4.BU,
            view_opex_s4.BUSINESS_UNIT_SUBBU AS SUBBU,
            view_opex_s4.BU_AREA,
            view_opex_s4.ALLOCATION,
            view_opex_s4.DOCUMENT_TYPE,
            view_opex_s4.DOCUMENT_TYPE_DESC,
            view_opex_s4.DOCUMENT_ID,
            view_opex_s4.ACCOUNT_ID,
            view_opex_s4.ACCOUNT_DESC,
            view_opex_s4.COST_CENTER,
            COALESCE(SUM(view_opex_s4.AMOUNT_LC), 0) AS AMOUNT_LC,
            COALESCE(SUM(view_opex_s4.AMOUNT_LC2_GLOB), 0) AS AMOUNT_LC2_GLOB
        FROM
            `meli-bi-data.WHOWNER.BT_CRS_FPS_OPEX_SUPLIER_DETAIL_S4` AS view_opex_s4
        WHERE
            view_opex_s4.AGRUPADOR_1 IN ('BU/ Area Expenses', 'Legal Fees', 'Others')
            AND view_opex_s4.BU_AREA = 'Legales'
            AND view_opex_s4.FISCAL_PERIOD IN (
                '202601','202602','202603','202604','202605','202606','202607',
                '202608','202609','202610','202611','202612'
            )
        GROUP BY
            view_opex_s4.COMPANY_ID,
            view_opex_s4.FISCAL_PERIOD,
            view_opex_s4.COUNTRY,
            view_opex_s4.AGRUPADOR_1,
            view_opex_s4.AGRUPADOR_2,
            view_opex_s4.PL_L0_ID,
            view_opex_s4.PL_L8_ID,
            view_opex_s4.VENDOR_ID,
            view_opex_s4.VENDOR_DESC,
            view_opex_s4.ITEM_TEXT,
            view_opex_s4.AREA,
            view_opex_s4.SUBAREA,
            view_opex_s4.BU,
            view_opex_s4.BUSINESS_UNIT_SUBBU,
            view_opex_s4.BU_AREA,
            view_opex_s4.ALLOCATION,
            view_opex_s4.DOCUMENT_TYPE,
            view_opex_s4.DOCUMENT_TYPE_DESC,
            view_opex_s4.DOCUMENT_ID,
            view_opex_s4.ACCOUNT_ID,
            view_opex_s4.ACCOUNT_DESC,
            view_opex_s4.COST_CENTER
    )
),

Base_Real AS (
    SELECT * FROM Base_Real_2025
    UNION ALL
    SELECT * FROM Base_Real_2026
)

SELECT
    base.Versao,
    base.Ano,
    base.Mes,
    base.COUNTRY,
    base.AGRUPADOR_1,
    base.AGRUPADOR_2,
    base.Account_name,
    base.Vendor_Desc,
    base.Item_Text,
    base.AREA,
    base.SUBAREA,
    CASE
        WHEN base.BU = 'MARKETPLACE GENERAL' THEN 'MARKETPLACE'
        WHEN base.BU = 'PAYMENTS GENERAL' THEN 'PAYMENTS'
        WHEN base.BU = 'CREDITS GENERAL' THEN 'CREDITS'
        WHEN base.BU = 'SHIPPING GENERAL' THEN 'SHIPPING'
        ELSE base.BU
    END AS BU,
    base.SubBU,
    base.Allocation,
    base.Document_Type_Desc,
    base.Document_ID,
    base.Supplier_Unificado,
    base.Valor_Local,
    base.Valor_USD,
    CASE
        WHEN base.AREA = 'LEGALES OPS' THEN 'Legal Central'
        ELSE dic.EQUIPO
    END AS EQUIPO
FROM
    Base_Real base
LEFT JOIN `<ENV>.STG.LK_PBD_LA_BUDGET_DICIONARIO_FATO` AS dic
    ON UPPER(base.SUBAREA) = UPPER(dic.Sub_Area)
    AND UPPER(
        CASE
            WHEN base.BU = 'MARKETPLACE GENERAL' THEN 'MARKETPLACE'
            WHEN base.BU = 'PAYMENTS GENERAL' THEN 'PAYMENTS'
            WHEN base.BU = 'CREDITS GENERAL' THEN 'CREDITS'
            WHEN base.BU = 'SHIPPING GENERAL' THEN 'SHIPPING'
            ELSE base.BU
        END
    ) = UPPER(dic.BUSINESS_UNIT);
