-- DEV
-- ddme000426-gopr4nla6zo-furyid

-- PROD
-- pdme000426-c1s7scatwm0-furyid

-- ============================================
-- LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE
-- ============================================
TRUNCATE TABLE `<ENV>.TBL.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE`;

INSERT INTO `<ENV>.TBL.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE` (
  data_envio_sisbacen,
  data_recebimento_inst,
  origem,
  tipo_de_oficio,
  no_protocolo,
  no_processo,
  instituicao,
  nome_do_solicitante,
  nome_da_vara_juizo,
  tribunal,
  cpf_cnpj,
  pessoa,
  ccs_numero_do_caso,
  ccs_inicio_do_periodo_solicitado,
  ccs_fim_do_periodo_solicitado,
  ccs_prazo_limite_de_resposta,
  ccs_hashtags,
  ccs_sistema_de_entrega,
  AUD_INS_DTTM,
  AUD_UPD_DTTM
)
SELECT
  CAST(data_envio_sisbacen AS STRING),
  CAST(data_recebimento_inst AS STRING),
  CAST(origem AS STRING),
  CAST(tipo_de_oficio AS STRING),
  CAST(no_protocolo AS STRING),
  CAST(no_processo AS STRING),
  CAST(instituicao AS STRING),
  CAST(nome_do_solicitante AS STRING),
  CAST(nome_da_vara_juizo AS STRING),
  CAST(tribunal AS STRING),
  CAST(cpf_cnpj AS STRING),
  CAST(pessoa AS STRING),
  CAST(ccs_numero_do_caso AS STRING),
  CAST(ccs_inicio_do_periodo_solicitado AS STRING),
  CAST(ccs_fim_do_periodo_solicitado AS STRING),
  CAST(ccs_prazo_limite_de_resposta AS STRING),
  CAST(ccs_hashtags AS STRING),
  CAST(ccs_sistema_de_entrega AS STRING),
  CURRENT_DATETIME(),
  CURRENT_DATETIME()
FROM
  `<ENV>.STG.QUEBRA_DE_SIGILO_CONTROLE`;
