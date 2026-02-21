/* =====================================================================
log de alteração:
  DATA: 24/11/2025
  AUTOR: MURILLO FRANÇA
  ALTERAÇÃO: INCLUSÃO DOS CAMPOS FLAG_FOCO, GRUPO_PAIS, DATA_REGISTRADO_1 as data_tarefa
  ---------------------------------------------------------------------
  DATA: 05/01/2026
  ALTERAÇÃO: ATUALIZAÇÃO DA TABELA DIM_WORKFLOW PARA VERSÃO _REVIEW
===================================================================== */

CREATE OR REPLACE TABLE `<ENV>.STG.TBL_FINAL_CONSOLIDADA_SUBSIDIOS` AS
WITH
/* =====================================================================
   1. CAP — FONTES HISPANOS (CAP / CAP_CX / OPS_ENLI / OPS_INTER)
   ===================================================================== */

cap AS (
    SELECT
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(DATA AS STRING)) AS registro_tarefa,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_1 AS status_tarefa,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado AS STRING)) AS data_registrado,
        objeto_3,
        usuario,
        CAST(NULL AS STRING) AS DATA_REGISTRADO_1
W_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_FINAL`
),

cap_cx AS (
    SELECT
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(DATA AS STRING)) AS data_registrado,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_1 AS status_tarefa,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado AS STRING)) AS registro_processo,
        objeto_3,
        usuario,
        CAST(NULL AS STRING) AS DATA_REGIS        CAST(NULL AS STRING) AS DATA_REGISTRADO_1
_CX_FINAL`
),

ops_1 AS (
    SELECT
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(DATA AS STRING)) AS data_registrado,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_1 AS status_tarefa,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado_1 AS STRING)) AS registro_processo,
        objeto_3,
        usuario,
        CAST(NULL AS STRING) AS DATA_REGISTRADO_1
    FROM `<ENV>.STG.STG_INPUT_DAT        CAST(NULL AS STRING) AS DATA_REGISTRADO_1

        processo_id,
        area_do_direito,
        sub_area_do_direito,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_de_confirmacao AS STRING)) AS data_de_confirmacao,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(DATA AS STRING)) AS data_registrado,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_1 AS status_tarefa,
        SAFE.PARSE_DATE('%d/%m/%Y', CAST(data_registrado_1 AS STRING)) AS registro_processo,
        objeto_3,
        usuario,
        CAST(NULL AS STRING) AS DATA_REGISTRADO_1
    FROM `<ENV>.STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HIS        CAST(NULL AS STRING) AS DATA_REGISTRADO_1
M cap_cx
    UNION ALL SELECT * FROM ops_1
    UNION ALL SELECT * FROM ops_2
),

/* =====================================================================
   2. PROCESSAMENTO HISPANOS
   ===================================================================== */

processed AS (
    SELECT
        UPPER(fase_de_workflow) AS fase_de_workflow,
        UPPER(workflow) AS workflow,
        objeto_3 AS objeto,
        'Enlighten' AS empresa,
        DATE_DIFF(data_de_confirmacao, data_registrado, DAY) AS tempo_medio_resposta,
        * EXCEPT (fase_de_workflow, workflow)
    FROM raw_hsp
),

final AS (
    SELECT
        p.*,
        df.grupo AS tipo_tarefa
    FROM processed p
    -- ALTERADO AQUI: _REVIEW
    LEFT JOIN `<ENV>.STG.DIM_15_DIMENSAO_WORKFLOW` df
           ON UPPER(TRIM(p.workflow)) = UPPER(TRIM(df.workflow))
          AND UPPER(TRIM(p.fase_de_workflow)) = UPPER(TRIM(df.fase_de_workflow))
    WHERE df.Considerar = 'Sim'
),

final_hsp AS (
    SELECT
        data_registrado,
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        data_de_confirmacao,
        registro_tarefa,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_tarefa,
        usuario,
        objeto,
        empresa,
        tempo_medio_resposta,
        tipo_tarefa,
        CAST(NULL AS STRING) AS procedimento_judicial,
        CAST(NULL AS STRING) AS processo_classificacao,
        DATA_REGISTRADO_1
    FROM final
),

