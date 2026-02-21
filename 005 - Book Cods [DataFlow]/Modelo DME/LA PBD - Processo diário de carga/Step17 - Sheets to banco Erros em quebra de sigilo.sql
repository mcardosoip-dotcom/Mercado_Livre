-- DEV
-- ddme000426-gopr4nla6zo-furyid

-- PROD
-- pdme000426-c1s7scatwm0-furyid

CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS` (
  tipo_erro STRING,
  origem STRING,
  dt_envio_bc STRING,
  dt_limite_resp STRING,
  dias_em_atraso STRING,
  num_ctrl_envio STRING,
  total STRING,
  ajuste STRING,
  atraso STRING,
  sla STRING,
  acao STRING,
  responsavel STRING,
  owner STRING,
  follow_up_status STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Follow_up(old)!A:O',
  uris = ['https://docs.google.com/spreadsheets/d/1Pui44iN8OQRPyG0P4OesIwlnUtOVRENFpY4p1BCZAtQ']
);

CREATE
OR REPLACE TABLE `<ENV>.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS_FATO` (
  tipo_erro STRING,
  origem STRING,
  dt_envio_bc STRING,
  dt_limite_resp STRING,
  dias_em_atraso STRING,
  num_ctrl_envio STRING,
  total STRING,
  ajuste STRING,
  atraso STRING,
  sla STRING,
  acao STRING,
  responsavel STRING,
  owner STRING,
  follow_up_status STRING
);

-- "Truncate"
DELETE FROM
  `<ENV>.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS_FATO`
WHERE
  TRUE;

-- Carga dos dados da externa para a fato
INSERT INTO
  `<ENV>.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS_FATO`
SELECT
  *
FROM
  `<ENV>.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS`;