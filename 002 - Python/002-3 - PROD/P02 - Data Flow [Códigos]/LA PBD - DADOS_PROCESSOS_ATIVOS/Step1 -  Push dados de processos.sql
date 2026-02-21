CREATE OR REPLACE EXTERNAL TABLE `<ENV>.STG.INPUT_DE_IDS` (
    Cust_ID_Autor STRING
)
OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = 'Input_Manual!A:A',
    uris = ['https://docs.google.com/spreadsheets/d/1jODz75dZM_-o3b-IKLzrdiXJy0M57KWIkh09v_Ddxso']
);

CREATE OR REPLACE TABLE `<ENV>.STG.Tab_ids_processos_ativos` AS
WITH BASE_1 AS (
    SELECT DISTINCT
        LEFT(CUST_ID_AUTOR, 10) AS CUST_ID_AUTOR
    FROM
        `<ENV>.TBL.LK_PBD_LA_ELAW_CONTENCIOSO_HISPANOS_ONGOING`
    WHERE
        pais IN ("Argentina", "México")
        AND status = "Ativo"
        AND CUST_ID_AUTOR IS NOT NULL

    UNION ALL

    SELECT DISTINCT
        LEFT(CUST_ID_AUTOR, 10) AS CUST_ID_AUTOR
    FROM
        `<ENV>.TBL.LK_PBD_LA_ELAW_CONTENCIOSO_BRASIL_ONGOING`
    WHERE
        status = "Ativo"
        AND CUST_ID_AUTOR IS NOT NULL
)
SELECT DISTINCT Cust_ID_Autor
FROM (
    SELECT Cust_ID_Autor FROM `<ENV>.STG.INPUT_DE_IDS`
    UNION ALL
    SELECT Cust_ID_Autor FROM BASE_1
)
WHERE
    Cust_ID_Autor IS NOT NULL
    AND Cust_ID_Autor != '';
