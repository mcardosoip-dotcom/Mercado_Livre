CREATE OR REPLACE TABLE `<ENV>.STG.BUDGET_CORACAO_TEMP` AS

WITH BASE_BRASIL AS (
    SELECT
        CAST(pais AS STRING) AS pais,
        CAST(Visao AS STRING) AS Visao,
        CAST(Objeto AS STRING) AS Objeto,
        CAST(Anomes AS STRING) AS Anomes,
        SUBSTR(CAST(Anomes AS STRING), 1, 4) AS Ano,

        CAST(Entradas_JEC AS STRING) AS Entradas_JEC,
        CAST(Entradas_JC AS STRING) AS Entradas_JC,
        CAST(Entradas_Procon AS STRING) AS Entradas_Procon,
        CAST(Total_Entradas AS STRING) AS Total_Entradas,

        CAST(Encerrados_JEC AS STRING) AS Encerrados_JEC,
        CAST(Encerrados_JC AS STRING) AS Encerrados_JC,
        CAST(Encerrados_Procon AS STRING) AS Encerrados_Procon,
        CAST(Total_Encerrados AS STRING) AS Total_Encerrados,

        CAST(JEC_Qty_Acordo AS STRING) AS JEC_Qty_Acordo,
        CAST(JC_Qty_Acordo AS STRING) AS JC_Qty_Acordo,
        CAST(Procon_Qty_Acordo AS STRING) AS Procon_Qty_Acordo,
        CAST(Total_Qty_Acordo AS STRING) AS Total_Qty_Acordo,

        CAST(JEC_Qty_Ganhamos AS STRING) AS JEC_Qty_Ganhamos,
        CAST(JC_Qty_Ganhamos AS STRING) AS JC_Qty_Ganhamos,
        CAST(Procon_Qty_Ganhamos AS STRING) AS Procon_Qty_Ganhamos,
        CAST(Total_Qty_Ganhamos AS STRING) AS Total_Qty_Ganhamos,

        CAST(JEC_Qty_Perdemos AS STRING) AS JEC_Qty_Perdemos,
        CAST(JC_Qty_Perdemos AS STRING) AS JC_Qty_Perdemos,
        CAST(Procon_Qty_Perdemos AS STRING) AS Procon_Qty_Perdemos,
        CAST(Total_Qty_Perdemos AS STRING) AS Total_Qty_Perdemos,

        CAST(JEC_Qty_Desistido AS STRING) AS JEC_Qty_Desistido,
        CAST(JC_Qty_Desistido AS STRING) AS JC_Qty_Desistido,
        CAST(Procon_Qty_Desistido AS STRING) AS Procon_Qty_Desistido,
        CAST(Total_Qty_Desistido AS STRING) AS Total_Qty_Desistido,

        CAST(JEC_Qty_Outros AS STRING) AS JEC_Qty_Outros,
        CAST(JC_Qty_Outros AS STRING) AS JC_Qty_Outros,
        CAST(Procon_Qty_Outros AS STRING) AS Procon_Qty_Outros,
        CAST(Total_Qty_Outros AS STRING) AS Total_Qty_Outros,

        CAST(JEC_TM_Acordo AS STRING) AS JEC_TM_Acordo,
        CAST(JC_TM_Acordo AS STRING) AS JC_TM_Acordo,
        CAST(Procon_TM_Acordo AS STRING) AS Procon_TM_Acordo,
        CAST(NULL AS STRING) AS TM_Acordo,

        CAST(JEC_TM_Ganhamos AS STRING) AS JEC_TM_Ganhamos,
        CAST(JC_TM_Ganhamos AS STRING) AS JC_TM_Ganhamos,
        CAST(Procon_TM_Ganhamos AS STRING) AS Procon_TM_Ganhamos,
        CAST(NULL AS STRING) AS TM_Ganhamos,

        CAST(JEC_TM_Perdemos AS STRING) AS JEC_TM_Perdemos,
        CAST(JC_TM_Perdemos AS STRING) AS JC_TM_Perdemos,
        CAST(Procon_TM_Perdemos AS STRING) AS Procon_TM_Perdemos,
        CAST(NULL AS STRING) AS TM_Perdemos,

        CAST(JEC_TM_Desistido AS STRING) AS JEC_TM_Desistido,
        CAST(JC_TM_Desistido AS STRING) AS JC_TM_Desistido,
        CAST(Procon_TM_Desistido AS STRING) AS Procon_TM_Desistido,
        CAST(NULL AS STRING) AS TM_Desistido,

        CAST(JEC_TM_Outros AS STRING) AS JEC_TM_Outros,
        CAST(JC_TM_Outros AS STRING) AS JC_TM_Outros,
        CAST(Procon_TM_Outros AS STRING) AS Procon_TM_Outros,
        CAST(NULL AS STRING) AS TM_Outros
    FROM `<ENV>.STG.BUDGET_ACTUAL_BRA`
),

