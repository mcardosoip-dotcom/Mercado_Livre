CREATE OR REPLACE TABLE `<ENV>.STG.ZTZ_coleta` AS
WITH
  cleaned_docs AS (
    SELECT
      documents,
      REGEXP_REPLACE(TRIM(documents), '[^0-9]', '') AS clean_doc_num,
      LENGTH(REGEXP_REPLACE(TRIM(documents), '[^0-9]', '')) AS doc_len
    FROM
      `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN`
  ),
  cleaned_customers AS (
    SELECT
      CUS_CUST_ID,
      CUS_CUST_DOC_NUMBER,
      CUS_NICKNAME,
      REGEXP_REPLACE(TRIM(CUS_CUST_DOC_NUMBER), '[^0-9]', '') AS clean_cust_doc_num,
      LENGTH(REGEXP_REPLACE(TRIM(CUS_CUST_DOC_NUMBER), '[^0-9]', '')) AS cust_doc_len
    FROM
      `meli-bi-data.WHOWNER.LK_CUS_CUSTOMERS_DATA`
    WHERE
      SIT_SITE_ID_CUS = 'MLA'
      AND CUS_CUST_STATUS = 'active'
      AND LENGTH(REGEXP_REPLACE(TRIM(CUS_CUST_DOC_NUMBER), '[^0-9]', '')) > 0
  )
SELECT
  doc.documents AS DADO_INPUT,
  c.CUS_CUST_DOC_NUMBER,
  c.CUS_NICKNAME,
  b.AVAILABLE_AMOUNT,
  a.ASSET_MGMT_STATUS,
  a.ASSET_MGMT_PRODUCT_ID,
  CASE
    WHEN c.CUS_CUST_DOC_NUMBER IS NULL THEN 'no existen users'
    WHEN IFNULL(CAST(b.AVAILABLE_AMOUNT AS STRING), 'Cuenta sin validación de identidade') = 'Cuenta sin validación de identidade' THEN 'Cuenta sin validación de identidade'
    WHEN UPPER(a.ASSET_MGMT_STATUS) = 'INVESTING' AND a.ASSET_MGMT_PRODUCT_ID = 'MLA_BIND_ARS' THEN 'Fondo Invertido - BIND'
    WHEN UPPER(a.ASSET_MGMT_STATUS) = 'INVESTING' AND (a.ASSET_MGMT_PRODUCT_ID = 'MLA_MELI_ARS_TRANS' OR a.ASSET_MGMT_PRODUCT_ID = 'MLA_MELI_ARS') THEN 'Fondo Invertido Próprio'
    ELSE 'Cuenta não remunerada'
  END AS TIPO_FONDO_INVERTIDO,
  IFNULL(CAST(b.AVAILABLE_AMOUNT AS STRING), 'Cuenta sin validación de identidade') AS AVAILABLE_AMOUNT_AJUSTADO
FROM
  cleaned_docs doc
LEFT JOIN
  cleaned_customers c
  ON
    (
      doc.doc_len = 11
      AND c.cust_doc_len = 11
      AND doc.clean_doc_num = c.clean_cust_doc_num
    )
    OR
    (
      doc.doc_len < 11
      AND doc.doc_len > 0 
      AND (
        (doc.doc_len = c.cust_doc_len AND doc.clean_doc_num = c.clean_cust_doc_num)
        OR
        (c.cust_doc_len = 11 AND doc.clean_doc_num = SUBSTR(c.clean_cust_doc_num, 3, 8))
      )
    )
LEFT JOIN
  (
    SELECT
      CUS_CUST_ID,
      AVAILABLE_AMOUNT
    FROM
      `meli-bi-data.WHOWNER.BT_MP_USER_BALANCE`
    WHERE
      CURRENCY_ID = 'ARS'
  ) b
  ON c.CUS_CUST_ID = b.CUS_CUST_ID
LEFT JOIN
  `meli-bi-data.WHOWNER.LK_MP_INVESTFW_ACCOUNTS` a
  ON c.CUS_CUST_ID = a.CUS_CUST_ID;