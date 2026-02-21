WITH
-- CAP: fonte principal, já filtrando e renomeando colunas
cap AS (
  SELECT
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data         AS STRING)) AS registro_tarefa,
    fase_de_workflow,
    id,
    status,
    workflow,
    pais,
    estado,
    status_1                   AS status_tarefa,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado AS STRING)) AS data_registrado,
    objeto_3,
    usuario
  FROM
    `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP`
),

-- CAP_CX: mesma lógica sobre a fonte CX
cap_cx AS (
  SELECT
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data         AS STRING)) AS data_registrado,
    fase_de_workflow,
    id,
    status,
    workflow,
    pais,
    estado,
    status_1                   AS status_tarefa,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado AS STRING)) AS registro_processo,
    objeto_3,
    usuario
  FROM
    `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX`
),

-- OPS: mesma seleção aplicada à fonte OPS_ENLI
ops_1 AS (
  SELECT
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data         AS STRING)) AS data_registrado,
    fase_de_workflow,
    id,
    status,
    workflow,
    pais,
    estado,
    status_1                   AS status_tarefa,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado_1 AS STRING)) AS registro_processo,
    objeto_3,
    usuario
  FROM
    `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI`
),

ops_2 AS (
  SELECT
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data         AS STRING)) AS data_registrado,
    fase_de_workflow,
    id,
    status,
    workflow,
    pais,
    estado,
    status_1                   AS status_tarefa,
    SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado_1 AS STRING)) AS registro_processo,
    objeto_3,
    usuario
  FROM  `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER`
),

-- União final
raw_hsp AS (
SELECT * FROM cap
UNION ALL
SELECT * FROM cap_cx
UNION ALL
SELECT * FROM ops_1
UNION ALL
SELECT * FROM ops_2),

processed as (
SELECT 

UPPER(fase_de_workflow)                                        AS fase_de_workflow,
UPPER(workflow)                                                AS workflow,
objeto_3                 AS objeto,
'Enlighten'                                                    AS empresa,
DATE_DIFF(data_de_confirmacao, data_registrado, DAY)         AS tempo_medio_resposta,
* EXCEPT (fase_de_workflow,workflow)

FROM raw_hsp),

final AS (
  SELECT
    p.* ,
    df.grupo                                                     AS tipo_tarefa
  FROM processed p
  LEFT JOIN `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_DIM_WORKFLOW` df
    ON UPPER(TRIM(p.workflow)) = UPPER(TRIM(df.workflow))
   AND UPPER(TRIM(p.fase_de_workflow)) = UPPER(TRIM(df.fase_de_workflow))
  WHERE df.Considerar = 'Sim'
),

final_hsp AS (
SELECT
  data_registrado,
  processo_id,
  area_do_direito,
  sub_area_do_direito,
  data_de_confirmacao,
  registro_tarefa,
  fase_de_workflow,
  id,
  status,
  workflow,
  pais,
  estado,
  status_tarefa,
  usuario,
  objeto,
  empresa,
  tempo_medio_resposta,
  tipo_tarefa,
  CAST(NULL AS STRING) AS procedimento_judicial,
  CAST(NULL AS STRING) AS processo_classificacao
FROM final),



base_bra AS(

SELECT
  a.processo_id,
  a.status,
  SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado)                                     AS data_registrado,
  SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado_1)                                   AS registro_tarefa,
  SAFE.PARSE_DATE('%d/%m/%Y', a.data_de_confirmacao)                                 AS data_de_confirmacao,
  a.area_do_direito,
  a.sub_area_do_direito,
  UPPER(TRIM(a.fase_de_workflow))                                                     AS fase_workflow,
  a.id,
  a.status_1                                                                          AS status_tarefa,
  a.responsavel                                                                       AS usuario,
  UPPER(TRIM(a.workflow))                                                             AS workflow,
  a.pais,
  a.estado,
  CAST(a.processo_procedimento_judicial as STRING)                                                    AS procedimento_judicial,
  CAST(a.processo_objeto_unidade_de_negocio as STRING)                                                AS objeto_unidade_negocio,
  a.processo_objeto_objeto                                                            AS objeto,
  a.processo_indicar_ajuste_nome_do_campo_erro_detalhamento                           AS indicador_ajuste_erro,
  a.processo_informar_ajustes,
  a.processo_informar_ajustes_1                                                       AS informar_ajustes_1,
  a.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1                         AS indicador_ajuste_erro_1,
  a.processo_motivo_do_ajuste                                                        AS motivo_ajuste,
  a.processo_pedido_de_ajuste_foi_correto                                            AS pedido_ajuste_correto,
  a.processo_motivo_do_ajuste_1                                                       AS motivo_ajuste_1,
  a.processo_prazo                                                                    AS prazo,
  CAST(a.processo_classificacao as STRING)                                                            AS processo_classificacao,
  a.tarefas_data_do_prazo                                                             AS tarefas_data_prazo,
  a.aud_ins_dttm                                                                      AS aud_ins_dttm,
  a.aud_upd_dttm                                                                      AS aud_upd_dttm,
  CASE 
    WHEN a.estado IN ('MG','RJ','SP') THEN 'Finch' 
    ELSE 'Enlighten' 
  END                                                                                 AS empresa,
  IFNULL(
    DATE_DIFF(
      SAFE.PARSE_DATE('%d/%m/%Y', a.data_de_confirmacao),
      SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado),
      DAY
    ),
    0
  )                                                                                   AS tempo_medio_resposta,
  df.grupo                                                                             AS tipo_tarefa
