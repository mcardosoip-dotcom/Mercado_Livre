-- =============================================================================
-- Query de teste: condições BOLBRADESCO na MOV (espelhando o 001)
-- Objetivo: listar em WHOWNER.BT_MP_ACC_MOVEMENTS os movimentos que
--           atendem às MESMAS condições que o 001 aplica para bolbradesco,
--           para checar se algo na origem pode impedir de aparecer no final.
-- Ajuste DATA_INI e DATA_FIM conforme o período que quiser testar.
-- =============================================================================

SELECT
  MOV.MOV_MOVE_ID,
  MOV.CUS_CUST_ID,
  MOV.MOV_CREATED_DT,
  MOV.MOV_DETAIL,
  MOV.MOV_TYPE_ID,
  MOV.PAY_PAYMENT_METHOD_ID,
  MOV.MOV_FINANCIAL_ENTITY_ID,
  MOV.MOV_LABEL,
  MOV.MOV_AMOUNT,
  MOV.PAY_PAYMENT_ID,
  MOV.MOV_REFERENCE_ID
FROM WHOWNER.BT_MP_ACC_MOVEMENTS MOV
WHERE
  -- Datas (espelha 001: MOV_CREATED_DT entre range; ajuste o range abaixo)
  CAST(MOV.MOV_CREATED_DT AS DATE) BETWEEN DATE('2020-01-01') AND DATE('2026-12-31')
  -- Mesmos filtros gerais do 001
  AND MOV.MOV_CURRENCY_ID = 'BRL'
  AND MOV.SIT_SITE_ID = 'MLB'
  AND (MOV.MOV_FINANCIAL_ENTITY_ID IS NULL OR MOV.MOV_FINANCIAL_ENTITY_ID <> 'coupon')
  AND (MOV.MOV_LABEL IS NULL OR MOV.MOV_LABEL NOT LIKE '%hidden%')
  -- Condições BOLBRADESCO (as duas combinações do 001, com PAY_PAYMENT_METHOD_ID = 'bolbradesco')
  AND LOWER(TRIM(CAST(MOV.PAY_PAYMENT_METHOD_ID AS STRING))) = 'bolbradesco'
  AND (
    (MOV.MOV_DETAIL = 'account_fund' AND MOV.MOV_TYPE_ID = 'fund')
    OR
    (MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'fee')
  )
ORDER BY MOV.MOV_CREATED_DT DESC, MOV.MOV_MOVE_ID;
