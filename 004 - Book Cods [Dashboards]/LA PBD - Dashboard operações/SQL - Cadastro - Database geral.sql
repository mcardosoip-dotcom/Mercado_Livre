WITH Fonte AS (
  SELECT
    e.PROCESSO_ID,
    e.PAIS,
    e.NUMERO_DO_PROCESSO,
    e.STATUS,

    -- Tratamento da área do direito
    CASE
      WHEN e.AREA_DO_DIREITO = 'CORP - Civil' THEN 'Cível'
      WHEN e.AREA_DO_DIREITO = 'CORP - Consumidor' THEN 'Consumidor'
      WHEN e.AREA_DO_DIREITO = 'CORP - Criminal' THEN 'Criminal'
      WHEN e.AREA_DO_DIREITO = 'CORP - Laboral' THEN 'Trabalhista'
      ELSE e.AREA_DO_DIREITO
    END AS AREA_DO_DIREITO,

    e.SUB_AREA_DO_DIREITO,
    e.PROCESSO_ESTADO,
    SAFE.PARSE_DATE('%d/%m/%Y', e.DATA_REGISTRADO) AS DATA_REGISTRADO,
    SAFE.PARSE_DATE('%d/%m/%Y', e.DATA_DE_ENCERRAMENTO) AS DATA_DE_ENCERRAMENTO,
    e.OBJETO_TRATADO,
    e.UNIDADE_TRATADA,
    e.EMPRESA_TRATADA,
    SAFE.PARSE_DATE('%d/%m/%Y', e.DATA_DE_CITACAO) AS DATA_DE_CITACAO,
    e.MODALIDADE,  -- <<< campo incluído

    CASE
      WHEN e.PAIS = 'Brasil' THEN
        CASE
          WHEN e.PROCESSO_ESTADO IN ('MG','RJ','SP') THEN 'Finch'
          ELSE 'Enlighten'
        END
      ELSE 'SEGEM'
    END AS Parceiro_Cadastro,

    e.UNIDADE_TRATADA AS Unidade_de_negocio,

    DATE_DIFF(
      SAFE.PARSE_DATE('%d/%m/%Y', e.DATA_REGISTRADO),
      SAFE.PARSE_DATE('%d/%m/%Y', e.DATA_DE_CITACAO),
      DAY
    ) AS diff_days

  FROM
    `pdme000426-c1s7scatwm0-furyid.STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS` AS e
)

SELECT
  PROCESSO_ID,
  PAIS,
  NUMERO_DO_PROCESSO,
  STATUS,
  AREA_DO_DIREITO,
  SUB_AREA_DO_DIREITO,
  PROCESSO_ESTADO,
  DATA_REGISTRADO,
  DATA_DE_ENCERRAMENTO,
  OBJETO_TRATADO,
  UNIDADE_TRATADA,
  EMPRESA_TRATADA,
  DATA_DE_CITACAO,
  MODALIDADE,  -- <<< campo incluído
  Parceiro_Cadastro,
  Unidade_de_negocio,
  CASE
    WHEN diff_days IS NULL THEN 0
    WHEN diff_days < 0     THEN 0
    ELSE diff_days
  END AS SLA,
  COALESCE(GREATEST(diff_days, 0), 0) AS `TMC - Citação e Registrado`
FROM
  Fonte;
