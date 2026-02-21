# Análise: por que MOV_FINANCIAL_ENTITY_ID = bolbradesco não foram capturados

## Resumo

Os casos **bolbradesco** da base de erros (`ANALISE ERROS QS.csv`) não chegam ao arquivo final do processo padrão (Versão Original) por causa da **whitelist de pares (MOV_DETAIL, MOV_TYPE_ID)** no passo **001 - Tabelas auxiliares**. Parte dos movimentos é excluída porque **MOV_TYPE_ID = 'fee'** não está na lista permitida; não há filtro por `MOV_FINANCIAL_ENTITY_ID` (apenas `<> 'coupon'`).

---

## 1. O que a base de erros mostra (bolbradesco)

Nos registros com `MOV_FINANCIAL_ENTITY_ID = bolbradesco` aparecem basicamente dois perfis:

| MOV_DETAIL   | MOV_TYPE_ID | Exemplo no CSV        | PAY_PAYMENT_TYPE_ID |
|-------------|-------------|------------------------|----------------------|
| account_fund | fund        | Recarga (ex.: 600, 510.59) | ticket               |
| payment     | **fee**     | Taxa (ex.: -3.49)     | ticket               |

- **Proc QS** = `#N/D` em todos → não foram considerados pelo processo de Quebra de Sigilo.
- Todos têm `PAY_PAYMENT_ID` preenchido (pagamento por boleto/ticket).

---

## 2. Onde o pipeline filtra (001 - Tabelas auxiliares)

O fluxo até o arquivo final é:

1. **001 - Tabelas auxiliares**  
   - Monta `STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH` a partir de `BT_MP_ACC_MOVEMENTS` com:
     - JOIN em `STG_QS_TITULAR_CAD_VF_FINCH` (investigados + range de datas),
     - `MOV_FINANCIAL_ENTITY_ID <> 'coupon'`,
     - **Lista fixa de pares (MOV_DETAIL, MOV_TYPE_ID)** — quem não está na lista **não entra**.

2. **001** (continuação)  
   - `STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH`: exclui movimentos cujo `ID_PAGAMENTO` tem cancelamento.

3. **004 - Extrato Mercantil**  
   - Popula `CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH` a partir de `STG_QS_AUX_MOVIMENTACAO2`.

4. **014 - Extrato Financeiro CSV**  
   - Gera os CSVs de extrato a partir de `CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH`.

Ou seja: **quem não entra em STG_QS_AUX_MOVIMENTACAO nunca chega ao arquivo final.**

---

## 3. Whitelist atual (trecho relevante do 001)

No arquivo **001 - Tabelas auxiliares**, a condição que define quais movimentos entram é (por volta das linhas 432–455 e 468–491):

```sql
AND ((MOV.MOV_DETAIL = 'account_fund' AND MOV.MOV_TYPE_ID = 'fund') OR
(MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'expense') OR
(MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'income') OR
... outros pares ...)
```

Ou seja, para **payment** só são aceitos:

- `payment` + `expense`
- `payment` + `income`

**Não** existe:

- `payment` + **`fee`**

Para **account_fund** existe apenas:

- `account_fund` + `fund`

Ou seja, **account_fund + fund está na whitelist** (e não há filtro por entidade financeira além de `<> 'coupon'`).

---

## 4. Causas dos bolbradesco não capturados

### 4.1. Causa principal: MOV_TYPE_ID = 'fee' fora da whitelist

- Nos erros, vários registros bolbradesco são **payment** com **MOV_TYPE_ID = 'fee'** (taxa de boleto, ex.: -3.49).
- O pipeline **não inclui** o par `(payment, fee)` em lugar nenhum.
- Consequência: **todos os movimentos payment + fee (incluindo bolbradesco) são descartados já na criação de STG_QS_AUX_MOVIMENTACAO** e nunca chegam ao extrato final.

Isso explica de forma direta a não captura desses IDs.

### 4.2. account_fund + fund (recarga bolbradesco)

