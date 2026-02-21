-- DEV 
-- ddme000426-gopr4nla6zo-furyid

-- PROD
-- pdme000426-c1s7scatwm0-furyid


-- Tabela externa para ENLIGHTEN
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN` (
  Data STRING,
  Entradas STRING,
  Descartados STRING,
  Tratados STRING,
  Backlog STRING,
  Provedor STRING,
  Modalidade STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'ENLIGHTEN!A:G',
  uris = ['https://docs.google.com/spreadsheets/d/1LfV7vajl9KHt39eDCqK5-e0xdTyXGNt2AmZ2YhiNQao']
);

-- Tabela de fato (normal, gerenciada)
CREATE
OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN_FATO` (
  Data STRING,
  Entradas STRING,
  Descartados STRING,
  Tratados STRING,
  Backlog STRING,
  Provedor STRING,
  Modalidade STRING
);

-- "Truncate"
DELETE FROM
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN_FATO`
WHERE
  TRUE;

-- Carga dos dados da externa para a fato
INSERT INTO
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN_FATO`
SELECT
  *
FROM
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN`;

-- Tabela externa para FINCH
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH` (
  Data STRING,
  Entradas STRING,
  Descartados STRING,
  Tratados STRING,
  Backlog STRING,
  Provedor STRING,
  Modalidade STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'FINCH!A:G',
  uris = ['https://docs.google.com/spreadsheets/d/1LfV7vajl9KHt39eDCqK5-e0xdTyXGNt2AmZ2YhiNQao']
);

-- Tabela de fato FINCH (normal, gerenciada)
CREATE
OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH_FATO` (
  Data STRING,
  Entradas STRING,
  Descartados STRING,
  Tratados STRING,
  Backlog STRING,
  Provedor STRING,
  Modalidade STRING
);

-- "Truncate"
DELETE FROM
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH_FATO`
WHERE
  TRUE;

-- Carga dos dados da externa para a fato
INSERT INTO
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH_FATO`
SELECT
  *
FROM
  `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_FINCH`;