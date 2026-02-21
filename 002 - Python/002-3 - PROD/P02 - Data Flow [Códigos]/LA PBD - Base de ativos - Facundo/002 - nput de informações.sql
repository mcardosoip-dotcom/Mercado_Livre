-- 1. Comando para limpar (truncate) a tabela de destino (LK)
TRUNCATE TABLE `<ENV>.TBL.LK_BASE_PROCESSOS_ELAW_ATIVOS`;

-- 2. Comando para carregar a tabela LK com os dados da BASE
INSERT INTO `<ENV>.TBL.LK_BASE_PROCESSOS_ELAW_ATIVOS` (
    Processo_id,
    Pais,
    Status_pro,
    Area_do_direito,
    Sub_area_do_direito,
    Cust_id_autor,
    Data_registrado,
    Data_de_encerramento,
    Data_update,
    AUD_INS_DTTM,
    AUD_UPD_DTTM	
)
SELECT
    Processo_id,
    Pais,
    Status_pro,
    Area_do_direito,
    Sub_area_do_direito,
    Cust_id_autor,
    Data_registrado,
    Data_de_encerramento,
    Data_update,
    CURRENT_DATETIME() AS AUD_INS_DTTM,
    CURRENT_DATETIME() AS AUD_UPD_DTTM
FROM
    `<ENV>.STG.BASE_PROCESSOS_ELAW_ATIVOS`;