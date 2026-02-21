CREATE OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BASE_BASE_ATIVA` AS

-- ====================================================================================
-- QUERY AJUSTADA E OTIMIZADA:
-- - Endereço <ENV> usado como variável de ambiente.
-- - AGING AGORA CALCULADO COM BASE NA DATA ATUAL EM ANOS INTEIROS.
-- - Unifica as fontes de dados do Brasil e Hispanos.
-- - Lógica centralizada para evitar reprocessamento de colunas (datas e OBJETO_CROSS).
-- ====================================================================================

WITH 
  MULTAS AS (
    SELECT
      PROCESSO_ID AS PROCESSOID,
      DATA        AS MULTA_DATA,
      CASE
        WHEN REGEXP_CONTAINS(dm.TIPO_AJUSTADO, r'(?i)\bmulta\b') THEN 'Multa'
        ELSE 'Outros'
      END         AS MULTA_TIPO_AJUSTADO
    FROM `<ENV>.TBL.LK_PBD_LA_ELAW_REPORT_EXTRACAO_MULTAS` AS em
    LEFT JOIN `<ENV>.STG.DIM_16_DIMENSAO_MULTA` AS dm
      ON em.TIPO = dm.TIPO
  ),

  -- Passo 1: Unificar as duas fontes de dados de incoming.
  fontes_unificadas AS (
    SELECT * FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_ONGOING_FINAL`
    UNION ALL
    SELECT * FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_ONGOING_FINAL`
  ),

  -- Passo 2: Ler a fonte unificada e criar todas as colunas derivadas de uma só vez.
  base_com_derivados AS (
    SELECT
      *,
      -- Colunas de data tratadas, para serem usadas em toda a query
      SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado, 1, 10)) AS DATA_REGISTRADO_TRATADA,
      SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(DATA_DE_ENCERRAMENTO, 1, 10)) AS DATA_ENCERRAMENTO_TRATADA,
      
      -- Coluna OBJETO_CROSS, para ser usada nos JOINs e na seleção final
      UPPER(
        CASE
          WHEN PAIS = 'Brasil' THEN OBJETO
          WHEN PAIS <> 'Brasil' AND (OBJETO = '' OR OBJETO IS NULL) AND CAUSAS_RAIZES <> '' THEN CAUSAS_RAIZES
          ELSE OBJETO
        END
      ) AS OBJETO_CROSS
    FROM fontes_unificadas
  ),

  -- Passo 3: Enriquecer a base com dados de multas e região.
  INCOMING AS (
    SELECT
      base.*,
      m.MULTA_DATA,
      m.MULTA_TIPO_AJUSTADO,
      est.REGIAO
    FROM base_com_derivados AS base
    LEFT JOIN MULTAS AS m
      ON base.PROCESSO_ID = m.PROCESSOID
    LEFT JOIN `<ENV>.STG.DIM_6_DIMENSAO_ESTADOS_UF` AS est
      ON base.PROCESSO_ESTADO = est.ESTADO
  ),

  -- Passo 4: Desduplicar registros com base no processo e na data mais recente.
  DEDUP AS (
    SELECT * EXCEPT(RN)
    FROM (
      SELECT
        inc.*,
        ROW_NUMBER() OVER (
          PARTITION BY PROCESSO_ID
          ORDER BY DATA_REGISTRADO_TRATADA DESC
        ) AS RN
      FROM INCOMING inc
    )
    WHERE RN = 1
  ),

  WITH_FASES AS (
    SELECT
      d.*,
      CASE 
        WHEN NULLIF(TRIM(d.FASE_ESTADO), '') IS NOT NULL AND NULLIF(TRIM(d.FASE_ESTADO_4), '') IS NOT NULL THEN fas.TIPO
        ELSE 'NA'
      END AS FASE_DESFECHO
    FROM DEDUP d
    LEFT JOIN `<ENV>.STG.DIM_14_DIMENSAO_FASES_REVISADA` AS fas
      ON UPPER(d.FASE_ESTADO) = UPPER(fas.FASE)
      AND UPPER(d.FASE_ESTADO_4) = UPPER(fas.ESTADO)
  ),

  WITH_OBJETOS AS (
    SELECT
      wf.*,
      obj.OBJETO_NOVO AS OBJETO_TRATADO,
      obj.UNIDADE     AS UNIDADE_TRATADA,
      obj.EMPRESA     AS EMPRESA_TRATADA
    FROM WITH_FASES wf
    LEFT JOIN `<ENV>.STG.DIM_10_DIMENSAO_OBJETOS_2` AS obj
      -- Reutilizando a coluna OBJETO_CROSS criada no primeiro passo
      ON wf.OBJETO_CROSS = obj.OBJETO
  ),

  FINAL AS (
    SELECT
      wo.*,
      -- MUNDO: Usando a coluna de data já tratada
      CASE
        WHEN wo.DATA_REGISTRADO_TRATADA IS NULL THEN 'INDEFINIDO'
        WHEN wo.DATA_REGISTRADO_TRATADA < DATE '2024-01-01' THEN 'VELHO'
        ELSE 'NOVO'
      END AS MUNDO,

      -- Condicionais financeiras
      CASE WHEN SAFE_CAST(wo.VALOR_DA_CAUSA AS FLOAT64) >= 200000 THEN 'Sim' ELSE 'Não' END AS CAUSA_MAIOR_200K,
      CASE WHEN SAFE_CAST(wo.VALOR_DO_RISCO AS FLOAT64) >= 200000 THEN 'Sim' ELSE 'Não' END AS RISCO_MAIOR_200K,
      CASE WHEN SAFE_CAST(wo.VALOR_DO_RISCO AS FLOAT64) BETWEEN 100000 AND 199999.99 THEN 'Sim' ELSE 'Não' END AS RISCO_ENTRE_100K_E_200K,
      CASE WHEN SAFE_CAST(wo.VALOR_DA_CAUSA AS FLOAT64) BETWEEN 100000 AND 199999.99 THEN 'Sim' ELSE 'Não' END AS CAUSA_ENTRE_100K_E_200K,

      -- AGING: Usando a DATA ATUAL para um cálculo em ANOS inteiros
      DATE_DIFF(CURRENT_DATE(), wo.DATA_REGISTRADO_TRATADA, YEAR) AS AGING

    FROM WITH_OBJETOS wo
  )

-- NOTA DE PERFORMANCE: A CTE 'DEDUP' deve garantir a unicidade por PROCESSO_ID.
SELECT DISTINCT *
FROM FINAL;