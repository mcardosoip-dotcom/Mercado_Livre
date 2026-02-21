-- ============================================================================
-- BLOCO 04: COLETA DE MOVIMENTAÇÕES FINANCEIRAS
-- ============================================================================
-- Descrição: Coleta todas as movimentações financeiras no período de investigação
--             Mapeia tipos de movimentação para códigos da Carta Circular 3454
-- Objetivo: Extrair transações financeiras com classificação adequada
-- Performance: JOIN otimizado com filtros de data e moeda
-- MELHORIA 2026: Usa DATA_ABERTURA como data inicial (evita movimentações antes da conta)
-- ============================================================================

-- COLETAR MOVIMENTAÇÕES FINANCEIRAS
-- Mapeia MOV_DETAIL e MOV_TYPE_ID para descrições e códigos da Carta Circular
CREATE OR REPLACE TABLE SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH AS (
SELECT
  DISTINCT
  TIT.CUS_CUST_ID,
  CAST(MOV.MOV_MOVE_ID AS STRING) AS CODIGO_CHAVE_EXTRATO,
  MOV.MOV_CREATED_DT AS DATA_LANCAMENTO,
  CAST(
    CASE 
      WHEN MOV.MOV_DETAIL = 'account_fund' AND MOV.MOV_TYPE_ID = 'fund' THEN 'Recebimento de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'cbk_recovery' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Estornos'
      WHEN MOV.MOV_DETAIL = 'cdb_investment' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Aplicação'
      WHEN MOV.MOV_DETAIL = 'cdb_rescue' AND MOV.MOV_TYPE_ID = 'income' THEN 'Resgate de Aplicação'
      WHEN MOV.MOV_DETAIL = 'credit' AND MOV.MOV_TYPE_ID = 'income' THEN 'Empréstimo/Financiamento'
      WHEN MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Aplicação'
      WHEN MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'income' THEN 'Resgate de Aplicação'
      WHEN MOV.MOV_DETAIL = 'debt_payment' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Pagamento Fornecedores'
      WHEN MOV.MOV_DETAIL = 'internal_transfer' AND MOV.MOV_TYPE_ID = 'income' THEN 'Transferência entre contas'
      WHEN MOV.MOV_DETAIL = 'investment_fund_suscribe' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Aplicação'
      WHEN MOV.MOV_DETAIL = 'mcoin_burn' AND MOV.MOV_TYPE_ID = 'income' THEN 'Resgate de Aplicação'
      WHEN MOV.MOV_DETAIL = 'merchant_credit' AND MOV.MOV_TYPE_ID = 'income' THEN 'Empréstimo/Financiamento'
      WHEN MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Envio de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'income' THEN 'Recebimento de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Pagamento de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'income' THEN 'Recebimento de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'payment_addition' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Pagamento de dinheiro entre contas Mercado Pago'
      WHEN MOV.MOV_DETAIL = 'payouts' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Transferência entre contas'
      WHEN MOV.MOV_DETAIL = 'payouts_cash' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Saque eletrônico'
      WHEN MOV.MOV_DETAIL = 'payouts_transfer' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Envio de dinheiro entre contas'
      WHEN MOV.MOV_DETAIL = 'prepaid_iof' AND MOV.MOV_TYPE_ID = 'expense' THEN 'IOF'
      WHEN MOV.MOV_DETAIL = 'special_fund' AND MOV.MOV_TYPE_ID = 'income' THEN 'Transferência entre contas'
      WHEN MOV.MOV_DETAIL = 'withdraw' AND MOV.MOV_TYPE_ID = 'expense' THEN 'Envio de TED/DOC interbancaria'
      ELSE 'Identificar'
    END AS STRING
  ) AS DESCRICAO_LANCAMENTO,
  CAST(
    CASE 
      WHEN MOV.MOV_DETAIL = 'account_fund' AND MOV.MOV_TYPE_ID = 'fund' THEN '217'
      WHEN MOV.MOV_DETAIL = 'cbk_recovery' AND MOV.MOV_TYPE_ID = 'expense' THEN '103'
      WHEN MOV.MOV_DETAIL = 'cdb_investment' AND MOV.MOV_TYPE_ID = 'expense' THEN '106'
      WHEN MOV.MOV_DETAIL = 'cdb_rescue' AND MOV.MOV_TYPE_ID = 'income' THEN '206'
      WHEN MOV.MOV_DETAIL = 'credit' AND MOV.MOV_TYPE_ID = 'income' THEN '207'
      WHEN MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'expense' THEN '106'
      WHEN MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'income' THEN '206'
      WHEN MOV.MOV_DETAIL = 'debt_payment' AND MOV.MOV_TYPE_ID = 'expense' THEN '112'
      WHEN MOV.MOV_DETAIL = 'internal_transfer' AND MOV.MOV_TYPE_ID = 'income' THEN '213'
      WHEN MOV.MOV_DETAIL = 'investment_fund_suscribe' AND MOV.MOV_TYPE_ID = 'expense' THEN '106'
      WHEN MOV.MOV_DETAIL = 'mcoin_burn' AND MOV.MOV_TYPE_ID = 'income' THEN '206'
      WHEN MOV.MOV_DETAIL = 'merchant_credit' AND MOV.MOV_TYPE_ID = 'income' THEN '207'
      WHEN MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'expense' THEN '117'
      WHEN MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'income' THEN '213'
      WHEN MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'expense' THEN '117'
      WHEN MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'income' THEN '218'
      WHEN MOV.MOV_DETAIL = 'payment_addition' AND MOV.MOV_TYPE_ID = 'expense' THEN '117'
      WHEN MOV.MOV_DETAIL = 'payouts' AND MOV.MOV_TYPE_ID = 'expense' THEN '117'
      WHEN MOV.MOV_DETAIL = 'payouts_cash' AND MOV.MOV_TYPE_ID = 'expense' THEN '114'
      WHEN MOV.MOV_DETAIL = 'payouts_transfer' AND MOV.MOV_TYPE_ID = 'expense' THEN '120'
      WHEN MOV.MOV_DETAIL = 'prepaid_iof' AND MOV.MOV_TYPE_ID = 'expense' THEN '110'
      WHEN MOV.MOV_DETAIL = 'special_fund' AND MOV.MOV_TYPE_ID = 'income' THEN '213'
      WHEN MOV.MOV_DETAIL = 'withdraw' AND MOV.MOV_TYPE_ID = 'expense' THEN '120'
      ELSE 'Identificar'
    END AS STRING
  ) AS TIPO_LANCAMENTO,
  CAST((ABS(MOV.MOV_AMOUNT) * 100) AS STRING) AS VALOR_LANCAMENTO,
  CAST(
    CASE  
      WHEN MOV.MOV_TYPE_ID = 'expense' THEN 'D'
      WHEN MOV.MOV_TYPE_ID = 'income' OR MOV.MOV_TYPE_ID = 'fund' THEN 'C'
    END AS STRING
  ) AS NATUREZA_LANCAMENTO,
  CAST(
    CASE  
      WHEN MOV.MOV_TYPE_ID = 'expense' THEN 'D'
      WHEN MOV.MOV_TYPE_ID = 'income' OR MOV.MOV_TYPE_ID = 'fund' THEN 'C'
    END AS STRING
  ) AS NATUREZA_SALDO,
  CASE 
    WHEN MOV.CUS_CUST_ID = MOV.CUS_CUST_ID_SEL THEN MOV.CUS_CUST_ID_BUY
    WHEN MOV.CUS_CUST_ID = MOV.CUS_CUST_ID_BUY THEN MOV.CUS_CUST_ID_SEL
    ELSE NULL 
  END AS ID_RELACIONADO,
  CASE 
    WHEN MOV.MOV_DETAIL LIKE '%payouts%' THEN MOV.MOV_REFERENCE_ID 
    WHEN MOV.WIT_WITHDRAW_ID IS NOT NULL THEN MOV.WIT_WITHDRAW_ID
    WHEN MOV.PAY_PAYMENT_ID IS NOT NULL THEN MOV.PAY_PAYMENT_ID
    ELSE MOV.MOV_REFERENCE_ID 
  END AS ID_PAGAMENTO,
  CASE 
    WHEN MOV.MOV_DETAIL LIKE '%payouts%' THEN 'Payout' 
    WHEN MOV.WIT_WITHDRAW_ID IS NOT NULL THEN 'Withdrawal'
    WHEN MOV.PAY_PAYMENT_METHOD_ID = 'pix' THEN 'Pix'
    WHEN MOV.PAY_PAYMENT_ID IS NOT NULL THEN 'Payments'
    ELSE 'Identificar'
  END AS TBL_RELACIONADO,
  MOV.MOV_DETAIL,
  MOV.MOV_TYPE_ID,
  MOV.MOV_LABEL
FROM SBOX_LEGALES.STG_QS_TITULAR_CAD_VF_FINCH TIT
LEFT JOIN WHOWNER.BT_MP_ACC_MOVEMENTS MOV
  ON TIT.CUS_CUST_ID = MOV.CUS_CUST_ID
  -- MELHORIA 2026: Usa DATA_ABERTURA (AVK_CREATED) como data inicial
  -- Evita buscar movimentações antes da criação da conta
  AND MOV.MOV_CREATED_DT BETWEEN TIT.MOVIMENTACAO_MIN AND TIT.RANGE_MAX
  AND MOV.MOV_CURRENCY_ID = 'BRL'
  AND MOV.SIT_SITE_ID = 'MLB'
  AND MOV.MOV_FINANCIAL_ENTITY_ID <> 'coupon'
  AND MOV.MOV_LABEL NOT LIKE '%hidden%'
  AND (
    (MOV.MOV_DETAIL = 'account_fund' AND MOV.MOV_TYPE_ID = 'fund') OR
    (MOV.MOV_DETAIL = 'cbk_recovery' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'cdb_investment' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'cdb_rescue' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'credit' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'crypto_operation' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'debt_payment' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'internal_transfer' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'investment_fund_suscribe' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'mcoin_burn' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'merchant_credit' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'money_transfer' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'payment_addition' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'payouts' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'payouts_cash' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'payouts_transfer' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'prepaid_iof' AND MOV.MOV_TYPE_ID = 'expense') OR
    (MOV.MOV_DETAIL = 'special_fund' AND MOV.MOV_TYPE_ID = 'income') OR
    (MOV.MOV_DETAIL = 'withdraw' AND MOV.MOV_TYPE_ID = 'expense')
  )
WHERE 
  -- MELHORIA 2026: Filtro adicional para garantir período correto
  MOV.MOV_CREATED_DT BETWEEN TIT.MOVIMENTACAO_MIN AND TIT.RANGE_MAX
  AND MOV.SIT_SITE_ID = 'MLB'
  AND MOV.MOV_FINANCIAL_ENTITY_ID <> 'coupon'
  AND MOV.MOV_CURRENCY_ID = 'BRL'
  AND MOV.MOV_LABEL NOT LIKE '%hidden%'
);

