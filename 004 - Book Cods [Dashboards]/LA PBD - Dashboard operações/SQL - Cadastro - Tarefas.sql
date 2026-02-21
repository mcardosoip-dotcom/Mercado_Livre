WITH filtrado_e_parse AS (
  SELECT
    t.*, 
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(t.DATA_REGISTRADO,       1, 10)) AS parsed_registrado,
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(t.DATA_DE_CONFIRMACAO, 1, 10)) AS parsed_confirmacao
  FROM
    `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_VW_TAREFAS_AGENDAMENTOS_CLEAN` AS t
  INNER JOIN
    `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_DIM_WORKFLOW_REVIEW` AS w
    ON t.FASE_DE_WORKFLOW = w.FASE_DE_WORKFLOW
  WHERE
    -- Filtros da tabela dimensional (w)
    w.CONSIDERAR = 'Sim'
    AND w.GRUPO = 'Cadastro'
    -- Filtro da tabela principal (t)
    AND t.PAIS = 'Brasil'
)
SELECT
  * EXCEPT(
    DATA_REGISTRADO,
    DATA_DE_CONFIRMACAO,
    parsed_registrado,
    parsed_confirmacao
  ),

  parsed_registrado  AS DATA_REGISTRADO,
  parsed_confirmacao AS DATA_DE_CONFIRMACAO,

  DATE_DIFF(parsed_confirmacao, parsed_registrado, DAY)
    AS `SLA - Registro e Confirmação`
FROM
  filtrado_e_parse