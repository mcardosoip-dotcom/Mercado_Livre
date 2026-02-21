SELECT
    *,
    CASE
        WHEN DATE_DIFF(PARSE_DATE('%d/%m/%Y', fecha_de_expiracion), CURRENT_DATE(), DAY) <= 0 THEN 'Expirado'
        WHEN DATE_DIFF(PARSE_DATE('%d/%m/%Y', fecha_de_expiracion), CURRENT_DATE(), DAY) BETWEEN 1 AND 30 THEN 'Expira em 0-30 dias'
        WHEN DATE_DIFF(PARSE_DATE('%d/%m/%Y', fecha_de_expiracion), CURRENT_DATE(), DAY) BETWEEN 31 AND 60 THEN 'Expira em 31-60 dias'
        WHEN DATE_DIFF(PARSE_DATE('%d/%m/%Y', fecha_de_expiracion), CURRENT_DATE(), DAY) BETWEEN 61 AND 90 THEN 'Expira em 61-90 dias'
        WHEN DATE_DIFF(PARSE_DATE('%d/%m/%Y', fecha_de_expiracion), CURRENT_DATE(), DAY) BETWEEN 91 AND 120 THEN 'Expira em 91-120 dias'
        ELSE 'Expira em mais de 120 dias'
    END AS fecha_de_expiracion_range
FROM
    `pdme000426-c1s7scatwm0-furyid.STG.CLM_CONTROL_DE_CONTRATOS`;