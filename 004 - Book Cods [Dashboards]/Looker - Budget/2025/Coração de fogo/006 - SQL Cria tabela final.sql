CREATE OR REPLACE TABLE `<ENV>.STG.BUDGET_CORACAO_FINAL` AS

WITH TABELA_REAL AS (
  SELECT
    pais,
    Visao,
    Objeto,
    Anomes,
    Ano,

    -- INT
    IFNULL(SAFE_CAST(NULLIF(Entradas_JEC, '') AS INT64), 0) AS Entradas_JEC,
    IFNULL(SAFE_CAST(NULLIF(Entradas_JC, '') AS INT64), 0) AS Entradas_JC,
    IFNULL(SAFE_CAST(NULLIF(Entradas_Procon, '') AS INT64), 0) AS Entradas_Procon,
    IFNULL(SAFE_CAST(NULLIF(Total_Entradas, '') AS INT64), 0) AS Total_Entradas,

    IFNULL(SAFE_CAST(NULLIF(Encerrados_JEC, '') AS INT64), 0) AS Encerrados_JEC,
    IFNULL(SAFE_CAST(NULLIF(Encerrados_JC, '') AS INT64), 0) AS Encerrados_JC,
    IFNULL(SAFE_CAST(NULLIF(Encerrados_Procon, '') AS INT64), 0) AS Encerrados_Procon,
    IFNULL(SAFE_CAST(NULLIF(Total_Encerrados, '') AS INT64), 0) AS Total_Encerrados,

    IFNULL(SAFE_CAST(NULLIF(JEC_Qty_Acordo, '') AS INT64), 0) AS JEC_Qty_Acordo,
    IFNULL(SAFE_CAST(NULLIF(JC_Qty_Acordo, '') AS INT64), 0) AS JC_Qty_Acordo,
    IFNULL(SAFE_CAST(NULLIF(Procon_Qty_Acordo, '') AS INT64), 0) AS Procon_Qty_Acordo,
    IFNULL(SAFE_CAST(NULLIF(Total_Qty_Acordo, '') AS INT64), 0) AS Total_Qty_Acordo,

    IFNULL(SAFE_CAST(NULLIF(JEC_Qty_Ganhamos, '') AS INT64), 0) AS JEC_Qty_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(JC_Qty_Ganhamos, '') AS INT64), 0) AS JC_Qty_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(Procon_Qty_Ganhamos, '') AS INT64), 0) AS Procon_Qty_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(Total_Qty_Ganhamos, '') AS INT64), 0) AS Total_Qty_Ganhamos,

    IFNULL(SAFE_CAST(NULLIF(JEC_Qty_Perdemos, '') AS INT64), 0) AS JEC_Qty_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(JC_Qty_Perdemos, '') AS INT64), 0) AS JC_Qty_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(Procon_Qty_Perdemos, '') AS INT64), 0) AS Procon_Qty_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(Total_Qty_Perdemos, '') AS INT64), 0) AS Total_Qty_Perdemos,

    IFNULL(SAFE_CAST(NULLIF(JEC_Qty_Desistido, '') AS INT64), 0) AS JEC_Qty_Desistido,
    IFNULL(SAFE_CAST(NULLIF(JC_Qty_Desistido, '') AS INT64), 0) AS JC_Qty_Desistido,
    IFNULL(SAFE_CAST(NULLIF(Procon_Qty_Desistido, '') AS INT64), 0) AS Procon_Qty_Desistido,
    IFNULL(SAFE_CAST(NULLIF(Total_Qty_Desistido, '') AS INT64), 0) AS Total_Qty_Desistido,

    IFNULL(SAFE_CAST(NULLIF(JEC_Qty_Outros, '') AS INT64), 0) AS JEC_Qty_Outros,
    IFNULL(SAFE_CAST(NULLIF(JC_Qty_Outros, '') AS INT64), 0) AS JC_Qty_Outros,
    IFNULL(SAFE_CAST(NULLIF(Procon_Qty_Outros, '') AS INT64), 0) AS Procon_Qty_Outros,
    IFNULL(SAFE_CAST(NULLIF(Total_Qty_Outros, '') AS INT64), 0) AS Total_Qty_Outros,

    -- FLOAT
    IFNULL(SAFE_CAST(NULLIF(JEC_TM_Acordo, '') AS FLOAT64), 0) AS JEC_TM_Acordo,
    IFNULL(SAFE_CAST(NULLIF(JC_TM_Acordo, '') AS FLOAT64), 0) AS JC_TM_Acordo,
    IFNULL(SAFE_CAST(NULLIF(Procon_TM_Acordo, '') AS FLOAT64), 0) AS Procon_TM_Acordo,
    IFNULL(SAFE_CAST(NULLIF(TM_Acordo, '') AS FLOAT64), 0) AS TM_Acordo,

    IFNULL(SAFE_CAST(NULLIF(JEC_TM_Ganhamos, '') AS FLOAT64), 0) AS JEC_TM_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(JC_TM_Ganhamos, '') AS FLOAT64), 0) AS JC_TM_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(Procon_TM_Ganhamos, '') AS FLOAT64), 0) AS Procon_TM_Ganhamos,
    IFNULL(SAFE_CAST(NULLIF(TM_Ganhamos, '') AS FLOAT64), 0) AS TM_Ganhamos,

    IFNULL(SAFE_CAST(NULLIF(JEC_TM_Perdemos, '') AS FLOAT64), 0) AS JEC_TM_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(JC_TM_Perdemos, '') AS FLOAT64), 0) AS JC_TM_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(Procon_TM_Perdemos, '') AS FLOAT64), 0) AS Procon_TM_Perdemos,
    IFNULL(SAFE_CAST(NULLIF(TM_Perdemos, '') AS FLOAT64), 0) AS TM_Perdemos,

    IFNULL(SAFE_CAST(NULLIF(JEC_TM_Desistido, '') AS FLOAT64), 0) AS JEC_TM_Desistido,
    IFNULL(SAFE_CAST(NULLIF(JC_TM_Desistido, '') AS FLOAT64), 0) AS JC_TM_Desistido,
    IFNULL(SAFE_CAST(NULLIF(Procon_TM_Desistido, '') AS FLOAT64), 0) AS Procon_TM_Desistido,
    IFNULL(SAFE_CAST(NULLIF(TM_Desistido, '') AS FLOAT64), 0) AS TM_Desistido,

    IFNULL(SAFE_CAST(NULLIF(JEC_TM_Outros, '') AS FLOAT64), 0) AS JEC_TM_Outros,
    IFNULL(SAFE_CAST(NULLIF(JC_TM_Outros, '') AS FLOAT64), 0) AS JC_TM_Outros,
    IFNULL(SAFE_CAST(NULLIF(Procon_TM_Outros, '') AS FLOAT64), 0) AS Procon_TM_Outros,
    IFNULL(SAFE_CAST(NULLIF(TM_Outros, '') AS FLOAT64), 0) AS TM_Outros

  FROM `<ENV>.STG.BUDGET_CORACAO_TEMP`
  WHERE Visao = 'Real'
),

