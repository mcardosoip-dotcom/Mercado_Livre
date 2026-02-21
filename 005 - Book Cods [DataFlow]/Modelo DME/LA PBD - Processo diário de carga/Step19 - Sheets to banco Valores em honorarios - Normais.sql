------NORMAL---------------------------------------------
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_HONORARIOS_NORMAL` (
  Area STRING,
  SubArea STRING,
  Pais STRING,
  Procedimento STRING,
  Classificacao STRING,
  Tipo_desfecho STRING,
  Valor_honorario STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Database!A:G',
  uris = ['https://docs.google.com/spreadsheets/d/1bWNcn6RLAaFdSKcIo_YccUlTAReheyeDGysrAfR8q0g']
);

CREATE
OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_HONORARIOS_NORMAL_FATO` (
  Area STRING,
  SubArea STRING,
  Pais STRING,
  Procedimento STRING,
  Classificacao STRING,
  Tipo_desfecho STRING,
  Valor_honorario STRING
);

-- "Truncate"
DELETE FROM
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_NORMAL_FATO`
WHERE
  TRUE;

-- Carga dos dados da externa para a fato
INSERT INTO
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_NORMAL_FATO`
SELECT
  *
FROM
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_NORMAL`;

