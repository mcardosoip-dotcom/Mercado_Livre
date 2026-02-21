SELECT
  SAFE.PARSE_DATE('%d/%m/%Y', T1.data_registrado) AS data_registrado,
  COUNT(DISTINCT T1.processo_id) AS quantidade_casos
FROM
  `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_AMELIA_SHARE` AS T1
WHERE
  SAFE.PARSE_DATE('%d/%m/%Y', T1.data_registrado) IS NOT NULL
  AND SAFE.PARSE_DATE('%d/%m/%Y', T1.data_registrado) >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY)
  AND SAFE.PARSE_DATE('%d/%m/%Y', T1.data_registrado) <= CURRENT_DATE()
GROUP BY
  SAFE.PARSE_DATE('%d/%m/%Y', T1.data_registrado)
ORDER BY
  data_registrado DESC;