TABELA_BUDGET AS (
  SELECT
    pais,
    Visao,
    Objeto,
    Anomes,
    Ano,

    -- Campos tratados com REPLACE para casos com vírgula decimal
    -- INT (convertendo de string → float → int)
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Entradas_JEC, ',', '.') AS FLOAT64)) AS INT64), 0) AS Entradas_JEC,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Entradas_JC, ',', '.') AS FLOAT64)) AS INT64), 0) AS Entradas_JC,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Entradas_Procon, ',', '.') AS FLOAT64)) AS INT64), 0) AS Entradas_Procon,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Entradas, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Entradas,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Encerrados_JEC, ',', '.') AS FLOAT64)) AS INT64), 0) AS Encerrados_JEC,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Encerrados_JC, ',', '.') AS FLOAT64)) AS INT64), 0) AS Encerrados_JC,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Encerrados_Procon, ',', '.') AS FLOAT64)) AS INT64), 0) AS Encerrados_Procon,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Encerrados, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Encerrados,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_Qty_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_Qty_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_Qty_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_Qty_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_Qty_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_Qty_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Qty_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Qty_Acordo,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_Qty_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_Qty_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_Qty_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_Qty_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_Qty_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_Qty_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Qty_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Qty_Ganhamos,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_Qty_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_Qty_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_Qty_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_Qty_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_Qty_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_Qty_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Qty_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Qty_Perdemos,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_Qty_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_Qty_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_Qty_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_Qty_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_Qty_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_Qty_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Qty_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Qty_Desistido,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_Qty_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_Qty_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_Qty_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_Qty_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_Qty_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_Qty_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Total_Qty_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS Total_Qty_Outros,

    -- FLOAT (mantendo como INT64 com FLOOR para compatibilidade com TABELA_REAL)
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_TM_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_TM_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_TM_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_TM_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_TM_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_TM_Acordo,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(TM_Acordo, ',', '.') AS FLOAT64)) AS INT64), 0) AS TM_Acordo,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_TM_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_TM_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_TM_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_TM_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_TM_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_TM_Ganhamos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(TM_Ganhamos, ',', '.') AS FLOAT64)) AS INT64), 0) AS TM_Ganhamos,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_TM_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_TM_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_TM_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_TM_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_TM_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_TM_Perdemos,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(TM_Perdemos, ',', '.') AS FLOAT64)) AS INT64), 0) AS TM_Perdemos,


    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_TM_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_TM_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_TM_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_TM_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_TM_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_TM_Desistido,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(TM_Desistido, ',', '.') AS FLOAT64)) AS INT64), 0) AS TM_Desistido,

    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JEC_TM_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS JEC_TM_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(JC_TM_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS JC_TM_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(Procon_TM_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS Procon_TM_Outros,
    IFNULL(SAFE_CAST(FLOOR(SAFE_CAST(REPLACE(TM_Outros, ',', '.') AS FLOAT64)) AS INT64), 0) AS TM_Outros

  FROM `<ENV>.STG.BUDGET_CORACAO_TEMP`
  WHERE Visao = 'Budget'
)

SELECT * FROM TABELA_REAL
UNION ALL
SELECT * FROM TABELA_BUDGET;
