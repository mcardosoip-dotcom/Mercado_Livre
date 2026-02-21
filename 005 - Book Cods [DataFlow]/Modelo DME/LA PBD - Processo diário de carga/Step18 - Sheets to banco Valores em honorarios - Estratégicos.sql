------ESTRATÉGICO---------------------------------------------
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_HONORARIOS_ESTRATEGICO` (
  Area STRING,
  SubArea STRING,
  Pais STRING,
  Procedimento STRING,
  Classificacao STRING,
  Tipo_desfecho STRING,
  faixa STRING,
  Valor_honorario STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Database!A:H',
  uris = ['https://docs.google.com/spreadsheets/d/19TbOTqRSgqeeg2RcJ26UspHLSffyHukthy1GQyu7GCk']
);

CREATE
OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_HONORARIOS_ESTRATEGICO_FATO` (
  Area STRING,
  SubArea STRING,
  Pais STRING,
  Procedimento STRING,
  Classificacao STRING,
  Tipo_desfecho STRING,
  faixa STRING,
  Valor_honorario STRING
);

-- "Truncate"
DELETE FROM
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_ESTRATEGICO_FATO`
WHERE
  TRUE;

-- Carga dos dados da externa para a fato
INSERT INTO
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_ESTRATEGICO_FATO`
SELECT
  *
FROM
  `<ENV>.STG.LK_PBD_LA_HONORARIOS_ESTRATEGICO`;