-- =============================================================================
-- Validação: hipótese bolbradesco = account_fund + fund
-- Origem: WHOWNER.BT_MP_ACC_MOVEMENTS
-- Objetivo: listar na origem os casos MOV_DETAIL='account_fund', MOV_TYPE_ID='fund',
--           MOV_FINANCIAL_ENTITY_ID='bolbradesco' e verificar se entraram na staging
-- =============================================================================

WITH params AS (
  SELECT
    DATE('2020-01-01') AS DATA_INI,   -- altere para o range da sua carga (ex: 2021 para os IDs da base de erros)
    DATE('2026-12-31') AS DATA_FIM
),

-- 1) Casos na ORIGEM: account_fund + fund + bolbradesco
origem_bolbradesco_account_fund AS (
  SELECT
    MOV.MOV_MOVE_ID,
    MOV.CUS_CUST_ID,
    MOV.MOV_CREATED_DT,
    MOV.MOV_DETAIL,
    MOV.MOV_TYPE_ID,
    MOV.MOV_FINANCIAL_ENTITY_ID,
    MOV.MOV_LABEL,
    MOV.MOV_AMOUNT,
    MOV.PAY_PAYMENT_ID,
    MOV.MOV_REFERENCE_ID
  FROM WHOWNER.BT_MP_ACC_MOVEMENTS MOV
  CROSS JOIN params P
  WHERE MOV.MOV_DETAIL = 'account_fund'
    AND MOV.MOV_TYPE_ID = 'fund'
    AND LOWER(TRIM(CAST(MOV.MOV_FINANCIAL_ENTITY_ID AS STRING))) = 'bolbradesco'
    AND MOV.MOV_CURRENCY_ID = 'BRL'
    AND MOV.SIT_SITE_ID = 'MLB'
    AND (MOV.MOV_LABEL IS NULL OR MOV.MOV_LABEL NOT LIKE '%hidden%')
    AND (MOV.MOV_FINANCIAL_ENTITY_ID IS NULL OR MOV.MOV_FINANCIAL_ENTITY_ID <> 'coupon')
    AND CAST(MOV.MOV_CREATED_DT AS DATE) BETWEEN P.DATA_INI AND P.DATA_FIM
),

-- 2) Titulares no escopo da execução
titulares AS (
  SELECT
    TIT.CUS_CUST_ID,
    TIT.IDENTIFICACAO,
    TIT.DOC_NUMBER,
    TIT.MOVIMENTACAO_MIN,
    TIT.RANGE_MAX
  FROM SBOX_LEGALES.STG_QS_TITULAR_CAD_VF_FINCH TIT
),

-- 3) Casos da origem no range do titular (deveriam entrar na staging)
origem_no_escopo AS (
  SELECT
    O.*,
    TIT.IDENTIFICACAO,
    TIT.DOC_NUMBER,
    CASE
      WHEN O.MOV_CREATED_DT BETWEEN TIT.MOVIMENTACAO_MIN AND TIT.RANGE_MAX THEN 1
      ELSE 0
    END AS dentro_range_titular
  FROM origem_bolbradesco_account_fund O
  INNER JOIN titulares TIT
    ON TIT.CUS_CUST_ID = O.CUS_CUST_ID
),

-- 4) Staging: o que entrou em STG_QS_AUX_MOVIMENTACAO (account_fund + fund)
staging AS (
  SELECT
    CAST(CODIGO_CHAVE_EXTRATO AS STRING) AS CODIGO_CHAVE_EXTRATO,
    CUS_CUST_ID,
    DATA_LANCAMENTO,
    MOV_DETAIL,
    MOV_TYPE_ID,
    DESCRICAO_LANCAMENTO,
    ID_PAGAMENTO
  FROM SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH
  WHERE MOV_DETAIL = 'account_fund'
    AND MOV_TYPE_ID = 'fund'
),

-- 5) Staging2: o que passou da etapa de cancelamento (EXCLUIR = não)
staging2 AS (
  SELECT
    CAST(CODIGO_CHAVE_EXTRATO AS STRING) AS CODIGO_CHAVE_EXTRATO,
    CUS_CUST_ID,
    EXCLUIR
  FROM SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH
  WHERE MOV_DETAIL = 'account_fund'
    AND MOV_TYPE_ID = 'fund'
)

-- Resultado: origem vs staging vs staging2
SELECT
  O.MOV_MOVE_ID,
  O.CUS_CUST_ID,
  O.IDENTIFICACAO,
  O.DOC_NUMBER,
  O.MOV_CREATED_DT,
  O.MOV_AMOUNT,
  O.PAY_PAYMENT_ID,
  O.dentro_range_titular,
  CASE WHEN S.CODIGO_CHAVE_EXTRATO IS NOT NULL THEN 1 ELSE 0 END AS ENTRARAM_NA_STAGING,
  S.DESCRICAO_LANCAMENTO,
  CASE WHEN S2.CODIGO_CHAVE_EXTRATO IS NOT NULL THEN 1 ELSE 0 END AS ENTRARAM_NA_STAGING2,
  S2.EXCLUIR AS EXCLUIR_STAGING2
FROM origem_no_escopo O
LEFT JOIN staging S
  ON S.CODIGO_CHAVE_EXTRATO = CAST(O.MOV_MOVE_ID AS STRING)
  AND S.CUS_CUST_ID = O.CUS_CUST_ID
LEFT JOIN staging2 S2
  ON S2.CODIGO_CHAVE_EXTRATO = CAST(O.MOV_MOVE_ID AS STRING)
  AND S2.CUS_CUST_ID = O.CUS_CUST_ID
WHERE O.dentro_range_titular = 1
ORDER BY O.MOV_CREATED_DT DESC, O.MOV_MOVE_ID;
