-- Consulta combinada com tratamento de colunas numéricas e campo de data
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
    SAFE.PARSE_DATE('%d/%m/%Y', Data) AS Data,  -- Tratamento do campo de data

    COALESCE(SAFE_CAST(Entradas     AS INT64), 0) AS Entradas,
    COALESCE(SAFE_CAST(Descartados AS INT64), 0) AS Descartados,
    COALESCE(SAFE_CAST(Tratados    AS INT64), 0) AS Tratados,
    COALESCE(SAFE_CAST(Backlog     AS INT64), 0) AS Backlog,

    Provedor,
    Modalidade,
    Origem

  FROM TABELA
  WHERE Provedor IS NOT NULL
)

SELECT * FROM Clean
where Entradas <> 0  and Descartados<>0 and Tratados <>0 and Backlog<>0