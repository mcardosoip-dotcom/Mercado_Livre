-- ====================================================================================
-- VERSÃO COM CONTROLE DE DUPLICIDADE POR HIERARQUIA DE FONTE
--
-- Diferenças em relação à versão original:
--
-- 1. Correção da duplicidade de PROCESSO_ID entre bases
--    Na versão anterior, quando um mesmo processo existia em mais de uma base
--    (INCOMING, OUTGOING ou ONGOING), a escolha do registro era feita apenas
--    pela data de registro, o que podia resultar em seleção inconsistente.
--
-- 2. Introdução de hierarquia explícita entre as fontes
--    Foi criada a coluna PRIORIDADE_FONTE para definir precedência:
--      1 = OUTGOING
--      2 = INCOMING
--      3 = ONGOING
--    Essa hierarquia reflete o estado mais confiável do processo.
--
-- 3. Deduplicação determinística
--    O ROW_NUMBER passou a ordenar primeiro pela PRIORIDADE_FONTE e
--    somente depois pela DATA_REGISTRADO_TRATADA, garantindo que:
--      • OUTGOING sempre prevaleça sobre INCOMING e ONGOING
--      • INCOMING prevaleça sobre ONGOING
--      • dentro da mesma fonte, o registro mais recente seja mantido
--
-- 4. Preservação do resultado final
--    Nenhuma regra de negócio adicional foi alterada.
--    Joins, colunas derivadas, enriquecimentos e classificação de MUNDO
--    permanecem idênticos à versão original.
--
-- 5. Impacto controlado
--    A mudança afeta exclusivamente a lógica de escolha do registro
--    quando há duplicidade de PROCESSO_ID entre bases distintas.
-- ====================================================================================


CREATE OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS` AS

WITH
-- ====================================================================================
-- MULTAS: mantém apenas a multa mais recente por processo
-- ====================================================================================
MULTAS AS (
  SELECT
    * EXCEPT (RN)
  FROM (
    SELECT
      em.PROCESSO_ID AS PROCESSOID,
      em.DATA AS MULTA_DATA,
      dm.TIPO_AJUSTADO AS MULTA_TIPO_AJUSTADO,
      ROW_NUMBER() OVER (
        PARTITION BY em.PROCESSO_ID
        ORDER BY em.DATA DESC
      ) AS RN
    FROM `<ENV>.TBL.LK_PBD_LA_ELAW_REPORT_EXTRACAO_MULTAS` em
    LEFT JOIN `<ENV>.STG.DIM_16_DIMENSAO_MULTA` dm
      ON em.TIPO = dm.TIPO
  )
  WHERE RN = 1
),

-- ====================================================================================
-- IDs de pagamento unificados
-- ====================================================================================
update_de_ids_pagamento AS (
  SELECT DISTINCT
    processo_id,
    hisp_subsidios_id_da_operacao_mp
  FROM (
    SELECT processo_id, hisp_subsidios_id_da_operacao_mp
    FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_ONGOING_FINAL`

    UNION ALL
    SELECT processo_id, hisp_subsidios_id_da_operacao_mp
    FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING_FINAL`

    UNION ALL
    SELECT processo_id, hisp_subsidios_id_da_operacao_mp
    FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING_FINAL`
  )
  WHERE hisp_subsidios_id_da_operacao_mp IS NOT NULL
    AND hisp_subsidios_id_da_operacao_mp <> ''
),

-- ====================================================================================
-- Unificação das fontes com hierarquia explícita
-- PRIORIDADE_FONTE: 1 = OUTGOING | 2 = INCOMING | 3 = ONGOING
-- ====================================================================================
fontes_unificadas AS (
  SELECT *, 2 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING_FINAL`

  UNION ALL
  SELECT *, 2 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING_FINAL`

  UNION ALL
  SELECT *, 1 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING_FINAL`
  WHERE STATUS = 'Encerrado'

  UNION ALL
  SELECT *, 1 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING_FINAL`
  WHERE STATUS = 'Encerrado'

  UNION ALL
  SELECT *, 3 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_ONGOING_FINAL`

  UNION ALL
  SELECT *, 3 AS PRIORIDADE_FONTE
  FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_ONGOING_FINAL`
),

-- ====================================================================================
-- Criação de colunas derivadas
-- ====================================================================================
base_com_derivados AS (
  SELECT
    *,
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado, 1, 10)) AS DATA_REGISTRADO_TRATADA,
    UPPER(
      CASE
        WHEN PAIS = 'Brasil' THEN OBJETO
        WHEN PAIS <> 'Brasil'
          AND (OBJETO IS NULL OR OBJETO = '')
          AND CAUSAS_RAIZES <> '' THEN CAUSAS_RAIZES
        ELSE OBJETO
      END
    ) AS OBJETO_CROSS
  FROM fontes_unificadas
),

-- ====================================================================================
-- Deduplicação com hierarquia de fonte + data
-- ====================================================================================
DEDUP AS (
  SELECT
    base.* EXCEPT (RN, ID_DO_PAGAMENTO),
    COALESCE(base.ID_DO_PAGAMENTO, up.hisp_subsidios_id_da_operacao_mp) AS ID_DO_PAGAMENTO
  FROM (
    SELECT
      *,
      ROW_NUMBER() OVER (
        PARTITION BY PROCESSO_ID
        ORDER BY
          PRIORIDADE_FONTE ASC,
          DATA_REGISTRADO_TRATADA DESC
      ) AS RN
    FROM base_com_derivados
  ) base
  LEFT JOIN update_de_ids_pagamento up
    ON base.PROCESSO_ID = up.processo_id
  WHERE RN = 1
),

-- ====================================================================================
-- Enriquecimento final
-- ====================================================================================
FINAL_JOIN AS (
  SELECT
    d.*,
    m.MULTA_DATA,
    m.MULTA_TIPO_AJUSTADO,
    est.REGIAO,
    CASE
      WHEN NULLIF(TRIM(d.FASE_ESTADO), '') IS NOT NULL
       AND NULLIF(TRIM(d.FASE_ESTADO_4), '') IS NOT NULL
      THEN fas.TIPO
      ELSE 'NA'
    END AS FASE_DESFECHO,
    obj.OBJETO_NOVO AS OBJETO_TRATADO,
    obj.UNIDADE AS UNIDADE_TRATADA,
    obj.EMPRESA AS EMPRESA_TRATADA
  FROM DEDUP d
  LEFT JOIN MULTAS m
    ON d.PROCESSO_ID = m.PROCESSOID
  LEFT JOIN `<ENV>.STG.DIM_6_DIMENSAO_ESTADOS_UF` est
    ON d.PROCESSO_ESTADO = est.ESTADO
  LEFT JOIN `<ENV>.STG.DIM_14_DIMENSAO_FASES_REVISADA` fas
    ON UPPER(d.FASE_ESTADO) = UPPER(fas.FASE)
   AND UPPER(d.FASE_ESTADO_4) = UPPER(fas.ESTADO)
  LEFT JOIN `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS_2` obj
    ON d.OBJETO_CROSS = obj.OBJETO
)

-- ====================================================================================
-- Seleção final
-- ====================================================================================
SELECT
  f.*,
  CASE
    WHEN f.DATA_REGISTRADO_TRATADA IS NULL THEN 'INDEFINIDO'
    WHEN f.DATA_REGISTRADO_TRATADA < DATE '2024-01-01' THEN 'VELHO'
    ELSE 'NOVO'
  END AS MUNDO
FROM FINAL_JOIN f;