BASE_ARGENTINA AS (
    SELECT
        CAST(pais AS STRING) AS pais,
        CAST(Visao AS STRING) AS Visao,
        CAST(Objeto AS STRING) AS Objeto,
        CAST(Anomes AS STRING) AS Anomes,
        SUBSTR(CAST(Anomes AS STRING), 1, 4) AS Ano,

        CAST(NULL AS STRING) AS Entradas_JEC,
        CAST(NULL AS STRING) AS Entradas_JC,
        CAST(NULL AS STRING) AS Entradas_Procon,
        CAST(Total_Entradas AS STRING) AS Total_Entradas,

        CAST(NULL AS STRING) AS Encerrados_JEC,
        CAST(NULL AS STRING) AS Encerrados_JC,
        CAST(NULL AS STRING) AS Encerrados_Procon,
        CAST(Total_Encerrados AS STRING) AS Total_Encerrados,

        CAST(NULL AS STRING) AS JEC_Qty_Acordo,
        CAST(NULL AS STRING) AS JC_Qty_Acordo,
        CAST(NULL AS STRING) AS Procon_Qty_Acordo,
        CAST(Total_Qty_Acordo AS STRING) AS Total_Qty_Acordo,

        CAST(NULL AS STRING) AS JEC_Qty_Ganhamos,
        CAST(NULL AS STRING) AS JC_Qty_Ganhamos,
        CAST(NULL AS STRING) AS Procon_Qty_Ganhamos,
        CAST(Total_Qty_Ganhamos AS STRING) AS Total_Qty_Ganhamos,

        CAST(NULL AS STRING) AS JEC_Qty_Perdemos,
        CAST(NULL AS STRING) AS JC_Qty_Perdemos,
        CAST(NULL AS STRING) AS Procon_Qty_Perdemos,
        CAST(Total_Qty_Perdemos AS STRING) AS Total_Qty_Perdemos,

        CAST(NULL AS STRING) AS JEC_Qty_Desistido,
        CAST(NULL AS STRING) AS JC_Qty_Desistido,
        CAST(NULL AS STRING) AS Procon_Qty_Desistido,
        CAST(Total_Qty_Desistido AS STRING) AS Total_Qty_Desistido,

        CAST(NULL AS STRING) AS JEC_Qty_Outros,
        CAST(NULL AS STRING) AS JC_Qty_Outros,
        CAST(NULL AS STRING) AS Procon_Qty_Outros,
        CAST(Total_Qty_Outros AS STRING) AS Total_Qty_Outros,

        CAST(NULL AS STRING) AS JEC_TM_Acordo,
        CAST(NULL AS STRING) AS JC_TM_Acordo,
        CAST(NULL AS STRING) AS Procon_TM_Acordo,
        CAST(TM_Acordo AS STRING) AS TM_Acordo,

        CAST(NULL AS STRING) AS JEC_TM_Ganhamos,
        CAST(NULL AS STRING) AS JC_TM_Ganhamos,
        CAST(NULL AS STRING) AS Procon_TM_Ganhamos,
        CAST(TM_Ganhamos AS STRING) AS TM_Ganhamos,

        CAST(NULL AS STRING) AS JEC_TM_Perdemos,
        CAST(NULL AS STRING) AS JC_TM_Perdemos,
        CAST(NULL AS STRING) AS Procon_TM_Perdemos,
        CAST(TM_Perdemos AS STRING) AS TM_Perdemos,

        CAST(NULL AS STRING) AS JEC_TM_Desistido,
        CAST(NULL AS STRING) AS JC_TM_Desistido,
        CAST(NULL AS STRING) AS Procon_TM_Desistido,
        CAST(TM_Desistido AS STRING) AS TM_Desistido,

        CAST(NULL AS STRING) AS JEC_TM_Outros,
        CAST(NULL AS STRING) AS JC_TM_Outros,
        CAST(NULL AS STRING) AS Procon_TM_Outros,
        CAST(TM_Outros AS STRING) AS TM_Outros

    FROM `<ENV>.STG.BUDGET_ACTUAL_ARG`
),

