-- ============================================================================
-- BLOCO 01: PREPARAÇÃO DA BASE DE INVESTIGADOS
-- ============================================================================
-- Descrição: Prepara a base de investigados a partir da tabela de entrada
--             Identifica tipo de solicitação (Carta Circular 3454 ou Extrato)
-- Objetivo: Normalizar dados de entrada e criar flags de processamento
-- Performance: Operação leve, apenas agregação e CASE
-- ============================================================================

-- PREPARAR BASE PRESENTA
-- Identifica o tipo de solicitação através das hashtags
-- Agrega períodos (MIN/MAX) para cada investigado
CREATE OR REPLACE TABLE SBOX_LEGALES.STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH AS (
SELECT 
  CASE
    WHEN CCS_Hashtags LIKE '%#extratoMovimentacaoCartaCircular3454%' THEN 'Sim'
    ELSE 'Nao'
  END AS CIRCULAR_3454,
  CASE
    WHEN CCS_Hashtags LIKE '%#extratoAplicacoesFinanceiras%' 
         OR CCS_Hashtags LIKE '%#extratoMercantil%' THEN 'Sim'
    ELSE 'Nao'
  END AS EXTRATO,
  CAST(MIN(APOIO_RANGE_MIN) AS DATE) AS RANGE_MIN,
  CAST(MAX(APOIO_RANGE_MAX) AS DATE) AS RANGE_MAX,
  APOIO_CPF_CNPJ AS DOC_NUMBER,
  CASO AS IDENTIFICACAO,
  '1' AS FLAG_INVESTIGADO,
  SISTEMA,
  CURRENT_DATETIME AS DATAHORA_IMPORTACAO
FROM SBOX_LEGALES.TBL_QS_AUX_INVESTIGADO_FINCH
WHERE APOIO_CPF_CNPJ IS NOT NULL
GROUP BY 1, 2, 5, 6, 7, 8
);
