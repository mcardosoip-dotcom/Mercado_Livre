# Verificação extensa: pipeline Versão Original x casos Bolbradesco

Objetivo: identificar qualquer etapa que impeça **account_fund+fund+bolbradesco** ou **payment+fee+bolbradesco** de chegarem ao arquivo final (extrato financeiro CSV).

---

## Fluxo do extrato (resumo)

```
BT_MP_ACC_MOVEMENTS (origem)
    → 001: STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH (whitelist + JOIN titular)
    → 001: STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH (exclui cancelamentos)
    → 004: CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH (INSERT TIT LEFT JOIN MOV, EXTRATO='Sim')
    → 014: Python lê CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH e gera CSVs (EXTRATO / rendimento)
```

---

## 1. 001 - Tabelas auxiliares

### 1.1 Entrada em STG_QS_AUX_MOVIMENTACAO

- **Filtro por entidade:** apenas `MOV_FINANCIAL_ENTITY_ID <> 'coupon'`. **Bolbradesco não é excluído.**
- **Whitelist (MOV_DETAIL, MOV_TYPE_ID):**
  - `(account_fund, fund)` → **incluído** (todos os account_fund+fund, inclusive bolbradesco).
  - `(payment, fee)` → **incluído só** quando `MOV_FINANCIAL_ENTITY_ID = 'bolbradesco'`.
- **Conclusão:** Nenhuma condição impede bolbradesco (account_fund+fund ou payment+fee) de entrar na primeira staging.

### 1.2 Saída para MOVIMENTACAO2 (cancelamento)

- **Regra:** `EXCLUIR = 'sim'` quando existe **outro** movimento com o **mesmo ID_PAGAMENTO** que seja de cancelamento (`MOV_LABEL LIKE '%cancellation%'` ou `'%cancelled %'`) e `QTD > 1`.
- Para **account_fund+fund** bolbradesco, `ID_PAGAMENTO = PAY_PAYMENT_ID`.
- **Efeito:** Se um boleto/pagamento bolbradesco for cancelado, **todos** os movimentos com aquele `ID_PAGAMENTO` (incluindo o account_fund e o fee) saem da MOVIMENTACAO2. Isso é regra de negócio (não mostrar cancelados), não um filtro contra bolbradesco.
- **Conclusão:** Não há bloqueio específico a bolbradesco; apenas perda de movimentos que pertencem a pagamentos cancelados.

### 1.3 Tabelas de relacionado (Payout, Payin, Payments, Withdrawal)

- Bolbradesco **account_fund+fund** tem `PAY_PAYMENT_ID` preenchido → `TBL_RELACIONADO = 'Payments'`.
- Entram em `STG_QS_AUX_PAYMENTS_*` e depois `STG_QS_PAGAMENTO_*` e `STG_QS_PAGAMENTO_REL_*`.
- O relacionado vem de `BT_MP_PAY_PAYMENTS_ALL` (JOIN por `PAY_PAYMENT_ID`). Para pagamentos boleto/ticket, essa tabela pode ou não ter a contraparte; se não tiver, `ID_RELACIONADO` / dados do REL ficam NULL.
- **Importante:** Essas tabelas são usadas para **origem/destino** (REL). O **004 não filtra** por REL: faz `LEFT JOIN ... MOV` e insere **todos** os movimentos da MOVIMENTACAO2. Portanto, mesmo que o relacionado bolbradesco não exista em REL, o **movimento continua indo para CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH**.
- **Conclusão:** Nenhuma etapa aqui impede bolbradesco de chegar ao extrato; no máximo o “relacionado” pode vir vazio para alguns pagamentos boleto.

---

## 2. 002 - Tabelas auxiliares 2

- **STG_QS_RELACIONADO_CAD_VF_FINCH:** UNION de Payout, Payin, Payments e Withdrawal REL. Nenhum filtro por `MOV_DETAIL`, `MOV_TYPE_ID` ou entidade.
- **STG_QS_FLAG_MOV_CAD_VF_FINCH:** apenas LEFT JOIN MOVIMENTACAO2 por `CUS_CUST_ID`. Nenhum filtro por tipo de movimento.
- **Conclusão:** Nada aqui bloqueia bolbradesco.

---

## 3. 003 - Inserir tabelas finais

- **TBL_QS_EXTRATO_FINCH:** preenchida a partir de TIT + MOVIMENTACAO2 + REL. Usa `DESCRICAO_LANCAMENTO` e `TIPO_LANCAMENTO` da MOVIMENTACAO2 (onde já temos “Recarga via boleto (Bolbradesco)” e 217 para account_fund+fund bolbradesco).
- **Outras tabelas (Contas, Agências, Titulares, Origem Destino):** usam MOVIMENTACAO2 ou REL sem filtrar por tipo/entidade.
- **Conclusão:** Nenhum filtro que impeça bolbradesco.

---

## 4. 004 - Extrato Mercantil

- **INSERT em CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH:**
  - Fonte: `STG_QS_TITULAR_CAD_VF_FINCH TIT` **LEFT JOIN** `STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH MOV` por `CUS_CUST_ID`.
  - Filtro: `WHERE TIT.EXTRATO = 'Sim'`. **Não há** filtro em `MOV_DETAIL`, `MOV_TYPE_ID` ou entidade.
