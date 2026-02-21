CREATE OR REPLACE TABLE `<ENV>.STG.BUDGET_ACTUAL_MEX` AS

-- Dados INCOMING e OUTGOING - México
-- Usa SAFE.PARSE_DATE para evitar erro "Failed to parse input string None" quando DATA_REGISTRADO ou data_de_encerramento contêm "None" ou valor inválido
WITH Database_Hispanos AS (
    SELECT
        pais,
        SAFE.PARSE_DATE('%d/%m/%Y', DATA_REGISTRADO) AS DATA_REGISTRADO,
        SAFE.PARSE_DATE('%d/%m/%Y', data_de_encerramento) AS DATA_DE_ENCERRAMENTO,
        AREA_DO_DIREITO,
        SUB_AREA_DO_DIREITO,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        FASE_DESFECHO,
        FORMAT_DATE('%Y%m', SAFE.PARSE_DATE('%d/%m/%Y', DATA_REGISTRADO)) AS Anomes,
        VALOR_DO_RISCO
    FROM
        `<ENV>.STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS`
    WHERE
        pais = 'México'
),

-- Entradas (INCOMING)
Incoming_MEX AS (
    SELECT
        pais,
        Anomes,
        'NA' AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Total_Entradas
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_REGISTRADO >= DATE '2025-01-01'
        AND DATA_REGISTRADO < CURRENT_DATE()
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Saídas (OUTGOING)
Outgoing_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Encerrados
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Acordos
Acordos_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Qty_Acordo,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS TM_Acordo
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
        AND FASE_DESFECHO = "Acordo"
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Ganhamos
Ganhamos_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Qty_Ganhamos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS TM_Ganhamos
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
        AND FASE_DESFECHO = "Ganhamos"
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Perdemos
Perdemos_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Qty_Perdemos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS TM_Perdemos
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
        AND FASE_DESFECHO = "Perdemos"
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Desistido
Desistido_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Qty_Desistido,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS TM_Desistido
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
        AND FASE_DESFECHO = "Desistido"
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

-- Outros
Outros_MEX AS (
    SELECT
        pais, Anomes, 'NA' AS PROCEDIMENTO_JUDICIAL, objeto_tratado,
        COUNT(*) AS Total_Qty_Outros,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS TM_Outros
    FROM Database_Hispanos
    WHERE
        AREA_DO_DIREITO = "CORP - Consumidor"
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
        AND FASE_DESFECHO NOT IN ("Desistido", "Ganhamos", "Acordo", "Perdemos")
    GROUP BY pais, Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

Matrix AS (
    SELECT DISTINCT pais, objeto_tratado, Anomes
    FROM Database_Hispanos
    WHERE (Anomes LIKE '2025%' OR Anomes LIKE '2026%') AND objeto_tratado IS NOT NULL
)

-- Resultado final somente México
SELECT
    a.pais,
    'Real' AS Visao,
    a.objeto_tratado AS Objeto,
    a.Anomes,
    SUBSTR(a.Anomes, 1, 4) AS Ano,
    b.Total_Entradas,
    c.Total_Encerrados,
    d.Total_Qty_Acordo,
    d.TM_Acordo,
    e.Total_Qty_Ganhamos,
    e.TM_Ganhamos,
    f.Total_Qty_Perdemos,
    f.TM_Perdemos,
    g.Total_Qty_Desistido,
    g.TM_Desistido,
    h.Total_Qty_Outros,
    h.TM_Outros
FROM Matrix AS a
LEFT JOIN Incoming_MEX AS b ON a.Anomes = b.Anomes AND a.objeto_tratado = b.objeto_tratado AND a.pais = b.pais
LEFT JOIN Outgoing_MEX AS c ON a.Anomes = c.Anomes AND a.objeto_tratado = c.objeto_tratado AND a.pais = c.pais
LEFT JOIN Acordos_MEX AS d ON a.Anomes = d.Anomes AND a.objeto_tratado = d.objeto_tratado AND a.pais = d.pais
LEFT JOIN Ganhamos_MEX AS e ON a.Anomes = e.Anomes AND a.objeto_tratado = e.objeto_tratado AND a.pais = e.pais
LEFT JOIN Perdemos_MEX AS f ON a.Anomes = f.Anomes AND a.objeto_tratado = f.objeto_tratado AND a.pais = f.pais
LEFT JOIN Desistido_MEX AS g ON a.Anomes = g.Anomes AND a.objeto_tratado = g.objeto_tratado AND a.pais = g.pais
LEFT JOIN Outros_MEX AS h ON a.Anomes = h.Anomes AND a.objeto_tratado = h.objeto_tratado AND a.pais = h.pais;
