LOAD DATA OVERWRITE STG.QUEBRA_DE_SIGILO_CONTROLE
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Quebra_Sigilo/Quebra_de_sigilo_controle.parquet']
  );

LOAD DATA OVERWRITE STG.CONSUMIDORGOV
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/ConsumidorGov/Base_GOV_Consolidada.parquet']
  );

LOAD DATA OVERWRITE STG.CLM_CONTROL_DE_CONTRATOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/CLM_control_de_contratos.parquet']
  );

LOAD DATA OVERWRITE STG.CLM_METRICAS_DE_CONTRATOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/CLM_metricas_de_contrato.parquet']
  );

LOAD DATA OVERWRITE STG.CLM_METRICAS_FLUJOS_ACTIVOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/CLM_metricas_de_flujos_activos.parquet']
  );
  
  
