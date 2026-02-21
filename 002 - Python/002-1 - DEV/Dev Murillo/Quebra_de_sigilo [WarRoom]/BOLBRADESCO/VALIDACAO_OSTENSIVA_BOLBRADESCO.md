# Validação ostensiva: movimentação Bolbradesco até o arquivo final

**Condições em foco (PAY_PAYMENT_METHOD_ID = 'bolbradesco'):**
- `MOV_DETAIL = 'account_fund'` e `MOV_TYPE_ID = 'fund'`
- `MOV_DETAIL = 'payment'` e `MOV_TYPE_ID = 'fee'`

Verificação em cada arquivo do pipeline para garantir que **nada** impeça essas linhas de aparecer no extrato final (CSV/Zip).

---

## 1. 001 - Tabelas auxiliares

### 1.1 Entrada em STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH
- **Whitelist:** Inclui `(account_fund, fund)` para todos e `(payment, fee)` quando `LOWER(TRIM(CAST(PAY_PAYMENT_METHOD_ID AS STRING))) = 'bolbradesco'`. Nenhum filtro exclui essas combinações.
- **Filtros gerais:** `MOV_FINANCIAL_ENTITY_ID <> 'coupon'`, `MOV_LABEL NOT LIKE '%hidden%'`, BRL, MLB. Nenhum deles exclui bolbradesco.
- **JOIN:** Apenas com titular (CUS_CUST_ID) e intervalo de datas (MOV_CREATED_DT BETWEEN MOVIMENTACAO_MIN AND RANGE_MAX). Movimentos fora do range do titular não entram; não há filtro por tipo/entidade além da whitelist.
- **Conclusão:** Nenhum bloqueio à movimentação bolbradesco na primeira staging.

### 1.2 STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH (cancelamento)
- **Regra:** `EXCLUIR = 'sim'` quando existe outro movimento com o **mesmo ID_PAGAMENTO** com `MOV_LABEL` de cancelamento e `QTD > 1`.
- Para bolbradesco, `ID_PAGAMENTO = PAY_PAYMENT_ID`. Se o boleto/pagamento for cancelado, todos os movimentos com aquele ID (incluindo account_fund e fee) saem. É regra de negócio, não filtro por tipo.
- **Conclusão:** Nenhum bloqueio específico a bolbradesco; apenas exclusão por cancelamento do mesmo pagamento.

### 1.3 Tabelas de relacionado (Payout, Payin, **Payments**, Withdrawal)
- Bolbradesco (account_fund+fund e payment+fee) tem `PAY_PAYMENT_ID` preenchido → `TBL_RELACIONADO = 'Payments'`.
- Entram em `STG_QS_AUX_PAYMENTS_*` e depois `STG_QS_PAGAMENTO_*` e `STG_QS_PAGAMENTO_REL_*`.
- **Filtro usado:** `WHERE TBL_RELACIONADO = 'Payments'` (e COMID/SEMID por ID_RELACIONADO). Não há filtro por `MOV_DETAIL`, `MOV_TYPE_ID` ou `PAY_PAYMENT_METHOD_ID`.
- O 004 e o 003 **não** exigem que o movimento tenha linha em REL para ser inserido no extrato: usam `LEFT JOIN` em REL. Portanto, mesmo que o relacionado (BT_MP_PAY_PAYMENTS_ALL) não traga contraparte para algum boleto, o **movimento continua** em MOVIMENTACAO2 e segue para o extrato.
- **Conclusão:** Nenhum bloqueio; no máximo relacionado em branco para alguns pagamentos.

---

## 2. 002 - Tabelas auxiliares 2

### 2.1 STG_QS_RELACIONADO_CAD_VF_FINCH
- UNION de Payout, Payin, Payments e Withdrawal REL. Apenas CASE para SPLITTER/PAYINS em alguns campos. Nenhum filtro por `MOV_DETAIL`, `MOV_TYPE_ID` ou `PAY_PAYMENT_METHOD_ID`.
- **Conclusão:** Nenhum bloqueio.

### 2.2 STG_QS_FLAG_MOV_CAD_VF_FINCH
- `TIT LEFT JOIN MOVIMENTACAO2` por `CUS_CUST_ID`. Não filtra por tipo de movimento.
- **Conclusão:** Nenhum bloqueio.

---

## 3. 003 - Inserir tabelas finais

- **TBL_QS_EXTRATO_FINCH, TBL_QS_CONTAS_FINCH, TBL_QS_ORIGEM_DESTINO_FINCH, etc.:** Todas usam `LEFT JOIN STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH MOV` (e REL quando aplicável). Filtro apenas por `TIT.CIRCULAR_3454 = 'Sim'` onde aplicável. Nenhum `WHERE` em colunas de MOV (MOV_DETAIL, MOV_TYPE_ID, PAY_PAYMENT_METHOD_ID).
- **Conclusão:** Nenhum bloqueio à movimentação bolbradesco.

