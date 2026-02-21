WITH CASOS_ERROS AS (
    SELECT
        tipo_erro,
        origem,
        DATE(dt_envio_bc) AS dt_envio_bc,
        DATE(dt_limite_resp) AS dt_limite_resp,
        dias_em_atraso,
        TRIM(CAST(num_ctrl_envio AS STRING)) AS num_ctrl_envio,
        total,
        ajuste,
        atraso,
        sla,
        acao,
        responsavel,
        owner,
        follow_up_status
    FROM
        `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_QUEBRA_DE_SIGILO_CONTROLE_ERROS_FATO`
)

SELECT * FROM CASOS_ERROS;