- O par **account_fund + fund** **está** na whitelist.
- Se algum movimento **account_fund + fund** com bolbradesco ainda assim não aparece no arquivo final, as hipóteses são:
  1. **Cancelamento:** o mesmo `ID_PAGAMENTO` tem um movimento de cancelamento → o registro é removido em `STG_QS_AUX_MOVIMENTACAO2` (EXCLUIR = 'sim').
  2. **Escopo da execução:** o `CUS_CUST_ID` não estava em `STG_QS_TITULAR_CAD_VF_FINCH` naquela execução (planilha presenta, range de datas, hashtags #extratoMercantil/#extratoAplicacoesFinanceiras).
  3. **Datas:** `MOV_CREATED_DT` fora do `MOVIMENTACAO_MIN` e `RANGE_MAX` do titular.

Para fechar se há perda de account_fund+fund por cancelamento ou escopo, seria necessário cruzar os `MOV_MOVE_ID` / `ID_PAGAMENTO` da base de erros com as tabelas `STG_QS_AUX_MOVIMENTACAO_CAD_VF_FINCH` e `STG_QS_AUX_MOVIMENTACAO2_CAD_VF_FINCH` da execução em que a análise foi feita.

---

## 5. Recomendações

### 5.1. Incluir (payment, fee) na whitelist (001 - Tabelas auxiliares)

Para que as **taxas (fee)** de pagamento (incluindo bolbradesco) passem a ser capturadas:

1. Incluir o par na condição de movimento permitido, por exemplo:

   - No bloco do JOIN e no bloco do WHERE, adicionar:
   - `(MOV.MOV_DETAIL = 'payment' AND MOV.MOV_TYPE_ID = 'fee')`

2. Incluir mapeamento para descrição e tipo de lançamento nos CASEs já existentes (por volta das linhas 331–356 e 359–384), por exemplo:
   - Descrição: algo como `'Tarifa/Taxa de pagamento'` ou `'Taxa - Boleto'`.
   - Tipo de lançamento: usar um código de despesa/tarifa coerente com o plano de contas (ex.: 110 ou outro já usado para IOF/tarifas).

3. Garantir **natureza** para `fee`:
   - No trecho que define `NATUREZA_LANCAMENTO`/`NATUREZA_SALDO` (por volta de 386–395), hoje só há `expense`, `income` e `fund`. É preciso tratar `MOV_TYPE_ID = 'fee'` (normalmente como débito, por ex. `'D'`).

Com isso, os movimentos **payment + fee** (bolbradesco e outros) passam a entrar na base de movimentação e a seguir até o extrato final.

### 5.2. Conferir account_fund + fund (opcional)

- Se a análise for só sobre bolbradesco e o foco for “taxas não aparecem”, a inclusão de `(payment, fee)` já resolve a parte que hoje está 100% fora da whitelist.
- Se houver relato de “recargas bolbradesco (account_fund + fund) também faltando”, aí vale:
  - Verificar na execução real se esses `MOV_MOVE_ID`/`ID_PAGAMENTO` entram em `STG_QS_AUX_MOVIMENTACAO` e se são excluídos em `STG_QS_AUX_MOVIMENTACAO2` por cancelamento, e
  - Validar se o investigado e o range de datas estavam no escopo da planilha presenta.

---

## 6. Referência rápida (arquivos)

| Arquivo / passo              | Papel na captura dos movimentos                          |
|-----------------------------|-----------------------------------------------------------|
| 001 - Tabelas auxiliares    | Define quais (MOV_DETAIL, MOV_TYPE_ID) entram; aqui está a exclusão de payment+fee e a única menção a MOV_FINANCIAL_ENTITY_ID (<> 'coupon'). |
| 001 (MOVIMENTACAO2)         | Exclui movimentos com cancelamento no mesmo ID_PAGAMENTO. |
| 004 - Extrato Mercantil     | Monta CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH a partir de MOVIMENTACAO2. |
| 014 - Extrato Financeiro CSV| Gera os CSVs a partir de CAD_TBL_QS_EXTRATO_MOVIMENTACAO_FINCH. |

---

**Conclusão:** Os casos com **MOV_FINANCIAL_ENTITY_ID = bolbradesco** não são excluídos por serem “bolbradesco”, e sim porque uma parte relevante deles é **payment + fee**, e o processo padrão **não considera MOV_TYPE_ID = 'fee'** na whitelist de movimentos. Incluir o par **(payment, fee)** no 001 resolve a não captura desses IDs até o arquivo final.
