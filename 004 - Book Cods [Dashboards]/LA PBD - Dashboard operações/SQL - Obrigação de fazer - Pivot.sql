-- DEV
-- pdme000426-c1s7scatwm0-furyid

-- PROD
-- pdme000426-c1s7scatwm0-furyid

-- 1) Use a CTE com a query anterior
WITH obrigacoes_base AS (
  SELECT
    SAFE_CAST(processo_id                AS INT64)      AS processo_id,
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado,1,10))      AS data_registrado,
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_de_confirmacao,1,10))  AS data_de_confirmacao,
    COALESCE(processo_qual_a_solicitacao_da_obf, '')              AS solicitacoes
  FROM
    `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_OBRIGACOES_DE_FAZER`
),


solicitacoes_exploded AS (
  SELECT
    processo_id,
    data_registrado,
    data_de_confirmacao,
    TRIM(item) AS solicitacao
  FROM
    obrigacoes_base,
    UNNEST(SPLIT(solicitacoes, ',')) AS item
)

-- 3) Resultado final sem duplicatas e sem valores vazios
SELECT DISTINCT
  processo_id,
  data_registrado,
  data_de_confirmacao,
  solicitacao
FROM
  solicitacoes_exploded
WHERE
  solicitacao <> ''
ORDER BY
  processo_id,
  data_registrado,
  data_de_confirmacao,
  solicitacao