---

## 4. 004 - Extrato Mercantil

- **INSERT em CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH:**
  - Fonte: `STG_QS_TITULAR_CAD_VF_FINCH TIT` **LEFT JOIN** `STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH MOV` por `CUS_CUST_ID`.
  - Único filtro: `WHERE TIT.EXTRATO = 'Sim'`. Não há filtro em `MOV.MOV_DETAIL`, `MOV.MOV_TYPE_ID`, `MOV.PAY_PAYMENT_METHOD_ID` nem em qualquer coluna de MOV.
- **TIPO_MOVIMENTO:** `CASE WHEN MOV.CUS_CUST_ID IS NOT NULL THEN 'EXTRATO    ' ELSE NULL END` → todo movimento que veio do JOIN (qualquer tipo) recebe `'EXTRATO    '`.
- **Conclusão:** Nenhum bloqueio; toda linha de MOVIMENTACAO2 do titular com EXTRATO = 'Sim' é inserida, incluindo account_fund+fund e payment+fee bolbradesco.

---

## 5. 014 - Extrato - Extrato Financeiro - CSV (Python)

- **Leitura:** `SELECT ... FROM CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH WHERE DATAHORA_IMPORTACAO = (SELECT MAX(...) FROM STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH)`.
- **Filtro para CSV de extrato:** `TIPO_MOVIMENTO == 'EXTRATO'` (após strip). Todas as linhas inseridas pelo 004 têm `TIPO_MOVIMENTO = 'EXTRATO    '` → passam.
- Não há filtro por `MOV_DETAIL`, `MOV_TYPE_ID`, `PAY_PAYMENT_METHOD_ID` nem por qualquer coluna que identifique tipo de movimento.
- **Conclusão:** Nenhum bloqueio; bolbradesco que está na tabela é exportado para o CSV.

---

## 6. 015 - Quebra De Sigilo - Geração Do Zip

- Usa a mesma tabela `CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH`. Não há filtro por tipo de movimento ou por colunas de movimento nas consultas que alimentam o zip.
- **Conclusão:** Nenhum bloqueio.

---

## 7. Demais arquivos (000, 005 a 013)

- **000 - Criação de tabelas:** Apenas CREATE/TRUNCATE de estruturas; não filtra dados.
- **005 a 013:** Carta Circular 3454, Extrato não correspondente, etc. Não consomem MOVIMENTACAO2 para o fluxo do **extrato financeiro** (004 → 014/015). Não alteram CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH.
- **Conclusão:** Nenhum deles impede a movimentação bolbradesco de chegar ao arquivo final.

---

## Resumo da validação ostensiva

| Arquivo | Filtro por MOV_DETAIL / MOV_TYPE_ID / PAY_PAYMENT_METHOD_ID? | Pode impedir bolbradesco? |
|---------|----------------------------------------------------------------|----------------------------|
| 001 – Whitelist / JOIN | Não (bolbradesco está na whitelist) | Não |
| 001 – Cancelamento | Não (usa só ID_PAGAMENTO e MOV_LABEL cancelamento) | Não* |
| 001 – Payout/Payin/Payments/Wit | Só TBL_RELACIONADO = 'Payments'; bolbradesco entra | Não |
| 002 – RELACIONADO / FLAG_MOV | Não | Não |
| 003 – Inserir tabelas finais | Não | Não |
| 004 – Extrato Mercantil | Não | Não |
| 014 – CSV Python | Não (só TIPO_MOVIMENTO = EXTRATO) | Não |
| 015 – Zip Python | Não | Não |
| 000, 005–013 | Não aplicável ao fluxo do extrato | Não |

\*Cancelamento remove por negócio (pagamento cancelado), não por ser bolbradesco.

**Conclusão geral:** Nenhum arquivo do pipeline aplica filtro que exclua explicitamente as combinações **account_fund+fund** ou **payment+fee** com **PAY_PAYMENT_METHOD_ID = 'bolbradesco'**. Quem entra em STG_QS_AUX_MOVIMENTACAO (e depois em MOVIMENTACAO2, sem ser cancelado) segue até CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH e, em seguida, até o CSV (014) e ao Zip (015).

---

## Uso da query de teste

O arquivo **`query_teste_bolbradesco_001.sql`** aplica na **MOV** (BT_MP_ACC_MOVEMENTS) as mesmas condições de filtro que o 001 usa para bolbradesco (datas, BRL, MLB, coupon, hidden, PAY_PAYMENT_METHOD_ID = 'bolbradesco' e as duas combinações de MOV_DETAIL/MOV_TYPE_ID). Serve para:

1. Ver se existem linhas na origem que atendem ao critério.
2. Ver se há algum padrão (ex.: MOV_LABEL, datas, CUS_CUST_ID) que depois possa ser excluído por cancelamento ou por não estar no range do titular.

Ajuste **DATA_INI** e **DATA_FIM** no início do WHERE conforme o período que quiser testar.
