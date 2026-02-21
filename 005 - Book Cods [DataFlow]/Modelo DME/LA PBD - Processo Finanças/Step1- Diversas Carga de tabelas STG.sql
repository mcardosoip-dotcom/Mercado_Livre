-- ================================================
-- PAGAMENTOS
-- ================================================

LOAD DATA OVERWRITE STG.Database_Pagamentos_Brasil
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Pagamentos_Brasil.parquet']
  );

LOAD DATA OVERWRITE STG.Database_Pagamentos_Hispanos
FROM
  FILES ( 
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Pagamentos_Hispanos.parquet']
  );

-- ================================================
-- HONORARIOS
-- ================================================

LOAD DATA OVERWRITE STG.Database_Honorarios_Brasil
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Honorarios_Brasil.parquet']
  );

LOAD DATA OVERWRITE STG.Database_Honorarios_Hispanos
FROM
  FILES ( 
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Honorarios_Hispanos.parquet']
  );

-- ================================================
-- CONTINGENCIAS
-- ================================================

LOAD DATA OVERWRITE STG.Database_Contingencias_Brasil
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Contingencias_Brasil.parquet']
  );

LOAD DATA OVERWRITE STG.Database_Contingencias_Hispanos
FROM
  FILES ( 
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Database_Contingencias_Hispanos.parquet']
  );