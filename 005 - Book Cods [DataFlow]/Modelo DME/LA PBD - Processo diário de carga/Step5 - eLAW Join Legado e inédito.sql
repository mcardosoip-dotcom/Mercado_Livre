--- ============================================================
-- LOG DE ALTERAÇÕES:
--      DATA: 2025-11-21
--      AUTOR: Murillo França
--      ALTERAÇÃO: Adição da coluna DATA_REGISTRADO_1 nas inserções das tabelas de tarefas agendamentos.
--      DATA: 2026-02-12
--      ALTERAÇÃO: Corte dinâmico legado/inédito.
--                Legado = sempre o passado: data < 1º dia do mês atual (DATE_TRUNC(CURRENT_DATE(), MONTH)).
--                Inédito = sempre apenas o último mês (mês atual): data >= 1º dia mês atual E data < 1º dia mês seguinte.
--                Assim o filtro de corte fica dinâmico sem data fixa.
--      ALTERAÇÃO: SELECT DISTINCT na junção legado + inédito em todas as tabelas *_FINAL que unem as duas bases,
--                para evitar duplicidade (dentro do legado, dentro do inédito ou entre as duas fontes).
--      ALTERAÇÃO: TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES_legado tem schema distinto: usa coluna data_registrado_1
--                (não data_da_tarefa); CTE legado usa t1.data_registrado_1 no filtro e nas expressões.
--      ALTERAÇÃO: ACOMPANHAMENTO_DE_TAREFAS_CORP_CX_legado não tem data_registrado; no CTE legado usar t1.data_da_tarefa
--                para a coluna de saída data_registrado (compatibilidade de schema no UNION).
--- ============================================================




CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_ACOMPANHAMENTO_DE_TAREFAS_CORP_CX_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            PARSE_DATE('%d/%m/%Y', t1.data_da_tarefa) AS STRING
        ) AS data_da_tarefa,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.data_da_tarefa AS STRING) AS data_registrado,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_ACOMPANHAMENTO_DE_TAREFAS_CORP_CX_legado` t1
    WHERE
        PARSE_DATE('%d/%m/%Y', t1.data_da_tarefa) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            PARSE_DATE('%d/%m/%Y', t2.data_da_tarefa) AS STRING
        ) AS data_da_tarefa,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_ACOMPANHAMENTO_DE_TAREFAS_CORP_CX` t2
    WHERE
        PARSE_DATE('%d/%m/%Y', t2.data_da_tarefa) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND PARSE_DATE('%d/%m/%Y', t2.data_da_tarefa) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_DR_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_DR_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_DR` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_da_tarefa AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
-- Tabela comentada: não criar no momento (schema legado AGUARDANDO_INFORMACOES a alinhar).
/*
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual). Legado usa data_registrado_1 (não data_da_tarefa).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado_1 AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.empresa AS STRING) AS empresa,
        CAST(t1.data_registrado_1 AS STRING) AS data_da_tarefa,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.comarca AS STRING) AS comarca,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.data AS STRING) AS data,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.tipo AS STRING) AS tipo,
        CAST(t1.sub_tipo AS STRING) AS sub_tipo,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t1.data_registrado_1 AS STRING) AS data_registrado,
        CAST(t1.fase AS STRING) AS fase,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t1.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t1.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t1.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t1.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t1.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t1.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t1.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t1.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t1.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t1.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t1.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t1.status_cg AS STRING) AS status_cg,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(
            t1.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t1.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t1.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.fase_2 AS STRING) AS fase_2,
        CAST(t1.fase_1 AS STRING) AS fase_1,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.usuario_1 AS STRING) AS usuario_1,
        CAST(t1.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t1.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.objeto_2 AS STRING) AS objeto_2,
        CAST(t1.objeto_3 AS STRING) AS objeto_3,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_resultado AS STRING) AS processo_resultado,
        CAST(t1.materia AS STRING) AS materia,
        CAST(
            t1.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.prazo AS STRING) AS prazo,
        CAST(t1.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t1.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t1.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t1.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t1.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t1.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado_1 AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.empresa AS STRING) AS empresa,
        CAST(t2.data_da_tarefa AS STRING) AS data_da_tarefa,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.comarca AS STRING) AS comarca,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.data AS STRING) AS data,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.tipo AS STRING) AS tipo,
        CAST(t2.sub_tipo AS STRING) AS sub_tipo,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.tarefas_resumo_do_subsidio AS STRING) AS tarefas_resumo_do_subsidio,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.processo_valor_recompensa_action AS STRING) AS processo_valor_recompensa_action,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.fase AS STRING) AS fase,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(
            t2.data_resultado_observacao_1_2o_instancia AS STRING
        ) AS data_resultado_observacao_1_2o_instancia,
        CAST(t2.resultado_observacao_4_instancia AS STRING) AS resultado_observacao_4_instancia,
        CAST(t2.resultado_observacao_3_instancia AS STRING) AS resultado_observacao_3_instancia,
        CAST(t2.resultado_observacao_2_4o_instancia AS STRING) AS resultado_observacao_2_4o_instancia,
        CAST(t2.resultado_observacao_2_2o_instancia AS STRING) AS resultado_observacao_2_2o_instancia,
        CAST(t2.resultado_observacao_1_instancia AS STRING) AS resultado_observacao_1_instancia,
        CAST(t2.resultado_observacao_1_5o_instancia AS STRING) AS resultado_observacao_1_5o_instancia,
        CAST(
            t2.resultado_observacao_1_5o_instancia_1 AS STRING
        ) AS resultado_observacao_1_5o_instancia_1,
        CAST(t2.resultado_observacao_1_4o_instancia AS STRING) AS resultado_observacao_1_4o_instancia,
        CAST(t2.resultado_observacao_1_3o_instancia AS STRING) AS resultado_observacao_1_3o_instancia,
        CAST(t2.resultado_observacao_1_2o_instancia AS STRING) AS resultado_observacao_1_2o_instancia,
        CAST(t2.status_cg AS STRING) AS status_cg,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(
            t2.tarefas_quais_as_informacoes_necessarias AS STRING
        ) AS tarefas_quais_as_informacoes_necessarias,
        CAST(t2.quais_subsidios AS STRING) AS quais_subsidios,
        CAST(
            t2.favor_justificar_a_alteracao_de_valor AS STRING
        ) AS favor_justificar_a_alteracao_de_valor,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.fase_2 AS STRING) AS fase_2,
        CAST(t2.fase_1 AS STRING) AS fase_1,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_1 AS STRING) AS fase_estado_1,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.usuario_1 AS STRING) AS usuario_1,
        CAST(t2.subsidio_total_ou_parcial AS STRING) AS subsidio_total_ou_parcial,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.usuario_reclamou_a_cx_1 AS STRING) AS usuario_reclamou_a_cx_1,
        CAST(t2.data_audiencia_inicial_1 AS STRING) AS data_audiencia_inicial_1,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.objeto_2 AS STRING) AS objeto_2,
        CAST(t2.objeto_3 AS STRING) AS objeto_3,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_resultado AS STRING) AS processo_resultado,
        CAST(t2.materia AS STRING) AS materia,
        CAST(
            t2.tarefas_resultado_da_audiencia_grupo AS STRING
        ) AS tarefas_resultado_da_audiencia_grupo,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.prazo AS STRING) AS prazo,
        CAST(t2.descricao_evento_concluido AS STRING) AS descricao_evento_concluido,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.processo_data_de_reativacao AS STRING) AS processo_data_de_reativacao,
        CAST(
            t2.processo_justificativa_de_reativacao AS STRING
        ) AS processo_justificativa_de_reativacao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.processo_documento_de_identificacao AS STRING) AS processo_documento_de_identificacao,
        CAST(
            t2.processo_qual_o_motivo_da_solicitacao_de_complementacao AS STRING
        ) AS processo_qual_o_motivo_da_solicitacao_de_complementacao,
        CAST(
            t2.processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial AS STRING
        ) AS processo_a_informacao_que_foi_pedida_ja_constava_no_subsidio_inicial,
        CAST(
            t2.tarefas_descripcion_del_evento_concluido AS STRING
        ) AS tarefas_descripcion_del_evento_concluido,
        CAST(t2.tarefas_descricao_do_objeto AS STRING) AS tarefas_descricao_do_objeto
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_da_tarefa AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);
*/

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_CONFIRMADOS_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t1.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t1.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t1.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t1.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t1.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t1.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t1.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_CONFIRMADOS_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t2.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t2.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t2.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t2.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t2.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t2.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t2.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_CONFIRMADOS` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_PENDENTES_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t1.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t1.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t1.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t1.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t1.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t1.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t1.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_PENDENTES_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t2.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t2.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t2.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t2.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t2.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t2.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t2.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_PENDENTES` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados (DISTINCT para evitar duplicatas nas bases consolidadas).
SELECT DISTINCT *
FROM (
    SELECT * FROM dados_legado_filtrados
    UNION ALL
    SELECT * FROM dados_novo_filtrados
);

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_AUDIENCIAS_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t1.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t1.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t1.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t1.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t1.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t1.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t1.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_AUDIENCIAS_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t2.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t2.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t2.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t2.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t2.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t2.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t2.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_AUDIENCIAS` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
)
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_GARANTIAS_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t1.processo_id AS STRING) AS processo_id,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t1.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t1.id AS STRING) AS id,
        CAST(t1.status_1 AS STRING) AS status_1,
        CAST(t1.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t1.workflow AS STRING) AS workflow,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.estado AS STRING) AS estado,
        CAST(t1.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t1.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.responsavel AS STRING) AS responsavel,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t1.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t1.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t1.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t1.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t1.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t1.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t1.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_GARANTIAS_legado` t1
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t1.data_registrado AS STRING)) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
dados_novo_filtrados AS (
    SELECT
        CAST(
            SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) AS STRING
        ) AS data_registrado_convertida,
        CAST(t2.processo_id AS STRING) AS processo_id,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.data_de_confirmacao AS STRING) AS data_de_confirmacao,
        CAST(t2.fase_de_workflow AS STRING) AS fase_de_workflow,
        CAST(t2.id AS STRING) AS id,
        CAST(t2.status_1 AS STRING) AS status_1,
        CAST(t2.usuario_confirmado AS STRING) AS usuario_confirmado,
        CAST(t2.workflow AS STRING) AS workflow,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.estado AS STRING) AS estado,
        CAST(t2.data_registrado_1 AS STRING) AS data_registrado_1,
        CAST(t2.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.responsavel AS STRING) AS responsavel,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.tarefas_data_do_prazo AS STRING) AS tarefas_data_do_prazo,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.processo_objeto_unidade_de_negocio AS STRING) AS processo_objeto_unidade_de_negocio,
        CAST(t2.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento,
        CAST(t2.processo_informar_ajustes AS STRING) AS processo_informar_ajustes,
        CAST(t2.processo_informar_ajustes_1 AS STRING) AS processo_informar_ajustes_1,
        CAST(
            t2.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS STRING
        ) AS processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1,
        CAST(t2.processo_motivo_do_ajuste AS STRING) AS processo_motivo_do_ajuste,
        CAST(
            t2.processo_pedido_de_ajuste_foi_correto AS STRING
        ) AS processo_pedido_de_ajuste_foi_correto,
        CAST(t2.processo_motivo_do_ajuste_1 AS STRING) AS processo_motivo_do_ajuste_1
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_GARANTIAS` t2
    WHERE
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
)
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;

