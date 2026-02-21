-- Fontes: STG.Database_Honorarios_Brasil | STG.Database_Honorarios_Hispanos
-- Consolidação: campos unificados como processo_id e valor_honorario

SELECT
  CAST(id AS STRING) AS processo_id,
  honorarios_total AS valor_honorario,
  CAST(escritorio_responsavel AS STRING) AS escritorio_responsavel
FROM `pdme000426-c1s7scatwm0-furyid.STG.Database_Honorarios_Brasil`

UNION ALL

SELECT
  CAST(processo_id AS STRING) AS processo_id,
  monto AS valor_honorario,
  CAST(escritorio_externo AS STRING) AS escritorio_responsavel
FROM `pdme000426-c1s7scatwm0-furyid.STG.Database_Honorarios_Hispanos`