/* =====================================================================
   3. BASE BRASIL
   =======================        DATA_REGISTRADO_1
= */

base_bra AS (
    SELECT
        a.processo_id,
        a.status,
        SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado) AS data_registrado,
        SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado_1) AS registro_tarefa,
        SAFE.PARSE_DATE('%d/%m/%Y', a.data_de_confirmacao) AS data_de_confirmacao,
        a.area_do_direito,
        a.sub_area_do_direito,
        UPPER(TRIM(a.fase_de_workflow)) AS fase_workflow,
        a.id,
        a.status_1 AS status_tarefa,
        a.responsavel AS usuario,
        UPPER(TRIM(a.workflow)) AS workflow,
        a.pais,
        a.estado,
        CAST(a.processo_procedimento_judicial AS STRING) AS procedimento_judicial,
        CAST(a.processo_objeto_unidade_de_negocio AS STRING) AS objeto_unidade_negocio,
        a.processo_objeto_objeto AS objeto,
        a.processo_indicar_ajuste_nome_do_campo_erro_detalhamento AS indicador_ajuste_erro,
        a.processo_informar_ajustes,
        a.processo_informar_ajustes_1 AS informar_ajustes_1,
        a.processo_indicar_ajuste_nome_do_campo_erro_detalhamento_1 AS indicador_ajuste_erro_1,
        a.processo_motivo_do_ajuste AS motivo_ajuste,
        a.processo_pedido_de_ajuste_foi_correto AS pedido_ajuste_correto,
        a.processo_motivo_do_ajuste_1 AS motivo_ajuste_1,
        a.processo_prazo AS prazo,
        CAST(a.processo_classificacao AS STRING) AS processo_classificacao,
        a.tarefas_data_do_prazo AS tarefas_data_prazo,
        a.aud_ins_dttm,
        a.aud_upd_dttm,
        CASE
            WHEN a.estado IN ('MG','RJ','SP') THEN 'Finch' ELSE 'Enlighten'
        END AS empresa,
        IFNULL(
            DATE_DIFF(
                SAFE.PARSE_DASAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado_1),
                DAY
            ), 0
        ) AS tempo_medio_resposta,
        df.grupo AS tipo_tarefa,
        a.data_registrado_1 AS data_tarefa
    FROM `<ENV>.STG.LK_PBD_LA_VW_TAREFAS_AGENDAMENTOS_CLEAN` a
    -- ALTERADO AQUI: _REVIEW
    LEFT JOIN `<ENV>.STG.DIM_15_DIMENSAO_WORKFLOW` df
           ON UPPER(TRIM(a.workflow)) = UPPER(TRIM(df.workflow))
          AND UPPER(TRIM(a.fase_de_workflow)) = UPPER(TRIM(df.fase_de_workflow))
    WHERE df.considerar = 'Sim'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY a.processo_id, a.id ORDER BY SAFE.PARSE_DATE('%d/%m/%Y', a.data_registrado)) = 1
),

final_bra_trim AS (
    SELECT
        data_registrado,
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        data_de_confirmacao,
        registro_tarefa,
        fase_workflow AS fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        status_tarefa,
        usuario,
        objeto,
        empresa,
        tempo_medio_resposta,
        tipo_tarefa,
        procedimento_judicial,
        processo_classificacao,
        data_tarefa
    FROM base_bra
),

/* =====================================================================
   4. UNIÃO HSP + BRASIL
   ===================================================================== */

united AS (
            data_tarefa
 ALL
    SELECT * FROM final_hsp
),

/* =====================================================================
   5. FILTROS, NORMALIZAÇÕES E DEDUP
   ===================================================================== */

filtrado AS (
    SELECT
        *,
        CASE WHEN empresa IN ('Finch','') THEN 'Enlighten' ELSE empresa END AS empresa_norm,
        COALESCE(tipo_tarefa, 'Complementação de subsídio') AS tipo_tarefa_norm
    FROM united
    WHERE area_do_direito <> 'Requerimentos'
      AND area_do_direito IN ('Consumidor','CORP - Civil','CORP - Consumidor','Cível')
),

