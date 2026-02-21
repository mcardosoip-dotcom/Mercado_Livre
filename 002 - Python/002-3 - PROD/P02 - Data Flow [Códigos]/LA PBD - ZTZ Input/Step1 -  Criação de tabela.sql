CREATE OR REPLACE TABLE `<ENV>.STG.ZTZ_coleta_historico` (
    DADO_INPUT STRING,
    CUS_CUST_DOC_NUMBER STRING,
    CUS_NICKNAME STRING,
    AVAILABLE_AMOUNT FLOAT64, -- Mantido como FLOAT64 para o valor original
    ASSET_MGMT_STATUS STRING,
    ASSET_MGMT_PRODUCT_ID STRING,
    TIPO_FONDO_INVERTIDO STRING, -- Nova coluna adicionada
    AVAILABLE_AMOUNT_AJUSTADO STRING -- Nova coluna adicionada (como STRING, conforme sua lógica)
);
