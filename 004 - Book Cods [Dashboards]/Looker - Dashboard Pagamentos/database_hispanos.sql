WITH base AS (
  SELECT
    id,
    pais,
    equipo,
    SAFE_CAST(valor AS NUMERIC) AS valor_num,
    fecha_registro
  FROM `pdme000426-c1s7scatwm0-furyid.STG.Database_Pagamentos_Hispanos`
  WHERE REGEXP_CONTAINS(fecha_registro, r'^\d{4}-\d{2}-\d{2}')
)

SELECT
  pais,
  equipo,
  EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%d %H:%M:%S', fecha_registro)) AS ano,
  EXTRACT(MONTH FROM PARSE_DATETIME('%Y-%m-%d %H:%M:%S', fecha_registro)) AS mes,
  COUNT(id) AS total_ids,
  SUM(valor_num) AS total_valor
FROM base
GROUP BY
  pais, equipo, ano, mes
ORDER BY
  ano, mes, pais, equipo;