dedup AS (
    SELECT
        processo_id,
        area_do_direito,
        sub_area_do_direito,
        data_registrado,
        registro_tarefa,
        data_de_confirmacao,
        fase_de_workflow,
        id,
        status,
        workflow,
        pais,
        estado,
        usuario,
        objeto,
        tempo_medio_resposta,
        tipo_tarefa_norm AS tipo_tarefa,
        status_tarefa,
        procedimento_judicial,
        processo_classificacao,
        empresa_norm AS empresa,
        data_tarefa
    FROM filtrado
    QUALIFY ROW_NUMBER() OVER (PARTITION BY processo_id, id ORDER BY data_registrado DESC) = 1
),

/* =====================================================================
   6. CLASSIFICAÇÕES FINAIS
   ============        data_tarefa
================== */

subsidios AS (
    SELECT
        d.*,
        CASE
            WHEN UPPER(TRIM(fase_de_workflow)) = 'ELABORAR SUBSÍDIOS' THEN 'Subsídios_BR'
            WHEN UPPER(TRIM(fase_de_workflow)) IN ('CONFECCIÓN DEL SUBSÍDIO','CONFECCIÓN DEL SUBSIDIO') THEN 'Subsídios_HSP'
        END AS tc_subsidios,

        CASE
            WHEN UPPER(TRIM(fase_de_workflow)) = 'ELABORAR COMPLEMENTAÇÃO DE SUBSÍDIOS' THEN 'Complementação_BR'
            WHEN UPPER(TRIM(fase_de_workflow)) IN ('PROVIDÊNCIA - CAP','COMPLEMENTAÇÃO DE SUBSÍDIOS - ENL') THEN 'Complementação_HSP'
        END AS tc_complementacao,

        CASE
            WHEN pais = 'Brasil'
             AND fase_de_workflow IN ('ELABORAR COMPLEMENTAÇÃO DE SUBSÍDIOS','ELABORAR SUBSÍDIOS')
             AND area_do_direito IN ('Consumidor','Civel','Cível','Civil')
             AND sub_area_do_direito IN ('Administrativo','Judicial')
            THEN 'Foco Brasil'

            WHEN pais <> 'Brasil'
             AND fase_de_workflow IN ('COMPLEMENTAÇÃO DE SUBSÍDIOS - ENL','CONFEÇÃO DE SUBSÍDIO','CONFECCIÓN DEL SUBSÍDIO','INFORMAR LOS DATOS')
             AND area_do_direito IN ('CORP - Consumidor','CORP - Civil','CORP - Civel')
            THEN 'Foco HSP'

            WHEN fase_de_workflow IN ('PROVIDÊNCIA - CAP') 
            THEN 'Foco CAP'
            ELSE 'Outros'
        END AS Flag_foco,

        CASE WHEN pais = 'Brasil' THEN 'Brasil' ELSE 'HSP' END AS grupo_pais
    FROM dedup d
    WHERE workflow IN (
          'CADASTRO/SUBSÍDIOS - CÍVEL JUDICIAL E ADMINISTRATIVO',
          'CADASTRO/SUBSÍDIOS - CONSUMIDOR JUDICIAL',
          'CADASTRO/SUBSÍDIOS PRÉ ADMINISTRATIVO/ ADMINISTRATIVO - CONSUMIDOR',
          'COMPLEMENTAÇÃO SUBSÍDIOS (ACIONAMENTO AVULSO)',
          'RECOVERY - SUBSÍDIOS',
          'SUBSÍDIOS AVULSO - BASE MIGRADA',
          'ACIONAMENTO - SUBSÍDIOS',
          'HISP - SUBSIDIOS GERAL'
    )
)

/* =====================================================================
   7. RESULTADO FINAL
   ===================================================================== */

SELECT DISTINCT *
FROM subsidios