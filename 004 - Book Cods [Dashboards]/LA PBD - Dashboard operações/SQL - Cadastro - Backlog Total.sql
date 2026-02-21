-- Backlog por provedor na data mais recente (tratando datas como texto)
WITH TABELA AS (
  SELECT 
    Data,
    Entradas,
    Descartados,
    Tratados,
    Backlog,
    Provedor,
    Modalidade,
    'ENLIGHTEN' AS Origem
  FROM `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN_FATO`

  UNION ALL

  SELECT 
    Data,
    Entradas,
    Descartados,
    Tratados,
    Backlog,
    Provedor,
    Modalidade,
    'FINCH' AS Origem
  FROM `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH_FATO`
),

Clean AS (
  SELECT
    Provedor,
    COALESCE(SAFE_CAST(Backlog AS INT64), 0) AS Backlog,
    SAFE.PARSE_DATE('%d/%m/%Y', Data) AS Data_Convertida
  FROM TABELA
  WHERE Provedor IS NOT NULL
),

Ultima_Data AS (
  SELECT
    Provedor,
    MAX(Data_Convertida) AS Data_Maxima
  FROM Clean
  GROUP BY Provedor
),

Backlog_Acumulado AS (
  SELECT 
    c.Provedor,
    u.Data_Maxima,
    SUM(c.Backlog) AS Backlog_Total
  FROM Clean c
  JOIN Ultima_Data u
    ON c.Provedor = u.Provedor AND c.Data_Convertida = u.Data_Maxima
  GROUP BY c.Provedor, u.Data_Maxima
)

SELECT * FROM Backlog_Acumulado