BASE_MEXICO AS (
    SELECT
        CAST(pais AS STRING) AS pais,
        CAST(Visao AS STRING) AS Visao,
        CAST(Objeto AS STRING) AS Objeto,
        CAST(Anomes AS STRING) AS Anomes,
        SUBSTR(CAST(Anomes AS STRING), 1, 4) AS Ano,

        CAST(NULL AS STRING) AS Entradas_JEC,
        CAST(NULL AS STRING) AS Entradas_JC,
        CAST(NULL AS STRING) AS Entradas_Procon,
        CAST(Total_Entradas AS STRING) AS Total_Entradas,

        CAST(NULL AS STRING) AS Encerrados_JEC,
        CAST(NULL AS STRING) AS Encerrados_JC,
        CAST(NULL AS STRING) AS Encerrados_Procon,
        CAST(Total_Encerrados AS STRING) AS Total_Encerrados,

        CAST(NULL AS STRING) AS JEC_Qty_Acordo,
        CAST(NULL AS STRING) AS JC_Qty_Acordo,
        CAST(NULL AS STRING) AS Procon_Qty_Acordo,
        CAST(Total_Qty_Acordo AS STRING) AS Total_Qty_Acordo,

        CAST(NULL AS STRING) AS JEC_Qty_Ganhamos,
        CAST(NULL AS STRING) AS JC_Qty_Ganhamos,
        CAST(NULL AS STRING) AS Procon_Qty_Ganhamos,
        CAST(Total_Qty_Ganhamos AS STRING) AS Total_Qty_Ganhamos,

        CAST(NULL AS STRING) AS JEC_Qty_Perdemos,
        CAST(NULL AS STRING) AS JC_Qty_Perdemos,
        CAST(NULL AS STRING) AS Procon_Qty_Perdemos,
        CAST(Total_Qty_Perdemos AS STRING) AS Total_Qty_Perdemos,

        CAST(NULL AS STRING) AS JEC_Qty_Desistido,
        CAST(NULL AS STRING) AS JC_Qty_Desistido,
        CAST(NULL AS STRING) AS Procon_Qty_Desistido,
        CAST(Total_Qty_Desistido AS STRING) AS Total_Qty_Desistido,

        CAST(NULL AS STRING) AS JEC_Qty_Outros,
        CAST(NULL AS STRING) AS JC_Qty_Outros,
        CAST(NULL AS STRING) AS Procon_Qty_Outros,
        CAST(Total_Qty_Outros AS STRING) AS Total_Qty_Outros,

        CAST(NULL AS STRING) AS JEC_TM_Acordo,
        CAST(NULL AS STRING) AS JC_TM_Acordo,
        CAST(NULL AS STRING) AS Procon_TM_Acordo,
        CAST(TM_Acordo AS STRING) AS TM_Acordo,

        CAST(NULL AS STRING) AS JEC_TM_Ganhamos,
        CAST(NULL AS STRING) AS JC_TM_Ganhamos,
        CAST(NULL AS STRING) AS Procon_TM_Ganhamos,
        CAST(TM_Ganhamos AS STRING) AS TM_Ganhamos,

        CAST(NULL AS STRING) AS JEC_TM_Perdemos,
        CAST(NULL AS STRING) AS JC_TM_Perdemos,
        CAST(NULL AS STRING) AS Procon_TM_Perdemos,
        CAST(TM_Perdemos AS STRING) AS TM_Perdemos,

        CAST(NULL AS STRING) AS JEC_TM_Desistido,
        CAST(NULL AS STRING) AS JC_TM_Desistido,
        CAST(NULL AS STRING) AS Procon_TM_Desistido,
        CAST(TM_Desistido AS STRING) AS TM_Desistido,

        CAST(NULL AS STRING) AS JEC_TM_Outros,
        CAST(NULL AS STRING) AS JC_TM_Outros,
        CAST(NULL AS STRING) AS Procon_TM_Outros,
        CAST(TM_Outros AS STRING) AS TM_Outros

    FROM `<ENV>.STG.BUDGET_ACTUAL_MEX`
),

BASE_CONSOLIDADA_REAL AS (
    SELECT * FROM BASE_BRASIL
    UNION ALL
    SELECT * FROM BASE_ARGENTINA
    UNION ALL
    SELECT * FROM BASE_MEXICO
),