FROM
  `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_VW_TAREFAS_AGENDAMENTOS_CLEAN` AS a
LEFT JOIN
  `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_DIM_WORKFLOW` AS df
    ON UPPER(TRIM(a.workflow)) = UPPER(TRIM(df.workflow))
   AND UPPER(TRIM(a.fase_de_workflow)) = UPPER(TRIM(df.fase_de_workflow))
WHERE
  df.considerar = 'Sim'
QUALIFY
  ROW_NUMBER() OVER (
    PARTITION BY a.processo_id, a.id
    ORDER BY SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado)
  ) = 1
),
final_bra_trim AS (

  SELECT
    data_registrado,
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    data_de_confirmacao,
    registro_tarefa,
    fase_workflow       AS fase_de_workflow,  
    id,
    status,
    workflow,
    pais,
    estado,
    status_tarefa,
    usuario,
    objeto,
    empresa,
    tempo_medio_resposta,
    tipo_tarefa,
    procedimento_judicial,
    processo_classificacao
  FROM base_bra
),


united AS (
  SELECT * FROM final_bra_trim
  UNION ALL
  SELECT * FROM final_hsp
),

filtrado AS (
  SELECT
    *,
    CASE WHEN empresa IN ('Finch','') THEN 'Enlighten' ELSE empresa END                AS empresa_norm,
    COALESCE(tipo_tarefa, 'Complementação de subsídio')                                AS tipo_tarefa_norm
  FROM united
  WHERE area_do_direito <> 'Requerimentos'
    AND area_do_direito IN (
      'Consumidor',
      'CORP - Civil',
      'CORP - Consumidor',
      'Cível'
    )
),


dedup AS (
  SELECT
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    data_registrado,
    registro_tarefa,
    data_de_confirmacao,
    fase_de_workflow,
    id,
    status,
    workflow,
    pais,
    estado,
    usuario,
    objeto,
    tempo_medio_resposta,
    tipo_tarefa_norm   AS tipo_tarefa,
    status_tarefa,
    procedimento_judicial,
    processo_classificacao,
    empresa_norm       AS empresa
  FROM filtrado
  QUALIFY
    ROW_NUMBER() OVER (
      PARTITION BY processo_id, id
      ORDER BY data_registrado DESC
    ) = 1
),


subsidios AS (
  SELECT
    d.*,
    CASE
      WHEN UPPER(TRIM(fase_de_workflow)) = 'ELABORAR SUBSÍDIOS' THEN 'Subsídios_BR'
      WHEN UPPER(TRIM(fase_de_workflow)) IN ('CONFECCIÓN DEL SUBSÍDIO','CONFECCIÓN DEL SUBSIDIO') THEN 'Subsídios_HSP'
      ELSE NULL
    END AS tc_subsidios,
    CASE
      WHEN UPPER(TRIM(fase_de_workflow)) = 'ELABORAR COMPLEMENTAÇÃO DE SUBSÍDIOS' THEN 'Complementação_BR'
      WHEN UPPER(TRIM(fase_de_workflow)) IN ('PROVIDÊNCIA - CAP','COMPLEMENTAÇÃO DE SUBSÍDIOS - ENL') THEN 'Complementação_HSP'
      ELSE NULL
    END AS tc_complementacao
  FROM dedup AS d
 
  WHERE workflow IN (
    'CADASTRO/SUBSÍDIOS - CÍVEL JUDICIAL E ADMINISTRATIVO',
    'CADASTRO/SUBSÍDIOS - CONSUMIDOR JUDICIAL',
    'CADASTRO/SUBSÍDIOS PRÉ ADMINISTRATIVO/ ADMINISTRATIVO - CONSUMIDOR',
    'COMPLEMENTAÇÃO SUBSÍDIOS (ACIONAMENTO AVULSO)',
    'RECOVERY - SUBSÍDIOS',
    'SUBSÍDIOS AVULSO - BASE MIGRADA',
    'ACIONAMENTO - SUBSÍDIOS',
    'HISP - SUBSIDIOS GERAL'
  )
  
)


SELECT DISTINCT *
FROM subsidios