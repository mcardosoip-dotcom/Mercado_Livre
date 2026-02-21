CREATE OR REPLACE TABLE `<ENV>.STG.BUDGET_ACTUAL_BRA` AS


-- Dados INCOMING e OUTGOING Brasil
WITH Database_brasil AS (
    SELECT
        pais,
        PARSE_DATE('%d/%m/%Y', DATA_REGISTRADO) AS DATA_REGISTRADO,
        PARSE_DATE('%d/%m/%Y', data_de_encerramento) AS DATA_DE_ENCERRAMENTO,
        AREA_DO_DIREITO,
        SUB_AREA_DO_DIREITO,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        FASE_DESFECHO,
        FORMAT_DATE('%Y%m', PARSE_DATE('%d/%m/%Y', DATA_REGISTRADO)) AS Anomes_registrado, -- Renomeado
        FORMAT_DATE('%Y%m', PARSE_DATE('%d/%m/%Y', data_de_encerramento)) AS Anomes_encerrado, -- Novo campo
        VALOR_DO_RISCO
    FROM
        `<ENV>.STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS`
    WHERE
        pais = "Brasil"
),

-- Entradas (INCOMING)
Incoming_JEC AS (
    SELECT
        Anomes_registrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Entradas_JEC
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND DATA_REGISTRADO >= DATE '2025-01-01'
        AND DATA_REGISTRADO < CURRENT_DATE()
    GROUP BY Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

Incoming_JC AS (
    SELECT
        Anomes_registrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Entradas_JC
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND DATA_REGISTRADO >= DATE '2025-01-01'
        AND DATA_REGISTRADO < CURRENT_DATE()
    GROUP BY Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

Incoming_Procon AS (
    SELECT
        Anomes_registrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Entradas_Procon
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_REGISTRADO >= DATE '2025-01-01'
        AND DATA_REGISTRADO < CURRENT_DATE()
    GROUP BY Anomes, objeto_tratado
),

-- Saídas (OUTGOING)
Outgoing_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Encerrados_JEC
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO =  "Consumidor"
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

Outgoing_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Encerrados_JC
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY Anomes, PROCEDIMENTO_JUDICIAL, objeto_tratado
),

Outgoing_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Encerrados_Procon
    FROM Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY Anomes, objeto_tratado
),

-- Ticket Médio de ACORDOS
TM_Acordo_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JEC_Qty_Acordo,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JEC_TM_Acordo
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Acordo"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Acordo_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JC_Qty_Acordo,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JC_TM_Acordo
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Acordo"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Acordo_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Procon_Qty_Acordo,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS Procon_TM_Acordo
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND FASE_DESFECHO = "Acordo"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        objeto_tratado
),

-- Ticket Médio de GANHAMOS
TM_Ganhamos_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JEC_Qty_Ganhamos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JEC_TM_Ganhamos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Ganhamos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Ganhamos_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JC_Qty_Ganhamos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JC_TM_Ganhamos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Ganhamos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Ganhamos_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Procon_Qty_Ganhamos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS Procon_TM_Ganhamos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND FASE_DESFECHO = "Ganhamos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        objeto_tratado
),

-- Ticket Médio de PERDEMOS
TM_Perdemos_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JEC_Qty_Perdemos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JEC_TM_Perdemos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Perdemos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Perdemos_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JC_Qty_Perdemos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JC_TM_Perdemos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Perdemos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Perdemos_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Procon_Qty_Perdemos,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS Procon_TM_Perdemos
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND FASE_DESFECHO = "Perdemos"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        objeto_tratado
),


-- Ticket Médio de DESISTIDO
TM_Desistido_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JEC_Qty_Desistido,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JEC_TM_Desistido
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Desistido"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Desistido_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JC_Qty_Desistido,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JC_TM_Desistido
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO = "Desistido"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

TM_Desistido_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Procon_Qty_Desistido,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS Procon_TM_Desistido
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND FASE_DESFECHO = "Desistido"
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        objeto_tratado
),

-- Ticket Médio de OUTROS
Qty_Outros_JEC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JEC_Qty_Outros,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JEC_TM_Outros
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JEC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO NOT IN ("Desistido", "Ganhamos", "Acordo", "Perdemos")
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

Qty_Outros_JC AS (
    SELECT
        Anomes_encerrado as Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS JC_Qty_Outros,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS JC_TM_Outros
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL = "JC"
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO = "Judicial"
        AND FASE_DESFECHO NOT IN ("Desistido", "Ganhamos", "Acordo", "Perdemos")
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        PROCEDIMENTO_JUDICIAL,
        objeto_tratado
),