BASE_BUDGET AS (
    SELECT
        CAST(Pais AS STRING) AS Pais,
        'Budget' AS Visao,
        CAST(Objeto AS STRING) AS Objeto,
        CAST(Anomes AS STRING) AS Anomes,
        SUBSTR(CAST(Anomes AS STRING), 1, 4) AS Ano,

        CAST(Entradas_JEC AS STRING) AS Entradas_JEC,
        CAST(Entradas_JC AS STRING) AS Entradas_JC,
        CAST(Entradas_Procon AS STRING) AS Entradas_Procon,
        CAST(Entradas AS STRING) AS Total_Entradas,

        CAST(Encerrados_JEC AS STRING) AS Encerrados_JEC,
        CAST(Encerrados_JC AS STRING) AS Encerrados_JC,
        CAST(Encerrados_Procon AS STRING) AS Encerrados_Procon,
        CAST(Encerrados AS STRING) AS Total_Encerrados,

        CAST(JEC_Qty_Acordo AS STRING) AS JEC_Qty_Acordo,
        CAST(JC_Qty_Acordo AS STRING) AS JC_Qty_Acordo,
        CAST(Procon_Qty_Acordo AS STRING) AS Procon_Qty_Acordo,
        CAST(Qty_Acordo AS STRING) AS Total_Qty_Acordo,

        CAST(JEC_Qty_Ganhamos AS STRING) AS JEC_Qty_Ganhamos,
        CAST(JC_Qty_Ganhamos AS STRING) AS JC_Qty_Ganhamos,
        CAST(Procon_Qty_Ganhamos AS STRING) AS Procon_Qty_Ganhamos,
        CAST(Qty_Ganhamos AS STRING) AS Total_Qty_Ganhamos,

        CAST(JEC_Qty_Perdemos AS STRING) AS JEC_Qty_Perdemos,
        CAST(JC_Qty_Perdemos AS STRING) AS JC_Qty_Perdemos,
        CAST(Procon_Qty_Perdemos AS STRING) AS Procon_Qty_Perdemos,
        CAST(Qty_Perdemos AS STRING) AS Total_Qty_Perdemos,

        CAST(JEC_Qty_Desistido AS STRING) AS JEC_Qty_Desistido,
        CAST(JC_Qty_Desistido AS STRING) AS JC_Qty_Desistido,
        CAST(Procon_Qty_Desistido AS STRING) AS Procon_Qty_Desistido,
        CAST(Qty_Desistido AS STRING) AS Total_Qty_Desistido,

        CAST(JEC_Qty_Outros AS STRING) AS JEC_Qty_Outros,
        CAST(JC_Qty_Outros AS STRING) AS JC_Qty_Outros,
        CAST(Procon_Qty_Outros AS STRING) AS Procon_Qty_Outros,
        CAST(Qty_Outros AS STRING) AS Total_Qty_Outros,

        CAST(JEC_TM_Acordo AS STRING) AS JEC_TM_Acordo,
        CAST(JC_TM_Acordo AS STRING) AS JC_TM_Acordo,
        CAST(Procon_TM_Acordo AS STRING) AS Procon_TM_Acordo,
        CAST(TM_Acordo AS STRING) AS TM_Acordo,

        CAST(JEC_TM_Ganhamos AS STRING) AS JEC_TM_Ganhamos,
        CAST(JC_TM_Ganhamos AS STRING) AS JC_TM_Ganhamos,
        CAST(Procon_TM_Ganhamos AS STRING) AS Procon_TM_Ganhamos,
        CAST(TM_Ganhamos AS STRING) AS TM_Ganhamos,

        CAST(JEC_TM_Perdemos AS STRING) AS JEC_TM_Perdemos,
        CAST(JC_TM_Perdemos AS STRING) AS JC_TM_Perdemos,
        CAST(Procon_TM_Perdemos AS STRING) AS Procon_TM_Perdemos,
        CAST(TM_Perdemos AS STRING) AS TM_Perdemos,

        CAST(NULL AS STRING) AS JEC_TM_Desistido,
        CAST(NULL AS STRING) AS JC_TM_Desistido,
        CAST(NULL AS STRING) AS Procon_TM_Desistido,
        CAST(NULL AS STRING) AS TM_Desistido,

        CAST(NULL AS STRING) AS JEC_TM_Outros,
        CAST(NULL AS STRING) AS JC_TM_Outros,
        CAST(NULL AS STRING) AS Procon_TM_Outros,
        CAST(NULL AS STRING) AS TM_Outros
    FROM `<ENV>.STG.BUDGET_CORACAO_FATO`
)


-- Resultado Final Consolidado
SELECT * FROM BASE_CONSOLIDADA_REAL
UNION ALL
SELECT * FROM BASE_BUDGET;
