-- ============================
-- LOAD: DIM_1_DIMENSAO_ADVOGADOS
-- ============================
LOAD DATA OVERWRITE STG.DIM_1_DIMENSAO_ADVOGADOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_1_Dimensao_Advogados.parquet']
);

-- ============================
-- LOAD: DIM_2_DIMENSAO_DE_PARA_ESCRITORIOS
-- ============================
LOAD DATA OVERWRITE STG.DIM_2_DIMENSAO_DE_PARA_ESCRITORIOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_2_Dimensao_De_Para_Escritorios.parquet']
);

-- ============================
-- LOAD: DIM_3_DIMENSAO_EMPRESAS
-- ============================
LOAD DATA OVERWRITE STG.DIM_3_DIMENSAO_EMPRESAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_3_Dimensao_Empresas.parquet']
);

-- ============================
-- LOAD: DIM_4_DIMENSAO_ESCRITORIOS
-- ============================
LOAD DATA OVERWRITE STG.DIM_4_DIMENSAO_ESCRITORIOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_4_Dimensao_Escritorios.parquet']
);

-- ============================
-- LOAD: DIM_5_DIMENSAO_ESFERAS
-- ============================
LOAD DATA OVERWRITE STG.DIM_5_DIMENSAO_ESFERAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_5_Dimensao_Esferas.parquet']
);

-- ============================
-- LOAD: DIM_6_DIMENSAO_ESTADOS_UF
-- ============================
LOAD DATA OVERWRITE STG.DIM_6_DIMENSAO_ESTADOS_UF
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_6_Dimensao_Estados_UF.parquet']
);

-- ============================
-- LOAD: DIM_7_DIMENSAO_FASES
-- ============================
LOAD DATA OVERWRITE STG.DIM_7_DIMENSAO_FASES
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_7_Dimensao_Fases.parquet']
);

-- ============================
-- LOAD: DIM_8_DIMENSAO_GRUPO_ADVOGADOS_DR
-- ============================
LOAD DATA OVERWRITE STG.DIM_8_DIMENSAO_GRUPO_ADVOGADOS_DR
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_8_Dimensao_Grupo_Advogados_DR.parquet']
);

-- ============================
-- LOAD: DIM_9_DIMENSAO_MES
-- ============================
LOAD DATA OVERWRITE STG.DIM_9_DIMENSAO_MES
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_9_Dimensao_Mes.parquet']
);

-- ============================
-- LOAD: DIM_10_DIMENSAO_OBJETOS
-- ============================
LOAD DATA OVERWRITE STG.DIM_10_DIMENSAO_OBJETOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_10_Dimensao_Objetos.parquet']
);

-- ============================
-- LOAD: DIM_12_DIMENSAO_PARCEIROS
-- ============================
LOAD DATA OVERWRITE STG.DIM_12_DIMENSAO_PARCEIROS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_12_Dimensao_Parceiros.parquet']
);

-- ============================
-- LOAD: DIM_13_DIMENSAO_REGIAO
-- ============================
LOAD DATA OVERWRITE STG.DIM_13_DIMENSAO_REGIAO
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_13_Dimensao_Regiao.parquet']
);

-- ============================
-- LOAD: DIM_14_DIMENSAO_FASES_REVISADA
-- ============================
LOAD DATA OVERWRITE STG.DIM_14_DIMENSAO_FASES_REVISADA
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_14_Dimensao_Fases_Revisada.parquet']
);

-- ============================
-- LOAD: DIM_15_DIMENSAO_WORKFLOW
-- ============================
LOAD DATA OVERWRITE STG.DIM_15_DIMENSAO_WORKFLOW
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_15_Dimensao_Workflow.parquet']
);

-- ============================
-- LOAD: DIM_16_DIMENSAO_MULTA
-- ============================
LOAD DATA OVERWRITE STG.DIM_16_DIMENSAO_MULTA
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_16_Dimensao_Multa.parquet']
);

-- ============================
-- LOAD: DIM_17_DIMENSAO_SIGLA_PAIS
-- ============================
LOAD DATA OVERWRITE STG.DIM_17_DIMENSAO_SIGLA_PAIS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_17_Dimensao_Sigla_Pais.parquet']
);

-- ============================
-- LOAD: DIM_10_DIMENSAO_OBJETOS_2
-- ============================
LOAD DATA OVERWRITE STG.DIM_10_DIMENSAO_OBJETOS_2
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_10_Dimensao_Objetos_2.parquet']
);

-- ============================
-- LOAD: DIM_36_TPN_E_SI
-- ============================
LOAD DATA OVERWRITE STG.DIM_36_TPN_E_SI
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Dimensoes/Dim_36_TPN_e_SI.parquet']
);