Qty_Outros_Procon AS (
    SELECT
        Anomes_encerrado as Anomes,
        "Procon" AS PROCEDIMENTO_JUDICIAL,
        objeto_tratado,
        COUNT(*) AS Procon_Qty_Outros,
        AVG(SAFE_CAST(VALOR_DO_RISCO AS FLOAT64)) AS Procon_TM_Outros
    FROM
        Database_brasil
    WHERE
        PROCEDIMENTO_JUDICIAL IS NULL
        AND AREA_DO_DIREITO IN ("Consumidor", "Cível")
        AND SUB_AREA_DO_DIREITO <> "Judicial"
        AND FASE_DESFECHO NOT IN ("Desistido", "Ganhamos", "Acordo", "Perdemos")
        AND DATA_DE_ENCERRAMENTO >= DATE '2025-01-01'
        AND DATA_DE_ENCERRAMENTO < CURRENT_DATE()
    GROUP BY
        Anomes,
        objeto_tratado
),

Matrix AS
(
SELECT  distinct
        pais
        ,objeto_tratado
        ,Anomes_registrado as Anomes
        FROM Database_brasil
        WHERE (Anomes_registrado LIKE '2025%' OR Anomes_registrado LIKE '2026%')
        AND objeto_tratado IS NOT NULL

)

-- Resultado final completo
SELECT
    a.pais,
    'Real' AS Visao,
    a.objeto_tratado AS Objeto,
    a.Anomes,
    SUBSTR(a.Anomes, 1, 4) AS Ano,

    -- Entradas
    IFNULL(b.Entradas_JEC, 0) AS Entradas_JEC,
    IFNULL(c.Entradas_JC, 0) AS Entradas_JC,
    IFNULL(d.Entradas_Procon, 0) AS Entradas_Procon,

    -- Total Entradas
    SAFE_ADD(SAFE_ADD(IFNULL(b.Entradas_JEC, 0), IFNULL(c.Entradas_JC, 0)), IFNULL(d.Entradas_Procon, 0)) AS Total_Entradas,

    -- Encerrados
    IFNULL(e.Encerrados_JEC, 0) AS Encerrados_JEC,
    IFNULL(f.Encerrados_JC, 0) AS Encerrados_JC,
    IFNULL(g.Encerrados_Procon, 0) AS Encerrados_Procon,

    -- Total Encerrados
    SAFE_ADD(SAFE_ADD(IFNULL(e.Encerrados_JEC, 0), IFNULL(f.Encerrados_JC, 0)), IFNULL(g.Encerrados_Procon, 0)) AS Total_Encerrados,

    -- Quantidades: Acordo
    IFNULL(h.JEC_Qty_Acordo, 0) AS JEC_Qty_Acordo,
    IFNULL(i.JC_Qty_Acordo, 0) AS JC_Qty_Acordo,
    IFNULL(j.Procon_Qty_Acordo, 0) AS Procon_Qty_Acordo,
    SAFE_ADD(SAFE_ADD(IFNULL(h.JEC_Qty_Acordo, 0), IFNULL(i.JC_Qty_Acordo, 0)), IFNULL(j.Procon_Qty_Acordo, 0)) AS Total_Qty_Acordo,

    -- Quantidades: Ganhamos
    IFNULL(k.JEC_Qty_Ganhamos, 0) AS JEC_Qty_Ganhamos,
    IFNULL(l.JC_Qty_Ganhamos, 0) AS JC_Qty_Ganhamos,
    IFNULL(m.Procon_Qty_Ganhamos, 0) AS Procon_Qty_Ganhamos,
    SAFE_ADD(SAFE_ADD(IFNULL(k.JEC_Qty_Ganhamos, 0), IFNULL(l.JC_Qty_Ganhamos, 0)), IFNULL(m.Procon_Qty_Ganhamos, 0)) AS Total_Qty_Ganhamos,

    -- Quantidades: Perdemos
    IFNULL(n.JEC_Qty_Perdemos, 0) AS JEC_Qty_Perdemos,
    IFNULL(o.JC_Qty_Perdemos, 0) AS JC_Qty_Perdemos,
    IFNULL(p.Procon_Qty_Perdemos, 0) AS Procon_Qty_Perdemos,
    SAFE_ADD(SAFE_ADD(IFNULL(n.JEC_Qty_Perdemos, 0), IFNULL(o.JC_Qty_Perdemos, 0)), IFNULL(p.Procon_Qty_Perdemos, 0)) AS Total_Qty_Perdemos,

    -- Quantidades: Desistido
    IFNULL(q.JEC_Qty_Desistido, 0) AS JEC_Qty_Desistido,
    IFNULL(r.JC_Qty_Desistido, 0) AS JC_Qty_Desistido,
    IFNULL(s.Procon_Qty_Desistido, 0) AS Procon_Qty_Desistido,
    SAFE_ADD(SAFE_ADD(IFNULL(q.JEC_Qty_Desistido, 0), IFNULL(r.JC_Qty_Desistido, 0)), IFNULL(s.Procon_Qty_Desistido, 0)) AS Total_Qty_Desistido,

    -- Quantidades: Outros
    IFNULL(t.JEC_Qty_Outros, 0) AS JEC_Qty_Outros,
    IFNULL(u.JC_Qty_Outros, 0) AS JC_Qty_Outros,
    IFNULL(v.Procon_Qty_Outros, 0) AS Procon_Qty_Outros,
    SAFE_ADD(SAFE_ADD(IFNULL(t.JEC_Qty_Outros, 0), IFNULL(u.JC_Qty_Outros, 0)), IFNULL(v.Procon_Qty_Outros, 0)) AS Total_Qty_Outros,

    -- Valores Médios: Acordo
    IFNULL(h.JEC_TM_Acordo, 0) AS JEC_TM_Acordo,
    IFNULL(i.JC_TM_Acordo, 0) AS JC_TM_Acordo,
    IFNULL(j.Procon_TM_Acordo, 0) AS Procon_TM_Acordo,

    -- Valores Médios: Ganhamos
    IFNULL(k.JEC_TM_Ganhamos, 0) AS JEC_TM_Ganhamos,
    IFNULL(l.JC_TM_Ganhamos, 0) AS JC_TM_Ganhamos,
    IFNULL(m.Procon_TM_Ganhamos, 0) AS Procon_TM_Ganhamos,

    -- Valores Médios: Perdemos
    IFNULL(n.JEC_TM_Perdemos, 0) AS JEC_TM_Perdemos,
    IFNULL(o.JC_TM_Perdemos, 0) AS JC_TM_Perdemos,
    IFNULL(p.Procon_TM_Perdemos, 0) AS Procon_TM_Perdemos,

    -- Valores Médios: Desistido
    IFNULL(q.JEC_TM_Desistido, 0) AS JEC_TM_Desistido,
    IFNULL(r.JC_TM_Desistido, 0) AS JC_TM_Desistido,
    IFNULL(s.Procon_TM_Desistido, 0) AS Procon_TM_Desistido,

    -- Valores Médios: Outros
    IFNULL(t.JEC_TM_Outros, 0) AS JEC_TM_Outros,
    IFNULL(u.JC_TM_Outros, 0) AS JC_TM_Outros,
    IFNULL(v.Procon_TM_Outros, 0) AS Procon_TM_Outros

