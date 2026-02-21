WITH BaseDeEntradas AS (
    SELECT
        MB.id AS entrada_id,
        DATE(TIMESTAMP_MICROS(CAST(fecha_registro / 1000 AS INT64))) AS mesa_fecha_registro_data,
        TIME(TIMESTAMP_MICROS(CAST(fecha_registro / 1000 AS INT64))) AS mesa_fecha_registro_hora,
        CAST(MB.entrada_estado_id AS STRING) AS mesa_entrada_estado_id,
        NULL AS grupo,
        TE.estado_nombre AS mesa_estado_nombre,
        MB.entrada_tipo_documento_id AS mesa_entrada_tipo_documento_id,
        TD.tipo_documento_nombre,
        entrada_lista_distribucion AS mesa_entrada_lista_distribucion,
        entrada_numero_externo_meli AS mesa_entrada_numero_externo_meli,
        expediente AS mesa_expediente,
        MB.anulado AS anulado,
        MB.entrada_tematica_id AS entrada_tematica_id,
        MB.entrada_pais_id
    FROM
        `pdme000426-c1s7scatwm0-furyid.STG.INPUT_MESA_BASE_TAB_ENTRADAS` MB
        LEFT JOIN `pdme000426-c1s7scatwm0-furyid.STG.INPUT_MESA_BASE_TAB_ESTADOS` TE
            ON TE.id = CAST(MB.entrada_estado_id AS INT64)
        LEFT JOIN `pdme000426-c1s7scatwm0-furyid.STG.INPUT_MESA_BASE_TIPO_DOCUMENTOS` TD
            ON TD.id = MB.entrada_tipo_documento_id
),

tematica AS (
    SELECT
        id,
        tematica,
        tematica_clasificacion
    FROM
        `pdme000426-c1s7scatwm0-furyid.STG.INPUT_MESA_BASE_VISTA_ENTRADAS`
),

EstadosFiltrados AS (
    SELECT
        entrada_id,
        MAX(FECHAHORA_FIN) AS DATA_MAX_FECHAHORA_FIN
    FROM
        `pdme000426-c1s7scatwm0-furyid.STG.LK_MESA_BASE_ENTRADA_ESTADOS`
    WHERE
        ENTRADA_ESTADO_ID = '3'
        AND FECHAHORA_FIN IS NOT NULL
    GROUP BY
        entrada_id
)

SELECT
    a.* EXCEPT(entrada_pais_id),

    CASE
        WHEN a.entrada_pais_id = 1 THEN 'SIN PAIS'
        WHEN a.entrada_pais_id = 2 THEN 'ARGENTINA'
        WHEN a.entrada_pais_id = 3 THEN 'CHILE'
        WHEN a.entrada_pais_id = 4 THEN 'COLOMBIA'
        WHEN a.entrada_pais_id = 5 THEN 'MEXICO'
        WHEN a.entrada_pais_id = 6 THEN 'PERU'
        WHEN a.entrada_pais_id = 7 THEN 'URUGUAY'
        WHEN a.entrada_pais_id = 8 THEN 'VENEZUELA'
        WHEN a.entrada_pais_id = 9 THEN 'COSTA RICA'
        WHEN a.entrada_pais_id = 10 THEN 'ECUADOR'
        WHEN a.entrada_pais_id = 11 THEN 'ESPAÑA'
        ELSE 'ID Não Mapeado'
    END AS nome_pais,

    COALESCE(NULLIF(TRIM(b.tematica), ''), 'Sem inf') AS tematica,

    DATE(c.DATA_MAX_FECHAHORA_FIN) AS mesa_data_fim,
    TIME(c.DATA_MAX_FECHAHORA_FIN) AS mesa_hora_fim,

    DATE_DIFF(
        DATE(c.DATA_MAX_FECHAHORA_FIN),
        a.mesa_fecha_registro_data,
        DAY
    ) AS diferenca_dias_conclusao,

    CASE
        WHEN a.mesa_entrada_numero_externo_meli IS NOT NULL
             AND TRIM(a.mesa_entrada_numero_externo_meli) <> '' THEN 1
        ELSE 0
    END AS Registro_Meli,

    DATE_DIFF(
        DATE(c.DATA_MAX_FECHAHORA_FIN),
        a.mesa_fecha_registro_data,
        DAY
    ) AS TMC,

    CASE
        WHEN DATE_DIFF(
                 DATE(c.DATA_MAX_FECHAHORA_FIN),
                 a.mesa_fecha_registro_data,
                 DAY
             ) > 2 THEN 'Fora'
        ELSE 'Dentro'
    END AS SLA_Txt,

    CASE
        WHEN b.tematica IN (
            'Solicitud de informacion de usuarios','Embargo - usuario','Averiguacion de paradero',
            'Secuestro','Trata de personas','Pornografia infantil','Detenidos','Audiencia urgente',
            'Estafa com prestamos','Averiguacion delito','Lavado de dinero','Propiedad Intelectual',
            'Allanamento','Requerimiento sin adjunto','BCRA Masivo','Embargo proveedor'
        ) THEN 'Salesforce'

        WHEN b.tematica IN (
            'Audiencia','SECLO','Demanda','Notificacion procesal','Mediacion','Sancion judicial',
            'Imputación administrativa','Sancion administrativa','Reclamo','Defensa Consumidor',
            'Queja','Intimacion'
        ) THEN 'eLaw'

        WHEN b.tematica IN (
            'Requerimiento','Prohibición de comercialización','Licencias y Permissos',
            'Proceso relacionados a discriminación','Temas patronales/Vivienda de los trabalhadores',
            'Cartas notariales','Patentes','Libre Competencia','Antitrust','Uso de marca',
            'Derecho de petición - Tutela','BCRA Oficial de cumplimiento','Carta Simple',
            'Talonarios de Seguimento','Notificación INAI'
        ) THEN 'Outros'

        ELSE 'Outros'
    END AS destino
FROM
    BaseDeEntradas a
    LEFT JOIN tematica b
        ON a.entrada_id = b.id
    LEFT JOIN EstadosFiltrados c
        ON CAST(a.entrada_id AS STRING) = c.entrada_id;
