SELECT
  processo_id,
  -- processo_cpf,
  processo_id_da_venda,
  processo_chave_pix,
  id,
  processo_qual_a_solicitacao_da_obf AS processo_qual_a_solicitacao_da_obf,
  processo_cust_id_autor AS processo_cust_id_autor,
  -- processo_e_mail_do_usuario AS processo_e_mail_do_usuario,
  processo_adicionar_periodo_de_referencia AS processo_adicionar_periodo_de_referencia,
  processo_adicionar_periodo_de_referencia_grupo AS processo_adicionar_periodo_de_referencia_grupo,
  processo_tem_multa_fixada AS processo_tem_multa_fixada,
  processo_tem_multa_fixada_grupo AS processo_tem_multa_fixada_grupo,
  processo_tipo_de_decisao AS processo_tipo_de_decisao,
  processo_tipo_de_decisao_grupo AS processo_tipo_de_decisao_grupo,
  processo_id_da_operacao_mp AS processo_id_da_operacao_mp,
  processo_id_do_anuncio AS processo_id_do_anuncio,
  area_do_direito AS area_do_direito,
  sub_area_do_direito AS sub_area_do_direito,
  fase_de_workflow AS fase_de_workflow,
  workflow AS workflow,
  objeto AS objeto,
  -- descricao_evento_concluido AS descricao_evento_concluido,
  -- parse de datas sem hora (dd/mm/yyyy)
  SAFE.PARSE_DATE(
    '%d/%m/%Y',
    SUBSTR(processo_prazo_para_cumprimento, 1, 10)
  ) AS processo_prazo_para_cumprimento,
  SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado, 1, 10)) AS data_registrado,
  SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_de_confirmacao, 1, 10)) AS data_de_confirmacao,
  -- diferenças em dias
  DATE_DIFF(
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_de_confirmacao, 1, 10)),
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado, 1, 10)),
    DAY
  ) AS TME,
  DATE_DIFF(
    CURRENT_DATE(),
    SAFE.PARSE_DATE('%d/%m/%Y', SUBSTR(data_registrado, 1, 10)),
    DAY
  ) AS tempo_desde_o_registro
FROM
  `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_OBRIGACOES_DE_FAZER`