FROM Matrix AS a
LEFT JOIN Incoming_JEC AS b ON a.Anomes = b.Anomes AND a.objeto_tratado = b.objeto_tratado
LEFT JOIN Incoming_JC AS c ON a.Anomes = c.Anomes AND a.objeto_tratado = c.objeto_tratado
LEFT JOIN Incoming_Procon AS d ON a.Anomes = d.Anomes AND a.objeto_tratado = d.objeto_tratado

LEFT JOIN Outgoing_JEC AS e ON a.Anomes = e.Anomes AND a.objeto_tratado = e.objeto_tratado
LEFT JOIN Outgoing_JC AS f ON a.Anomes = f.Anomes AND a.objeto_tratado = f.objeto_tratado
LEFT JOIN Outgoing_Procon AS g ON a.Anomes = g.Anomes AND a.objeto_tratado = g.objeto_tratado

LEFT JOIN TM_Acordo_JEC AS h ON a.Anomes = h.Anomes AND a.objeto_tratado = h.objeto_tratado
LEFT JOIN TM_Acordo_JC AS i ON a.Anomes = i.Anomes AND a.objeto_tratado = i.objeto_tratado
LEFT JOIN TM_Acordo_Procon AS j ON a.Anomes = j.Anomes AND a.objeto_tratado = j.objeto_tratado

LEFT JOIN TM_Ganhamos_JEC AS k ON a.Anomes = k.Anomes AND a.objeto_tratado = k.objeto_tratado
LEFT JOIN TM_Ganhamos_JC AS l ON a.Anomes = l.Anomes AND a.objeto_tratado = l.objeto_tratado
LEFT JOIN TM_Ganhamos_Procon AS m ON a.Anomes = m.Anomes AND a.objeto_tratado = m.objeto_tratado

LEFT JOIN TM_Perdemos_JEC AS n ON a.Anomes = n.Anomes AND a.objeto_tratado = n.objeto_tratado
LEFT JOIN TM_Perdemos_JC AS o ON a.Anomes = o.Anomes AND a.objeto_tratado = o.objeto_tratado
LEFT JOIN TM_Perdemos_Procon AS p ON a.Anomes = p.Anomes AND a.objeto_tratado = p.objeto_tratado

LEFT JOIN TM_Desistido_JEC AS q ON a.Anomes = q.Anomes AND a.objeto_tratado = q.objeto_tratado
LEFT JOIN TM_Desistido_JC AS r ON a.Anomes = r.Anomes AND a.objeto_tratado = r.objeto_tratado
LEFT JOIN TM_Desistido_Procon AS s ON a.Anomes = s.Anomes AND a.objeto_tratado = s.objeto_tratado

LEFT JOIN Qty_Outros_JEC AS t ON a.Anomes = t.Anomes AND a.objeto_tratado = t.objeto_tratado
LEFT JOIN Qty_Outros_JC AS u ON a.Anomes = u.Anomes AND a.objeto_tratado = u.objeto_tratado
LEFT JOIN Qty_Outros_Procon AS v ON a.Anomes = v.Anomes AND a.objeto_tratado = v.objeto_tratado;