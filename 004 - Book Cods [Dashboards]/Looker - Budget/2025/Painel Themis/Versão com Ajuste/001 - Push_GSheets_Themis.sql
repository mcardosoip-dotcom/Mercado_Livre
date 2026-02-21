CREATE
OR REPLACE EXTERNAL TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_THEMIS_2025` (
  owner STRING,
  created_by STRING,
  subsegment_name STRING,
  subsegment_code STRING,
  account_name STRING,
  supplier_name STRING,
  supplier_external_id STRING,
  business_unit STRING,
  subarea STRING,
  allocation STRING,
  society STRING,
  mur_refund STRING,
  is_it_a_new_service STRING,
  service STRING,
  grouper_name STRING,
  grouper_description STRING,
  category_name STRING,
  currency_name STRING,
  currency_symbol STRING,
  currency_code STRING,
  department_name STRING,
  department_external_id STRING,
  initiative_name STRING,
  initiative_external_code STRING,
  initiative_id STRING,
  year STRING,
  january_usd FLOAT64,
  february_usd FLOAT64,
  march_usd FLOAT64,
  april_usd FLOAT64,
  may_usd FLOAT64,
  june_usd FLOAT64,
  july_usd FLOAT64,
  august_usd FLOAT64,
  september_usd FLOAT64,
  october_usd FLOAT64,
  november_usd FLOAT64,
  december_usd FLOAT64,
  local_currency_name STRING,
  local_currency_symbol STRING,
  local_currency_code STRING,
  january_local FLOAT64,
  february_local FLOAT64,
  march_local FLOAT64,
  april_local FLOAT64,
  may_local FLOAT64,
  june_local FLOAT64,
  july_local FLOAT64,
  august_local FLOAT64,
  september_local FLOAT64,
  october_local FLOAT64,
  november_local FLOAT64,
  december_local FLOAT64,
  quantity STRING,
  unit_price_usd STRING,
  unit_price_local STRING,
  subtotal_usd STRING,
  hash_group STRING,
  base_price STRING,
  updated_at STRING,
  layer_from STRING,
  layer_to STRING,
  increase_type STRING,
  distributable STRING,
  comments STRING,
  bu_area STRING,
  agrupador_1 STRING,
  agrupador_2 STRING,
  subsegment_new STRING,
  vertical STRING,
  equipo STRING,
  supplier_unificado STRING,
  ytd STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Themis_2025!A:BU',
  uris = ['https://docs.google.com/spreadsheets/d/15DHeKGmkzHWyQqYcMrYcHtginknI9G5mn3Epn13OAvk']
);

CREATE
OR REPLACE TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_THEMIS_2025_FATO` (
  owner STRING,
  created_by STRING,
  subsegment_name STRING,
  subsegment_code STRING,
  account_name STRING,
  supplier_name STRING,
  supplier_external_id STRING,
  business_unit STRING,
  subarea STRING,
  allocation STRING,
  society STRING,
  mur_refund STRING,
  is_it_a_new_service STRING,
  service STRING,
  grouper_name STRING,
  grouper_description STRING,
  category_name STRING,
  currency_name STRING,
  currency_symbol STRING,
  currency_code STRING,
  department_name STRING,
  department_external_id STRING,
  initiative_name STRING,
  initiative_external_code STRING,
  initiative_id STRING,
  year STRING,
  january_usd FLOAT64,
  february_usd FLOAT64,
  march_usd FLOAT64,
  april_usd FLOAT64,
  may_usd FLOAT64,
  june_usd FLOAT64,
  july_usd FLOAT64,
  august_usd FLOAT64,
  september_usd FLOAT64,
  october_usd FLOAT64,
  november_usd FLOAT64,
  december_usd FLOAT64,
  local_currency_name STRING,
  local_currency_symbol STRING,
  local_currency_code STRING,
  january_local FLOAT64,
  february_local FLOAT64,
  march_local FLOAT64,
  april_local FLOAT64,
  may_local FLOAT64,
  june_local FLOAT64,
  july_local FLOAT64,
  august_local FLOAT64,
  september_local FLOAT64,
  october_local FLOAT64,
  november_local FLOAT64,
  december_local FLOAT64,
  quantity STRING,
  unit_price_usd STRING,
  unit_price_local STRING,
  subtotal_usd STRING,
  hash_group STRING,
  base_price STRING,
  updated_at STRING,
  layer_from STRING,
  layer_to STRING,
  increase_type STRING,
  distributable STRING,
  comments STRING,
  bu_area STRING,
  agrupador_1 STRING,
  agrupador_2 STRING,
  subsegment_new STRING,
  vertical STRING,
  equipo STRING,
  supplier_unificado STRING,
  ytd STRING
);

DELETE FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_THEMIS_2025_FATO`
WHERE
  TRUE;

INSERT INTO
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_THEMIS_2025_FATO`
SELECT
  *
FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_THEMIS_2025`;

--Criação de tabela dicionário
CREATE
OR REPLACE EXTERNAL TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO` (
  Area STRING,
  Sub_Area STRING,
  Business_Unit STRING,
  Direccion STRING,
  Owner STRING,
  Equipo STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Diccionario!A:F',
  uris = ['https://docs.google.com/spreadsheets/d/1-r2-qYifcntHzLeQaXVXYMnj0IBHJLrHkCdHpqA39yg']
);

CREATE
OR REPLACE TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_FATO` (
  Area STRING,
  Sub_Area STRING,
  Business_Unit STRING,
  Direccion STRING,
  Owner STRING,
  Equipo STRING
);

DELETE FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_FATO`
WHERE
  TRUE;

INSERT INTO
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_FATO`
SELECT
  *
FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO`;

--Criação de tabela dicionário de Vendor
CREATE
OR REPLACE EXTERNAL TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR` (
  Vendor_desc STRING,
  Vendor_desc_final STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Diccionario!M:N',
  uris = ['https://docs.google.com/spreadsheets/d/1-r2-qYifcntHzLeQaXVXYMnj0IBHJLrHkCdHpqA39yg']
);

CREATE
OR REPLACE TABLE `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR_FATO` (
  Vendor_desc STRING,
  Vendor_desc_final STRING
);

DELETE FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR_FATO`
WHERE
  TRUE;

INSERT INTO
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR_FATO`
SELECT
  *
FROM
  `ddme000426-gopr4nla6zo-furyid.STG.LK_PBD_LA_BUDGET_DICIONARIO_VENDOR`;