- Todos os movimentos da MOVIMENTACAO2 do titular (incluindo account_fund+fund e payment+fee bolbradesco) são inseridos.
- **TIPO_MOVIMENTO:** `CASE WHEN MOV.CUS_CUST_ID IS NOT NULL THEN 'EXTRATO    ' ELSE NULL END` → todo movimento que veio do JOIN recebe `'EXTRATO    '`.
- **Conclusão:** Nenhuma condição impede bolbradesco de entrar na tabela final de extrato.

---

## 5. 014 - Extrato Financeiro - CSV (Python)

- Lê **CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH** com filtro `DATAHORA_IMPORTACAO = (SELECT MAX(...) FROM STG_QS_PLANILHA_PRESENTA_CAD_VF_FINCH)`.
- **Filtro para o CSV de extrato:** `TIPO_MOVIMENTO == 'EXTRATO'` (após strip). Os movimentos que vieram do 004 têm `TIPO_MOVIMENTO = 'EXTRATO    '` → passam no filtro.
- Não há filtro por `MOV_DETAIL`, `MOV_TYPE_ID` ou entidade.
- **Conclusão:** Bolbradesco que está na tabela é exportado para o CSV de extrato.

---

## 6. 015 - Quebra De Sigilo - Geração Do Zip

- Também lê **CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH**. Sem filtro por tipo de movimento ou entidade na lógica de geração do zip.
- **Conclusão:** Nenhum bloqueio a bolbradesco.

---

## 7. Demais arquivos (000, 005–013)

- **000 - Criação de tabelas:** só cria/trunca estruturas; não filtra dados.
- **005–013:** Carta Circular 3454, Extrato não correspondente etc. Não consomem MOVIMENTACAO2 para o **extrato financeiro** que é preenchido pelo 004 e lido pelo 014.
- **Conclusão:** Nenhum deles impede bolbradesco de chegar ao extrato final.

---

## Resumo: o que pode impedir Bolbradesco de “chegar ao fim”?

| Etapa | Bloqueia Bolbradesco? | Observação |
|-------|------------------------|------------|
| 001 – Whitelist / JOIN titular | Não | account_fund+fund e payment+fee+bolbradesco estão permitidos. |
| 001 – Cancelamento (MOVIMENTACAO2) | Só por negócio | Movimentos do mesmo ID_PAGAMENTO de um cancelamento são excluídos (correto). |
| 001 – PAYMENTS / REL | Não | Só preenchem relacionado; 004 não exige REL para inserir movimento. |
| 002 – RELACIONADO / FLAG_MOV | Não | Sem filtro por tipo/entidade. |
| 003 – Tabelas finais | Não | Usam MOVIMENTACAO2/REL sem filtrar bolbradesco. |
| 004 – INSERT extrato | Não | Inserção por TIT + MOV (MOVIMENTACAO2), sem filtro em MOV. |
| 014 – CSV | Não | Filtra só por TIPO_MOVIMENTO = 'EXTRATO'. |
| 015 – Zip | Não | Sem filtro por tipo/entidade. |

Conclusão da verificação: **não existe nenhuma condição no pipeline da Versão Original que exclua explicitamente casos Bolbradesco (account_fund+fund ou payment+fee+bolbradesco).**  
Quem já está em **STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH** (no escopo do titular e não cancelado) segue até **CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH** e, em seguida, até o CSV de extrato (014) e ao zip (015).

---

## Pontos de atenção (não bloqueiam, mas podem causar confusão)

1. **Cancelamento:** Se um boleto bolbradesco for cancelado, todos os movimentos com aquele `ID_PAGAMENTO` saem da MOVIMENTACAO2 e não aparecem no extrato. É esperado.
2. **Relacionado vazio:** Para alguns pagamentos boleto, `BT_MP_PAY_PAYMENTS_ALL` pode não ter a contraparte; nesse caso, origem/destino (REL) fica em branco, mas o **movimento continua no extrato**.
3. **Schema da tabela de extrato:** O 004 insere colunas como `ID_INVESTIGADO`, `DATA_LANCAMENTO` e o valor formatado. O script 014 usa nomes como `CUS_CUST_ID`, `MOV_CREATED_DT`, `MOV_AMOUNT`. Se a tabela real tiver apenas os nomes do 004, o Python pode estar usando views/aliases ou outra versão da tabela. Vale confirmar no BigQuery os nomes das colunas de **CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH** e a query exata que o 014 usa em produção.

---

## Recomendações

1. **Manter como está:** Nenhuma alteração é necessária no pipeline para “liberar” bolbradesco; ele já está contemplado na whitelist e em todas as etapas até o CSV.
2. **Se ainda faltar caso no arquivo final:** Verificar (a) se o movimento está em MOVIMENTACAO2 (ex.: query de validação account_fund) e (b) se não foi excluído por cancelamento (mesmo `ID_PAGAMENTO` com movimento de cancelamento).
3. **Descrição no extrato:** A alteração já feita no 001 (descrição “Recarga via boleto (Bolbradesco)” para account_fund+fund+bolbradesco) garante que esses lançamentos sejam identificáveis no arquivo final.
