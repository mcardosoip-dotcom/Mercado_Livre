SELECT
    i.cas_case_id,
    i.cus_cust_id,
    i.ci_created_by,
    i.ci_owner_id,
    i.ci_created_date,
    i.ci_event_name,
    q.que_queue_name,
    a.cx_team_name,
    c.cas_status as estado,
    COALESCE(
        tea.tea_team_name,
        team.tea_team_name,
        te.tea_team_name
    ) as team,
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
    cas_status,
    c.case_drop_flag
FROM
    meli - bi - data.WHOWNER.BT_CX_CASE_INTERACTION i
    left join meli - bi - data.WHOWNER.BT_CX_CASE c on i.cas_case_id = c.cas_case_id
    left join meli - bi - data.WHOWNER.LK_CX_PROCESS_ADM p on i.ci_process_id = p.cx_pr_id
    left join meli - bi - data.WHOWNER.LK_CX_QUEUE q on i.ci_queue_id = q.que_queue_id
    left join meli - bi - data.WHOWNER.LK_CX_MEMBER m on i.ci_owner_id = m.mem_member_ldap
    left join meli - bi - data.WHOWNER.LK_CX_TEAM te on m.tea_team_id = te.tea_team_id
    left join meli - bi - data.WHOWNER.LK_CX_MEMBER mem on i.ci_created_by = mem.mem_member_ldap
    left join meli - bi - data.WHOWNER.LK_CX_TEAM team on mem.tea_team_id = team.tea_team_id
    left join meli - bi - data.WHOWNER.LK_CX_MEMBER me on i.cas_agent_online = me.mem_member_ldap
    left join meli - bi - data.WHOWNER.LK_CX_TEAM tea on me.tea_team_id = tea.tea_team_id
    left join meli - bi - data.WHOWNER.LK_CX_TEAM_ADMIN a on i.ci_queue_id = a.cx_team_id
WHERE
    i.ci_queue_id in(1825)
    and c.sit_site_id not in ('MLB')
    and i.ci_event_name in (
        'INCOMING_CASE',
        'INCOMING_DERIVATION_EXTERNAL',
        'INCOMING_DERIVATION_EXTERNAL_RETURN',
        'INCOMING_DERIVATION_INTERNAL',
        'INCOMING_MANUAL',
        'INCOMING_RECONTACT',
        'INCOMING_RECONTACT_DUPLICATED',
        'INCOMING_SCHEDULED'
    )
    and i.ci_created_date between date '2024-08-01'
    and date '2024-08-31';