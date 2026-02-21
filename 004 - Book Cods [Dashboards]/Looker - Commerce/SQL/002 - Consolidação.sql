CREATE
OR REPLACE TABLE `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_FULL` AS WITH unified_data AS (
    SELECT
        Responsavel,
        Solicitante,
        Data_de_solicitacao,
        CAST(NULL AS TIME) AS Hora_de_solicitacao,
        Ariba_CLM,
        Nome_contraparte,
        Objeto,
        Descricao,
        Valor_global,
        Expectativa_GMV,
        Cost_Avoidance,
        Cost_Saving,
        Data_Entrega,
        CAST(NULL AS TIME) AS Hora_Entrega,
        Area,
        UPPER(Status_Macro) AS Status_Macro,
        UPPER(Status_Micro) AS Status_Micro,
        -- Extrai o ano diretamente da data de solicitação
        EXTRACT(
            YEAR
            FROM
                Data_de_solicitacao
        ) AS Ano
    FROM
        `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_2021`
    UNION
    ALL
    SELECT
        Responsavel,
        Solicitante,
        Data_de_solicitacao,
        CAST(NULL AS TIME) AS Hora_de_solicitacao,
        Ariba_CLM,
        Nome_contraparte,
        Objeto,
        Descricao,
        Valor_global,
        Expectativa_GMV,
        Cost_Avoidance,
        Cost_Saving,
        Data_Entrega,
        CAST(NULL AS TIME) AS Hora_Entrega,
        Area,
        UPPER(Status_Macro) AS Status_Macro,
        UPPER(Status_Micro) AS Status_Micro,
        -- Extrai o ano diretamente da data de solicitação
        EXTRACT(
            YEAR
            FROM
                Data_de_solicitacao
        ) AS Ano
    FROM
        `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_2022`
    UNION
    ALL
    SELECT
        Responsavel,
        Solicitante,
        Data_de_solicitacao,
        CAST(NULL AS TIME) AS Hora_de_solicitacao,
        Ariba_CLM,
        Nome_contraparte,
        Objeto,
        Descricao,
        Valor_global,
        Expectativa_GMV,
        Cost_Avoidance,
        Cost_Saving,
        Data_Entrega,
        CAST(NULL AS TIME) AS Hora_Entrega,
        Area,
        UPPER(Status_Macro) AS Status_Macro,
        UPPER(Status_Micro) AS Status_Micro,
        -- Extrai o ano diretamente da data de solicitação
        EXTRACT(
            YEAR
            FROM
                Data_de_solicitacao
        ) AS Ano
    FROM
        `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_2023`
    UNION
    ALL
    SELECT
        Responsavel,
        Solicitante,
        Data_de_solicitacao,
        CAST(NULL AS TIME) AS Hora_de_solicitacao,
        Ariba_CLM,
        Nome_contraparte,
        Objeto,
        Descricao,
        Valor_global,
        Expectativa_GMV,
        Cost_Avoidance,
        Cost_Saving,
        Data_Entrega,
        CAST(NULL AS TIME) AS Hora_Entrega,
        Area,
        UPPER(Status_Macro) AS Status_Macro,
        UPPER(Status_Micro) AS Status_Micro,
        -- Extrai o ano diretamente da data de solicitação
        EXTRACT(
            YEAR
            FROM
                Data_de_solicitacao
        ) AS Ano
    FROM
        `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_2024`
    UNION
    ALL
    SELECT
        Responsavel,
        Solicitante,
        Data_de_solicitacao,
        SAFE.PARSE_TIME('%H:%M', Hora_de_solicitacao) AS Hora_de_solicitacao,
        Ariba_CLM,
        Nome_contraparte,
        Objeto,
        Descricao,
        Valor_global,
        Expectativa_GMV,
        Cost_Avoidance,
        Cost_Saving,
        Data_Entrega,
        SAFE.PARSE_TIME('%H:%M', Hora_Entrega) AS Hora_Entrega,
        Area,
        UPPER(Status_Macro) AS Status_Macro,
        UPPER(Status_Micro) AS Status_Micro,
        -- Extrai o ano diretamente da data de solicitação
        EXTRACT(
            YEAR
            FROM
                Data_de_solicitacao
        ) AS Ano
    FROM
        `ddme000426-gopr4nla6zo-furyid.STG.COMMERCE_DATABASE_2025`
)
SELECT
    *
FROM
    unified_data
WHERE
    Responsavel IS NOT NULL;