SELECT
  EXTRACT(YEAR FROM PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', prazo_fatal)) AS ano,
  EXTRACT(MONTH FROM PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', prazo_fatal)) AS mes,
  FORMAT_TIMESTAMP('%B', PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', prazo_fatal)) AS mes_nome,

  empresa,
  tipo_de_transferencia,
  centro_de_custo_materia,
  area_do_direito,
  objeto_da_acao,
  status,

  COUNT(`nº_legales`) AS total_ids,

  SUM(CAST(importe AS FLOAT64)) AS total_importe

FROM `pdme000426-c1s7scatwm0-furyid.STG.Database_Pagamentos_Brasil`

GROUP BY
  ano, mes, mes_nome,
  empresa,
  tipo_de_transferencia,
  centro_de_custo_materia,
  area_do_direito,
  objeto_da_acao,
  status

ORDER BY ano, mes;
