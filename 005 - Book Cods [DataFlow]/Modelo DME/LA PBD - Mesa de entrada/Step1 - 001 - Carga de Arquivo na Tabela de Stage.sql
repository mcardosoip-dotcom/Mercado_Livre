LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_VISTA_ENTRADAS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_vista_entradas.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_HIST_CASOS_X_ESTADO
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_dw_hist_casos_x_estado.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_VISTA_CANTIDAD_CASOS_USUARIOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_vista_cantidad_casos_usuarios.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_VISTA_USUARIOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_vista_usuarios.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_V_METRICAS_QA
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_v_metricas_qa.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_METRICAS_BIG_QUERY
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_metricas_big_query.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_TAB_ENTRADAS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_tab_entradas.parquet']
  );

LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_TAB_ESTADOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_estados.parquet']
  );

  LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_TIPO_DOCUMENTOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_tipo_documentos.parquet']
  );


    LOAD DATA OVERWRITE STG.INPUT_MESA_BASE_ENTRADA_ESTADOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Mesa_de_entrada/Mesa_entrada_entradas_estados.parquet']
  );
