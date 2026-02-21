WITH filtered_interactions AS (
    SELECT
        *
    FROM
        meli - bi - data.WHOWNER.BT_CX_CASE_INTERACTION
    WHERE
        ci_queue_id = 1825
),
filtered_cases AS (
    SELECT
        *
    FROM
        meli - bi - data.WHOWNER.BT_CX_CASE
    WHERE
        sit_site_id NOT IN ('MLB')
),
query1 AS (
    SELECT
        i.cas_case_id,
        i.cus_cust_id,
        i.ci_created_by,
        i.ci_owner_id,
        DATE(i.ci_created_date) AS ci_created_date,
        -- Transformação de datetime para data
        i.ci_event_name,
        q.que_queue_name,
        a.cx_team_name,
        c.cas_status AS estado,
        COALESCE(
            tea.tea_team_name,
            team.tea_team_name,
            te.tea_team_name
        ) AS team,
        i.ci_process_id,
        p.cx_pr_name_HSP,
        i.ci_clasif_id,
        i.ci_clasif_name,
        i.ci_channel_type,
        c.sit_site_id,
        c.cas_subject,
        i.cas_agent_online,
        c.cas_contact_origin,
        c.cas_channel_queue_desc,
        c.cas_status,
        c.case_drop_flag
    FROM
        filtered_interactions i
        LEFT JOIN filtered_cases c ON i.cas_case_id = c.cas_case_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_PROCESS_ADM p ON i.ci_process_id = p.cx_pr_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_QUEUE q ON i.ci_queue_id = q.que_queue_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_MEMBER m ON i.ci_owner_id = m.mem_member_ldap
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_TEAM te ON m.tea_team_id = te.tea_team_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_MEMBER mem ON i.ci_created_by = mem.mem_member_ldap
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_TEAM team ON mem.tea_team_id = team.tea_team_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_MEMBER me ON i.cas_agent_online = me.mem_member_ldap
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_TEAM tea ON me.tea_team_id = tea.tea_team_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_TEAM_ADMIN a ON i.ci_queue_id = a.cx_team_id
    WHERE
        i.ci_event_name IN (
            'INCOMING_CASE',
            'INCOMING_DERIVATION_EXTERNAL',
            'INCOMING_DERIVATION_EXTERNAL_RETURN',
            'INCOMING_DERIVATION_INTERNAL',
            'INCOMING_MANUAL',
            'INCOMING_RECONTACT',
            'INCOMING_RECONTACT_DUPLICATED',
            'INCOMING_SCHEDULED'
        )
        AND i.ci_created_date BETWEEN DATE '2024-08-01'
        AND DATE '2024-08-31'
),
query2 AS (
    SELECT
        i.cas_case_id,
        DATE(i.ci_created_date) AS encerrado_date,
        -- Transformação de datetime para data
        i.ci_clasif_name AS proceso,
        s.cx_sol_name AS solucion
    FROM
        filtered_interactions i
        LEFT JOIN filtered_cases c ON i.cas_case_id = c.cas_case_id
        LEFT JOIN meli - bi - data.WHOWNER.LK_CX_SOLUTION_ADM s ON i.wcm_cont_id = s.cx_sol_id
    WHERE
        i.ci_event_name IN (
            'OUTGOING_FIRST_CONTACT',
            'OUTGOING_CONTACT',
            'OUTGOING_CONTACT_PROACTIVE',
            'OUTGOING_DERIVATION_EXTERNAL',
            'OUTGOING_DERIVATION_EXTERNAL_RETURN',
            'OUTGOING_DERIVATION_INTERNAL'
        )
        AND i.ci_created_date BETWEEN DATE '2024-09-16'
        AND DATE '2024-09-22'
)
SELECT
    q1.*,
    q2.encerrado_date,
    q2.proceso,
    q2.solucion,
    lkd.*,
    DATE_DIFF(q2.encerrado_date, q1.ci_created_date, DAY) AS diff_in_days,
    CASE
        WHEN lkd.LEGAL_ID IS NOT NULL
        AND lkd.LEGAL_ID <> '' THEN 1
        ELSE 0
    END AS Flag_base_legales,
    CASE
        WHEN q2.solucion IS NULL THEN 'Aberto'
        ELSE 'Fechado'
    END AS Status_CX
FROM
    query1 q1
    LEFT JOIN query2 q2 ON q1.cas_case_id = q2.cas_case_id
    LEFT JOIN meli - bi - data.WHOWNER.LK_LEGALES_DATABASE lkd ON q1.cus_cust_id = lkd.CUS_CUST_ID;