-- FILTRAR MOVIMENTAÇÕES SEM CANCELAMENTO
-- Remove movimentações que foram canceladas (exceto cancelamentos parciais)
CREATE OR REPLACE TABLE SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH AS (
SELECT
  *
FROM (
  SELECT 
    CASE 
      WHEN B.ID_PAGAMENTO IS NOT NULL AND C.QTD > 1 THEN 'sim'
      ELSE 'não'
    END AS EXCLUIR,
    A.*
  FROM SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH A 
  LEFT JOIN (
    SELECT DISTINCT ID_PAGAMENTO
    FROM SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH
    WHERE (MOV_LABEL LIKE '%cancellation%' OR MOV_LABEL LIKE '%cancelled %')
      AND MOV_LABEL NOT LIKE '%partial%'
      AND DATA_LANCAMENTO <> '1900-01-01'
  ) B
    ON A.ID_PAGAMENTO = B.ID_PAGAMENTO
  LEFT JOIN (
    SELECT DISTINCT ID_PAGAMENTO, COUNT(ID_PAGAMENTO) AS QTD
    FROM SBOX_LEGALES.STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH
    GROUP BY 1
  ) C
    ON A.ID_PAGAMENTO = C.ID_PAGAMENTO
)
WHERE EXCLUIR = 'não'
);
