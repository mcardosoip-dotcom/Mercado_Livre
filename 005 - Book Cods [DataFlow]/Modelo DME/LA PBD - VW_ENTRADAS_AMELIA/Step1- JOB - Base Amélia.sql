TRUNCATE TABLE `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_AMELIA_SHARE`;

INSERT INTO
  `pdme000426-c1s7scatwm0-furyid.TBL.LK_PBD_LA_ELAW_REPORT_AMELIA_SHARE` (
    pais,
    processo_id,
    area_do_direito,
    sub_area_do_direito,
    processo_procedimento_judicial,
    processo_objeto_objeto,
    data_audiencia_inicial,
    advogado_da_parte_contraria,
    processo_cust_id_autor,
    parte_contraria_cpf_cnpj,
    -- REMOVIDO OU ADICIONAR AO SELECT
    numero_do_processo,
    processo_audiencia_ficticia,
    processo_invoca_hipervulnerabilidad,
    PROCESSO_O_USUARIO_RECLAMA_POR_DOIS_OU_MAIS_PRODUTOS_DIFERENTES,
    processo_o_documento_de_identidade_da_reclamacao_corresponde_ao_da_compra,
    processo_e_high_risk_confirmado_pelo_pf,
    processo_id_da_operacao_mp,
    processo_id_do_anuncio,
    parte_contraria_nome,
    status,
    valor_da_causa,
    data_registrado,
    processo_o_objeto_da_reclamacao_e_pdd_on_ou_pnr_on,
    processo_fase_estado_fase,
    processo_fase_estado_estado,
    caratula,
    escritorio_responsavel,
    processo_estado,
    processo_probabilidade_de_ganhar_ou_perder_probabilidade,
    -- Assumindo que T2.UF vai para esta coluna
    AUD_INS_DTTM,
    AUD_UPD_DTTM
  )
SELECT
  T1.PAIS,
  T1.PROCESSO_ID,
  T1.AREA_DO_DIREITO,
  T1.SUB_AREA_DO_DIREITO,
  T1.PROCESSO_PROCEDIMENTO_JUDICIAL,
  T1.PROCESSO_OBJETO_OBJETO,
  T1.DATA_AUDIENCIA_INICIAL,
  T1.ADVOGADO_DA_PARTE_CONTRARIA,
  T1.PROCESSO_CUST_ID_AUTOR,
  T1.PARTE_CONTRARIA_CPF_CNPJ,
  -- Adicione aqui se existir na T1 e quiser inserir
  T1.NUMERO_DO_PROCESSO,
  T1.PROCESSO_AUDIENCIA_FICTICIA,
  T1.PROCESSO_INVOCA_HIPERVULNERABILIDAD,
  T1.PROCESSO_O_USUARIO_RECLAMA_POR_DOIS_OU_MAIS_PRODUTOS_DIFERENTES,
  T1.PROCESSO_O_DOCUMENTO_DE_IDENTIDADE_DA_RECLAMACAO_CORRESPONDE_AO_DA_COMPRA,
  T1.PROCESSO_E_HIGH_RISK_CONFIRMADO_PELO_PF,
  T1.PROCESSO_ID_DA_OPERACAO_MP,
  T1.PROCESSO_ID_DO_ANUNCIO,
  T1.PARTE_CONTRARIA_NOME,
  T1.STATUS,
  T1.VALOR_DA_CAUSA,
  T1.DATA_REGISTRADO,
  T1.PROCESSO_O_OBJETO_DA_RECLAMACAO_E_PDD_ON_OU_PNR_ON,
  T1.PROCESSO_FASE_ESTADO_FASE,
  T1.PROCESSO_FASE_ESTADO_ESTADO,
  T2.CARATULA,
  T2.PAGE_REPORT_ESCRITORIORESPONSAVEL AS ESCRITORIO_RESPONSAVEL,
  T2.PROCESSO_ESTADO AS UF,
  T1.processo_probabilidade_de_ganhar_ou_perder_probabilidade,
  -- Mapeando para 'processo_estado' na tabela de destino
  T1.AUD_INS_DTTM,
  T1.AUD_UPD_DTTM
FROM
  `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_ELAW_REPORT_AMELIA` AS T1
  LEFT JOIN `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS` AS T2 ON T1.PROCESSO_ID = T2.PROCESSO_ID -- Corrigido para T2.PROCESSO_ID
WHERE
  T1.AREA_DO_DIREITO IN (
    "Consumidor",
    "Cível",
    "CORP - Civil",
    "CORP - Consumidor"
  )
  AND T1.processo_o_objeto_da_reclamacao_e_pdd_on_ou_pnr_on="Sim"