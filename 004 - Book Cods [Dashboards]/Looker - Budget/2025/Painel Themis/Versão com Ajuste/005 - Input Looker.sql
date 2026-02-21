SELECT
    A.Versao AS Versao,
    A.Ano AS Ano,
    A.Mes AS Mes,
    A.Country AS COUNTRY,
    A.Area AS AREA,
    A.Agrupador_1 AS AGRUPADOR_1,
    -- Remove 'Legal Fees - ' do início do campo Agrupador_2
    REGEXP_REPLACE(A.Agrupador_2, r'^Legal Fees - ', '') AS AGRUPADOR_2,
    IFNULL(A.Account_name, 'NA') AS Account_name,
    A.Vendor_Desc,
    B.Vendor_desc_final AS Vendor_Desc_final,
    -- Substitui se houver correspondência
    A.Item_Text AS Item_Text,
    FORMAT('%0.2f', SAFE_CAST(A.Valor_Local AS FLOAT64)) AS Valor_Local,
    FORMAT('%0.2f', SAFE_CAST(A.Valor_USD AS FLOAT64)) AS Valor_USD
FROM
    `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_LOOKER_Input` AS A
    LEFT JOIN `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR_FATO` AS B ON a.Vendor_Desc = b.Vendor_Desc