-----
-- Base Amélia (apenas fonte nova; legado não utilizado)
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_AMELIA_FINAL` AS
SELECT
    CAST(
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(t2.data_registrado AS STRING)) AS STRING
    ) AS data_registrado_convertida,
    CAST(t2.pais AS STRING) AS pais,
    CAST(t2.processo_procedimento_judicial AS STRING) AS processo_procedimento_judicial,
    CAST(t2.processo_objeto_objeto AS STRING) AS processo_objeto_objeto,
    CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
    CAST(t2.processo_audiencia_ficticia AS STRING) AS processo_audiencia_ficticia,
    CAST(t2.processo_invoca_hipervulnerabilidad AS STRING) AS processo_invoca_hipervulnerabilidad,
    CAST(t2.advogado_da_parte_contraria AS STRING) AS advogado_da_parte_contraria,
    CAST(
        t2.processo_o_usuario_reclama_por_dois_ou_mais_produtos_diferentes AS STRING
    ) AS processo_o_usuario_reclama_por_dois_ou_mais_produtos_diferentes,
    CAST(
        t2.processo_o_documento_de_identidade_da_reclamacao_corresponde_ao_da_compra AS STRING
    ) AS processo_o_documento_de_identidade_da_reclamacao_corresponde_ao_da_compra,
    CAST(
        t2.processo_e_high_risk_confirmado_pelo_pf AS STRING
    ) AS processo_e_high_risk_confirmado_pelo_pf,
    CAST(t2.processo_cust_id_autor AS STRING) AS processo_cust_id_autor,
    CAST(t2.processo_id_da_operacao_mp AS STRING) AS processo_id_da_operacao_mp,
    CAST(t2.processo_id_do_anuncio AS STRING) AS processo_id_do_anuncio,
    CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
    CAST(t2.parte_contraria_cpf_cnpj AS STRING) AS parte_contraria_cpf_cnpj,
    CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
    CAST(t2.processo_id AS STRING) AS processo_id,
    CAST(t2.area_do_direito AS STRING) AS area_do_direito,
    CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
    CAST(t2.status AS STRING) AS status,
    CAST(t2.valor_da_causa AS STRING) AS valor_da_causa,
    CAST(t2.data_registrado AS STRING) AS data_registrado,
    CAST(
        t2.processo_o_objeto_da_reclamacao_e_pdd_on_ou_pnr_on AS STRING
    ) AS processo_o_objeto_da_reclamacao_e_pdd_on_ou_pnr_on,
    CAST(t2.processo_fase_estado_fase AS STRING) AS processo_fase_estado_fase,
    CAST(t2.processo_fase_estado_estado AS STRING) AS processo_fase_estado_estado,
    CAST(
        t2.processo_probabilidade_de_ganhar_ou_perder_probabilidade AS STRING
    ) AS processo_probabilidade_de_ganhar_ou_perder_probabilidade
FROM
    `<ENV>.STG.STG_INPUT_DATABASE_ELAW_AMELIA` t2;

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t1.data_de_encerramento AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_de_encerramento para consistência com QUALIFY
        CAST(t1.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t1.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.outros_numeros AS STRING) AS outros_numeros,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.cliente AS STRING) AS cliente,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t1.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.processo_estado AS STRING) AS processo_estado,
        CAST(t1.processo_comarca AS STRING) AS processo_comarca,
        CAST(t1.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.acao AS STRING) AS acao,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t1.distribuicao AS STRING) AS distribuicao,
        CAST(t1.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t1.risco AS STRING) AS risco,
        CAST(t1.observacao AS STRING) AS observacao,
        CAST(t1.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t1.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t1.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t1.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t1.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t1.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t1.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t1.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t1.id_mediacao AS STRING) AS id_mediacao,
        CAST(t1.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t1.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t1.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t1.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t1.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t1.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t1.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(t1.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t1.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t1.caratula AS STRING) AS caratula,
        CAST(t1.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t1.causas_raizes AS STRING) AS causas_raizes,
        CAST(t1.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t1.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t1.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t1.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t1.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.proceso_critico AS STRING) AS proceso_critico,
        CAST(t1.cbt AS STRING) AS cbt,
        CAST(t1.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t1.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t1.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t1.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t1.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t1.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t1.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t1.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t1.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t1.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t1.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t1.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t1.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t1.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t1.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t1.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t1.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t1.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t1.processo_materia AS STRING) AS processo_materia,
        CAST(t1.justica AS STRING) AS justica,
        CAST(t1.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t1.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t1.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t1.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t1.pedido AS STRING) AS pedido,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.acao_1 AS STRING) AS acao_1,
        CAST(t1.valor_objeto AS STRING) AS valor_objeto,
        CAST(t1.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t1.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t1.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t1.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t1.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t1.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t1.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t1.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t1.processo_crime AS STRING) AS processo_crime,
        CAST(t1.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t1.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t1.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t1.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING_legado` t1
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t1.data_de_encerramento AS STRING)
        ) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t2.data_de_encerramento AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_de_encerramento para consistência com QUALIFY
        CAST(t2.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t2.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.outros_numeros AS STRING) AS outros_numeros,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.cliente AS STRING) AS cliente,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t2.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.processo_estado AS STRING) AS processo_estado,
        CAST(t2.processo_comarca AS STRING) AS processo_comarca,
        CAST(t2.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.acao AS STRING) AS acao,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t2.distribuicao AS STRING) AS distribuicao,
        CAST(t2.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t2.risco AS STRING) AS risco,
        CAST(t2.observacao AS STRING) AS observacao,
        CAST(t2.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t2.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t2.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t2.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t2.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t2.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t2.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t2.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t2.id_mediacao AS STRING) AS id_mediacao,
        CAST(t2.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t2.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t2.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t2.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t2.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t2.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t2.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(t2.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t2.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t2.caratula AS STRING) AS caratula,
        CAST(t2.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t2.causas_raizes AS STRING) AS causas_raizes,
        CAST(t2.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t2.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t2.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t2.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t2.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.proceso_critico AS STRING) AS proceso_critico,
        CAST(t2.cbt AS STRING) AS cbt,
        CAST(t2.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t2.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t2.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t2.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t2.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t2.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t2.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t2.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t2.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t2.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t2.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t2.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t2.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t2.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t2.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t2.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t2.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t2.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t2.processo_materia AS STRING) AS processo_materia,
        CAST(t2.justica AS STRING) AS justica,
        CAST(t2.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t2.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t2.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t2.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t2.pedido AS STRING) AS pedido,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.acao_1 AS STRING) AS acao_1,
        CAST(t2.valor_objeto AS STRING) AS valor_objeto,
        CAST(t2.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t2.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t2.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t2.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t2.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t2.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t2.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t2.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t2.processo_crime AS STRING) AS processo_crime,
        CAST(t2.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t2.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t2.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t2.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING` t2
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_de_encerramento AS STRING)
        ) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_de_encerramento AS STRING)
        ) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados, selecionando apenas as colunas desejadas
-- e deduplicando-os com base no 'processo_id' e 'data_registrado_convertida'.
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t1.data_de_encerramento AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_de_encerramento para consistência com QUALIFY
        CAST(t1.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t1.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.outros_numeros AS STRING) AS outros_numeros,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.cliente AS STRING) AS cliente,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t1.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.processo_estado AS STRING) AS processo_estado,
        CAST(t1.processo_comarca AS STRING) AS processo_comarca,
        CAST(t1.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.acao AS STRING) AS acao,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t1.distribuicao AS STRING) AS distribuicao,
        CAST(t1.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t1.risco AS STRING) AS risco,
        CAST(t1.observacao AS STRING) AS observacao,
        CAST(t1.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t1.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t1.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t1.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t1.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t1.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t1.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t1.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t1.id_mediacao AS STRING) AS id_mediacao,
        CAST(t1.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t1.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t1.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t1.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t1.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t1.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t1.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(t1.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t1.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t1.caratula AS STRING) AS caratula,
        CAST(t1.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t1.causas_raizes AS STRING) AS causas_raizes,
        CAST(t1.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t1.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t1.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t1.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t1.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.proceso_critico AS STRING) AS proceso_critico,
        CAST(t1.cbt AS STRING) AS cbt,
        CAST(t1.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t1.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t1.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t1.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t1.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t1.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t1.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t1.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t1.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t1.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t1.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t1.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t1.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t1.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t1.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t1.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t1.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t1.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t1.processo_materia AS STRING) AS processo_materia,
        CAST(t1.justica AS STRING) AS justica,
        CAST(t1.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t1.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t1.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t1.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t1.pedido AS STRING) AS pedido,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.acao_1 AS STRING) AS acao_1,
        CAST(t1.valor_objeto AS STRING) AS valor_objeto,
        CAST(t1.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t1.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t1.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t1.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t1.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t1.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t1.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t1.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t1.processo_crime AS STRING) AS processo_crime,
        CAST(t1.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t1.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t1.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t1.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING_legado` t1
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t1.data_de_encerramento AS STRING)
        ) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t2.data_de_encerramento AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_de_encerramento para consistência com QUALIFY
        CAST(t2.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t2.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.outros_numeros AS STRING) AS outros_numeros,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.cliente AS STRING) AS cliente,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t2.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.processo_estado AS STRING) AS processo_estado,
        CAST(t2.processo_comarca AS STRING) AS processo_comarca,
        CAST(t2.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.acao AS STRING) AS acao,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t2.distribuicao AS STRING) AS distribuicao,
        CAST(t2.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t2.risco AS STRING) AS risco,
        CAST(t2.observacao AS STRING) AS observacao,
        CAST(t2.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t2.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t2.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t2.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t2.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t2.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t2.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t2.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t2.id_mediacao AS STRING) AS id_mediacao,
        CAST(t2.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t2.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t2.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t2.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t2.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t2.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t2.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(t2.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t2.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t2.caratula AS STRING) AS caratula,
        CAST(t2.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t2.causas_raizes AS STRING) AS causas_raizes,
        CAST(t2.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t2.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t2.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t2.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t2.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.proceso_critico AS STRING) AS proceso_critico,
        CAST(t2.cbt AS STRING) AS cbt,
        CAST(t2.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t2.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t2.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t2.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t2.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t2.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t2.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t2.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t2.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t2.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t2.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t2.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t2.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t2.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t2.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t2.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t2.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t2.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t2.processo_materia AS STRING) AS processo_materia,
        CAST(t2.justica AS STRING) AS justica,
        CAST(t2.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t2.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t2.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t2.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t2.pedido AS STRING) AS pedido,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.acao_1 AS STRING) AS acao_1,
        CAST(t2.valor_objeto AS STRING) AS valor_objeto,
        CAST(t2.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t2.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t2.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t2.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t2.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t2.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t2.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t2.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t2.processo_crime AS STRING) AS processo_crime,
        CAST(t2.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t2.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t2.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t2.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING` t2
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_de_encerramento AS STRING)
        ) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
        AND SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_de_encerramento AS STRING)
        ) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
) -- Une os dados legados e os novos dados, selecionando apenas as colunas desejadas
-- e deduplicando-os com base no 'processo_id' e 'data_registrado_convertida'.
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t1.data_registrado AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência com QUALIFY
        CAST(t1.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t1.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.outros_numeros AS STRING) AS outros_numeros,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.cliente AS STRING) AS cliente,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t1.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.processo_estado AS STRING) AS processo_estado,
        CAST(t1.processo_comarca AS STRING) AS processo_comarca,
        CAST(t1.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.acao AS STRING) AS acao,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t1.distribuicao AS STRING) AS distribuicao,
        CAST(t1.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t1.risco AS STRING) AS risco,
        CAST(t1.observacao AS STRING) AS observacao,
        CAST(t1.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t1.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t1.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t1.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t1.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t1.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t1.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t1.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t1.id_mediacao AS STRING) AS id_mediacao,
        CAST(t1.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t1.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t1.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t1.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t1.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t1.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t1.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(t1.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t1.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t1.caratula AS STRING) AS caratula,
        CAST(t1.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t1.causas_raizes AS STRING) AS causas_raizes,
        CAST(t1.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t1.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t1.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t1.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t1.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.proceso_critico AS STRING) AS proceso_critico,
        CAST(t1.cbt AS STRING) AS cbt,
        CAST(t1.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t1.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t1.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t1.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t1.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t1.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t1.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t1.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t1.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t1.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t1.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t1.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t1.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t1.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t1.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t1.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t1.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t1.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t1.processo_materia AS STRING) AS processo_materia,
        CAST(t1.justica AS STRING) AS justica,
        CAST(t1.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t1.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t1.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t1.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t1.pedido AS STRING) AS pedido,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.acao_1 AS STRING) AS acao_1,
        CAST(t1.valor_objeto AS STRING) AS valor_objeto,
        CAST(t1.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t1.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t1.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t1.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t1.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t1.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t1.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t1.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t1.processo_crime AS STRING) AS processo_crime,
        CAST(t1.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t1.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t1.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t1.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING_legado` t1
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t1.data_registrado AS STRING) -- CAMPO ALTERADO
        ) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t2.data_registrado AS STRING)
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência com QUALIFY
        CAST(t2.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t2.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.outros_numeros AS STRING) AS outros_numeros,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.cliente AS STRING) AS cliente,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t2.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.processo_estado AS STRING) AS processo_estado,
        CAST(t2.processo_comarca AS STRING) AS processo_comarca,
        CAST(t2.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.acao AS STRING) AS acao,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t2.distribuicao AS STRING) AS distribuicao,
        CAST(t2.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t2.risco AS STRING) AS risco,
        CAST(t2.observacao AS STRING) AS observacao,
        CAST(t2.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t2.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t2.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t2.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t2.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t2.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t2.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t2.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t2.id_mediacao AS STRING) AS id_mediacao,
        CAST(t2.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t2.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t2.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t2.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t2.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t2.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t2.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(t2.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t2.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t2.caratula AS STRING) AS caratula,
        CAST(t2.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t2.causas_raizes AS STRING) AS causas_raizes,
        CAST(t2.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t2.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t2.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t2.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t2.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.proceso_critico AS STRING) AS proceso_critico,
        CAST(t2.cbt AS STRING) AS cbt,
        CAST(t2.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t2.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t2.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t2.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t2.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t2.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t2.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t2.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t2.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t2.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t2.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t2.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t2.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t2.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t2.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t2.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t2.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t2.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t2.processo_materia AS STRING) AS processo_materia,
        CAST(t2.justica AS STRING) AS justica,
        CAST(t2.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t2.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t2.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t2.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t2.pedido AS STRING) AS pedido,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.acao_1 AS STRING) AS acao_1,
        CAST(t2.valor_objeto AS STRING) AS valor_objeto,
        CAST(t2.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t2.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t2.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t2.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t2.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t2.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t2.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t2.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t2.processo_crime AS STRING) AS processo_crime,
        CAST(t2.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t2.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t2.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t2.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING` t2
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_registrado AS STRING) -- CAMPO ALTERADO
        ) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
) -- Une os dados legados e os novos dados, selecionando apenas as colunas desejadas
-- e deduplicando-os com base no 'processo_id' e 'data_registrado_convertida'.
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;

-----
CREATE
OR REPLACE TABLE `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING_FINAL` AS WITH -- CTE para dados legados (corte = 1º dia do mês atual).
dados_legado_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t1.data_registrado AS STRING) -- CAMPO ALTERADO
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência com QUALIFY
        CAST(t1.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t1.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t1.pasta AS STRING) AS pasta,
        CAST(t1.pais AS STRING) AS pais,
        CAST(t1.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t1.outros_numeros AS STRING) AS outros_numeros,
        CAST(t1.status AS STRING) AS status,
        CAST(t1.area_do_direito AS STRING) AS area_do_direito,
        CAST(t1.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t1.cliente AS STRING) AS cliente,
        CAST(t1.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t1.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t1.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t1.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t1.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t1.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t1.processo_estado AS STRING) AS processo_estado,
        CAST(t1.processo_comarca AS STRING) AS processo_comarca,
        CAST(t1.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t1.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t1.acao AS STRING) AS acao,
        CAST(t1.objeto AS STRING) AS objeto,
        CAST(t1.objeto_1 AS STRING) AS objeto_1,
        CAST(t1.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t1.distribuicao AS STRING) AS distribuicao,
        CAST(t1.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t1.risco AS STRING) AS risco,
        CAST(t1.observacao AS STRING) AS observacao,
        CAST(t1.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t1.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t1.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t1.modalidade AS STRING) AS modalidade,
        CAST(t1.data_registrado AS STRING) AS data_registrado,
        CAST(t1.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t1.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t1.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t1.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t1.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t1.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t1.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t1.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t1.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t1.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t1.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t1.id_mediacao AS STRING) AS id_mediacao,
        CAST(t1.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t1.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t1.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t1.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t1.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t1.fase_estado AS STRING) AS fase_estado,
        CAST(t1.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t1.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t1.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t1.usuario AS STRING) AS usuario,
        CAST(t1.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t1.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t1.caratula AS STRING) AS caratula,
        CAST(t1.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t1.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t1.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t1.causas_raizes AS STRING) AS causas_raizes,
        CAST(t1.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t1.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t1.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t1.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t1.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t1.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t1.proceso_critico AS STRING) AS proceso_critico,
        CAST(t1.cbt AS STRING) AS cbt,
        CAST(t1.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t1.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t1.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t1.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t1.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t1.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t1.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t1.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t1.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t1.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t1.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t1.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t1.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t1.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t1.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t1.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t1.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t1.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t1.processo_materia AS STRING) AS processo_materia,
        CAST(t1.justica AS STRING) AS justica,
        CAST(t1.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t1.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t1.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t1.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t1.pedido AS STRING) AS pedido,
        CAST(
            t1.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t1.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t1.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t1.acao_1 AS STRING) AS acao_1,
        CAST(t1.valor_objeto AS STRING) AS valor_objeto,
        CAST(t1.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t1.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t1.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t1.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t1.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t1.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t1.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t1.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t1.processo_crime AS STRING) AS processo_crime,
        CAST(t1.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t1.processo_prazo AS STRING) AS processo_prazo,
        CAST(t1.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t1.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t1.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t1.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING_legado` t1
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t1.data_registrado AS STRING) -- CAMPO ALTERADO
        ) < DATE_TRUNC(CURRENT_DATE(), MONTH)
),
-- CTE para dados inéditos (base nova = mês atual em diante).
dados_novo_filtrados AS (
    SELECT
        -- Colunas especificadas pelo usuário e as essenciais para a lógica, todas convertidas para STRING
        CAST(
            SAFE.PARSE_DATE(
                '%d/%m/%Y',
                CAST(t2.data_registrado AS STRING) -- CAMPO ALTERADO
            ) AS STRING
        ) AS data_registrado_convertida,
        -- Derivada de data_registrado para consistência com QUALIFY
        CAST(t2.data_de_citacao AS STRING) AS data_de_citacao,
        CAST(t2.processo_id AS STRING) AS processo_id,
        -- Chave de partição para QUALIFY
        CAST(t2.pasta AS STRING) AS pasta,
        CAST(t2.pais AS STRING) AS pais,
        CAST(t2.numero_do_processo AS STRING) AS numero_do_processo,
        CAST(t2.outros_numeros AS STRING) AS outros_numeros,
        CAST(t2.status AS STRING) AS status,
        CAST(t2.area_do_direito AS STRING) AS area_do_direito,
        CAST(t2.sub_area_do_direito AS STRING) AS sub_area_do_direito,
        CAST(t2.cliente AS STRING) AS cliente,
        CAST(t2.parte_contraria_nome AS STRING) AS parte_contraria_nome,
        CAST(t2.cust_id_autor AS STRING) AS cust_id_autor,
        CAST(t2.outras_partes_nao_clientes AS STRING) AS outras_partes_nao_clientes,
        CAST(t2.page_report_escritorioresponsavel AS STRING) AS page_report_escritorioresponsavel,
        CAST(t2.data_audiencia_inicial AS STRING) AS data_audiencia_inicial,
        CAST(t2.advogado_responsavel AS STRING) AS advogado_responsavel,
        CAST(t2.processo_estado AS STRING) AS processo_estado,
        CAST(t2.processo_comarca AS STRING) AS processo_comarca,
        CAST(t2.processo_foro_tribunal_orgao AS STRING) AS processo_foro_tribunal_orgao,
        CAST(t2.processo_vara_orgao AS STRING) AS processo_vara_orgao,
        CAST(t2.acao AS STRING) AS acao,
        CAST(t2.objeto AS STRING) AS objeto,
        CAST(t2.objeto_1 AS STRING) AS objeto_1,
        CAST(t2.detalhamento_do_objeto AS STRING) AS detalhamento_do_objeto,
        CAST(t2.distribuicao AS STRING) AS distribuicao,
        CAST(t2.tipo_de_contingencia AS STRING) AS tipo_de_contingencia,
        CAST(t2.risco AS STRING) AS risco,
        CAST(t2.observacao AS STRING) AS observacao,
        CAST(t2.tipo_da_audiencia_inicial AS STRING) AS tipo_da_audiencia_inicial,
        CAST(t2.valor_da_causa AS STRING) AS valor_da_causa,
        CAST(t2.outros_clientes_reu AS STRING) AS outros_clientes_reu,
        CAST(t2.modalidade AS STRING) AS modalidade,
        CAST(t2.data_registrado AS STRING) AS data_registrado,
        CAST(t2.cpf_cnpj AS STRING) AS cpf_cnpj,
        CAST(t2.parte_contraria_cpf AS STRING) AS parte_contraria_cpf,
        CAST(t2.data_de_encerramento AS STRING) AS data_de_encerramento,
        CAST(t2.data_de_registro_do_encerramento AS STRING) AS data_de_registro_do_encerramento,
        CAST(t2.data_do_envio_ao_escritorio AS STRING) AS data_do_envio_ao_escritorio,
        CAST(t2.procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(t2.resumo_do_subsidio AS STRING) AS resumo_do_subsidio,
        CAST(t2.advogado_da_parte_contraria_nome AS STRING) AS advogado_da_parte_contraria_nome,
        CAST(t2.advogados_participantes AS STRING) AS advogados_participantes,
        CAST(t2.advogado_da_parte_contraria_cpf AS STRING) AS advogado_da_parte_contraria_cpf,
        CAST(t2.cust_id_contraparte AS STRING) AS cust_id_contraparte,
        CAST(t2.id_mediacao AS STRING) AS id_mediacao,
        CAST(t2.centro_custo_nome AS STRING) AS centro_custo_nome,
        CAST(t2.centro_de_custo_codigo AS STRING) AS centro_de_custo_codigo,
        CAST(t2.valor_do_risco AS STRING) AS valor_do_risco,
        CAST(t2.comportamento_do_usuario_cx AS STRING) AS comportamento_do_usuario_cx,
        CAST(t2.id_do_pagamento AS STRING) AS id_do_pagamento,
        CAST(t2.fase_estado AS STRING) AS fase_estado,
        CAST(t2.fase_estado_4 AS STRING) AS fase_estado_4,
        CAST(t2.parte_contraria_contumaz AS STRING) AS parte_contraria_contumaz,
        CAST(t2.advogado_parte_contraria_contumaz AS STRING) AS advogado_parte_contraria_contumaz,
        CAST(t2.usuario AS STRING) AS usuario,
        CAST(t2.audiencia_pendente_data AS STRING) AS audiencia_pendente_data,
        CAST(t2.motivo_de_encerramento AS STRING) AS motivo_de_encerramento,
        CAST(t2.caratula AS STRING) AS caratula,
        CAST(t2.indica_menoridade AS STRING) AS indica_menoridade,
        CAST(t2.processo_classificacao AS STRING) AS processo_classificacao,
        CAST(t2.invoca_hipervulnerabilidad AS STRING) AS invoca_hipervulnerabilidad,
        CAST(t2.causas_raizes AS STRING) AS causas_raizes,
        CAST(t2.causas_raizes_1 AS STRING) AS causas_raizes_1,
        CAST(t2.causas_raizes_2 AS STRING) AS causas_raizes_2,
        CAST(t2.id_de_salesforce AS STRING) AS id_de_salesforce,
        CAST(t2.modelo_de_contratacao AS STRING) AS modelo_de_contratacao,
        CAST(t2.numero_de_envio AS STRING) AS numero_de_envio,
        CAST(t2.usuario_reclamou_a_cx AS STRING) AS usuario_reclamou_a_cx,
        CAST(t2.proceso_critico AS STRING) AS proceso_critico,
        CAST(t2.cbt AS STRING) AS cbt,
        CAST(t2.unidade_de_negocio_impactada AS STRING) AS unidade_de_negocio_impactada,
        CAST(
            t2.campos_de_alteracao_de_valor_identificacao_do_pagamento AS STRING
        ) AS campos_de_alteracao_de_valor_identificacao_do_pagamento,
        CAST(t2.processo_cust_id_contraparte AS STRING) AS processo_cust_id_contraparte,
        CAST(t2.processo_identificacao_do_pagamento AS STRING) AS processo_identificacao_do_pagamento,
        CAST(t2.valor_1_instancia AS STRING) AS valor_1_instancia,
        CAST(
            t2.informacoes_complementares_cust_id_contraparte AS STRING
        ) AS informacoes_complementares_cust_id_contraparte,
        CAST(t2.processo_cust_id_contraparte_1 AS STRING) AS processo_cust_id_contraparte_1,
        CAST(t2.processo_apelido_contraparte AS STRING) AS processo_apelido_contraparte,
        CAST(t2.empresa_responsavel AS STRING) AS empresa_responsavel,
        CAST(
            t2.processo_identificacao_do_pagamento_1 AS STRING
        ) AS processo_identificacao_do_pagamento_1,
        CAST(t2.processo_empresa_demandada AS STRING) AS processo_empresa_demandada,
        CAST(t2.hisp_subsidios_id_da_operacao_mp AS STRING) AS hisp_subsidios_id_da_operacao_mp,
        CAST(t2.hisp_subsidios_status_do_pagamento AS STRING) AS hisp_subsidios_status_do_pagamento,
        CAST(t2.hisp_subsidios_cust_id_autor AS STRING) AS hisp_subsidios_cust_id_autor,
        CAST(t2.hisp_subsidios_numero_de_envio AS STRING) AS hisp_subsidios_numero_de_envio,
        CAST(t2.processo_custid_meli AS STRING) AS processo_custid_meli,
        CAST(t2.processo_revisado_por_dre AS STRING) AS processo_revisado_por_dre,
        CAST(
            t2.processo_escritorio_do_advogado_da_parte_contraria AS STRING
        ) AS processo_escritorio_do_advogado_da_parte_contraria,
        CAST(t2.processo_materia AS STRING) AS processo_materia,
        CAST(t2.justica AS STRING) AS justica,
        CAST(t2.processo_objeto_revisado AS STRING) AS processo_objeto_revisado,
        CAST(t2.processo_revisado_por_dre_1 AS STRING) AS processo_revisado_por_dre_1,
        CAST(t2.forma_de_participacao AS STRING) AS forma_de_participacao,
        CAST(t2.escritorio_externo AS STRING) AS escritorio_externo,
        CAST(t2.pedido AS STRING) AS pedido,
        CAST(
            t2.processo_apresentada_resposta_negativa AS STRING
        ) AS processo_apresentada_resposta_negativa,
        CAST(t2.data_de_reativacao AS STRING) AS data_de_reativacao,
        CAST(t2.motivo_de_reativacao AS STRING) AS motivo_de_reativacao,
        CAST(t2.acao_1 AS STRING) AS acao_1,
        CAST(t2.valor_objeto AS STRING) AS valor_objeto,
        CAST(t2.processo_condenacao_em_ma_fe AS STRING) AS processo_condenacao_em_ma_fe,
        CAST(t2.processo_valor_associado_a_ma_fe AS STRING) AS processo_valor_associado_a_ma_fe,
        CAST(t2.processo_data_denuncia AS STRING) AS processo_data_denuncia,
        CAST(t2.processo_data_do_protocolo AS STRING) AS processo_data_do_protocolo,
        CAST(t2.processo_data_instauracao AS STRING) AS processo_data_instauracao,
        CAST(t2.processo_estado_da_denuncia AS STRING) AS processo_estado_da_denuncia,
        CAST(t2.processo_tipo_de_operacao AS STRING) AS processo_tipo_de_operacao,
        CAST(t2.processo_data_da_operacao AS STRING) AS processo_data_da_operacao,
        CAST(t2.processo_crime AS STRING) AS processo_crime,
        CAST(t2.processo_crime_2 AS STRING) AS processo_crime_2,
        CAST(t2.processo_prazo AS STRING) AS processo_prazo,
        CAST(t2.advogado_escritorio AS STRING) AS advogado_escritorio,
        CAST(t2.processo_estado_de_la_denuncia AS STRING) AS processo_estado_de_la_denuncia,
        CAST(t2.decisao_analise_de_responsabilidade AS STRING) AS decisao_analise_de_responsabilidade,
        CAST(t2.processo_superendividamento AS STRING) AS processo_superendividamento
    FROM
        `<ENV>.STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING` t2
    WHERE
        SAFE.PARSE_DATE(
            '%d/%m/%Y',
            CAST(t2.data_registrado AS STRING) -- CAMPO ALTERADO
        ) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
) -- Une os dados legados e os novos dados, selecionando apenas as colunas desejadas
-- e deduplicando-os com base no 'processo_id' e 'data_registrado_convertida'.
SELECT
    *
FROM
    dados_legado_filtrados
UNION ALL
SELECT
    *
FROM
    dados_novo_filtrados;



-----
-- Extração de Multas: legado (corte = 1º dia mês atual) + inédito (mês atual em diante)
CREATE OR REPLACE TABLE `<ENV>.STG.Database_eLAW_Extracao_multas_FINAL` AS
WITH
  dados_legado_filtrados AS (
    SELECT
      CAST(t1.processo_id AS STRING) AS processo_id,
      CAST(t1.data AS STRING) AS data,
      CAST(t1.tipo AS STRING) AS tipo,
      CAST(t1.data_registrado AS STRING) AS data_registrado
    FROM
      `<ENV>.STG.Database_eLAW_Extracao_multas_legado` t1
    WHERE
      SAFE.PARSE_DATE('%d/%m/%Y', TRIM(CAST(t1.data_registrado AS STRING))) IS NOT NULL
      AND SAFE.PARSE_DATE('%d/%m/%Y', TRIM(CAST(t1.data_registrado AS STRING))) < DATE_TRUNC(CURRENT_DATE(), MONTH)
  ),
  dados_novo_filtrados AS (
    SELECT
      CAST(t2.processo_id AS STRING) AS processo_id,
      CAST(t2.data AS STRING) AS data,
      CAST(t2.tipo AS STRING) AS tipo,
      CAST(t2.data_registrado AS STRING) AS data_registrado
    FROM
      `<ENV>.STG.STG_INPUT_DATABASE_ELAW_EXTRACAO_MULTAS` t2
    WHERE
      SAFE.PARSE_DATE('%d/%m/%Y', TRIM(CAST(t2.data_registrado AS STRING))) IS NOT NULL
      AND SAFE.PARSE_DATE('%d/%m/%Y', TRIM(CAST(t2.data_registrado AS STRING))) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
      AND SAFE.PARSE_DATE('%d/%m/%Y', TRIM(CAST(t2.data_registrado AS STRING))) < DATE_ADD(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH)
  )
SELECT
  *
FROM
  dados_legado_filtrados
UNION ALL
SELECT
  *
FROM
  dados_novo_filtrados;
