# Antes e depois: Placeholders Mercado Pago para contas sem AVK_ID

Texto em detalhes para composição de email ou documentação.

---

## Contexto

No pipeline de Quebra de Sigilo (Carta Circular 3454), as contas Mercado Pago são identificadas, entre outros, pelo **AVK_ID** (exposto como **CONTA_SPB** nas tabelas staging). Esse valor vem do join com `BT_MP_ACCOUNT_VIRTUAL_KEY` e pode ficar **vazio** quando não há conta ativa encontrada para o cliente.  
Nestes casos, a identificação do titular e da conta na carta deve continuar possível, usando **CUS_CUST_ID** como identificador e preenchendo os dados da **instituição** com os placeholders padrão do Mercado Pago/Mercado Livre.

---

## O que acontecia ANTES (Versão Original)

- **CONTA_SPB (AVK_ID):** Não havia tratamento explícito quando o valor vinha vazio. O campo era apenas repassado (e podia ser NULL) para as tabelas de titular, contas, extrato e agências.
- **Número da conta (NUMERO_CONTA):** Quando CONTA_SPB estava vazio, o pipeline já usava **CUS_CUST_ID** como fallback, via `COALESCE(TIT.CONTA_SPB, CAST(TIT.CUS_CUST_ID AS STRING))`. Ou seja, a identificação da conta já era feita pelo cust_id nesses casos.
- **Dados da instituição (banco/agência/nome):** Para todas as contas Mercado Pago eram usados valores fixos:
  - **NUMERO_BANCO:** 323 (COMPE)
  - **NUMERO_AGENCIA:** 0001 (4 dígitos)
  - **NOME_AGENCIA:** “Mercado Pago”
- **Problema:** Não havia distinção formal entre “conta com AVK_ID preenchido” e “conta MP sem AVK_ID”. Além disso, a agência era sempre 0001 e o nome da instituição era apenas “Mercado Pago”, e não o nome completo oficial (“Mercado Pago - Instituição de Pagamento”), e a agência não refletia o padrão de banco digital (001).

Resumindo: a identificação por CUS_CUST_ID já existia quando CONTA_SPB estava vazio, mas os **placeholders da instituição** não eram diferenciados para esse cenário (agência 001, nome completo, etc.).

---

## O que acontece AGORA (Versão Placeholders MP sem AVK)

A nova versão (**002 - Versão Placeholders MP sem AVK**) altera apenas o step **003 - inserir tabelas finais**. Os steps 001 e 002 permanecem iguais aos da Versão Original.

### 1. Identificação da conta

- **Mantido:** Quando CONTA_SPB está vazio, **NUMERO_CONTA** continua sendo preenchido com **CUS_CUST_ID** (via `COALESCE(TIT.CONTA_SPB, CAST(TIT.CUS_CUST_ID AS STRING))`). Nenhuma mudança na regra de identificação da conta.

### 2. Tabela de Agências (TBL_QS_AGENCIAS_FINCH)

- **Antes:** NUMERO_AGENCIA = `0001`, NOME_AGENCIA = `Mercado Pago`.
- **Agora:** NUMERO_AGENCIA = `001`, NOME_AGENCIA = `Mercado Pago - Instituição de Pagamento`.  
Assim, o registro único de agência da execução já reflete o padrão de banco digital e o nome completo da instituição.

### 3. Tabela de Contas (TBL_QS_CONTAS_FINCH)

- **Antes:** NUMERO_AGENCIA era sempre `0001` para todos os titulares. NUMERO_CONTA = COALESCE(CONTA_SPB, CUS_CUST_ID).
- **Agora:**
  - **NUMERO_CONTA:** inalterado — continua COALESCE(CONTA_SPB, CUS_CUST_ID).
  - **NUMERO_AGENCIA:** quando **CONTA_SPB está vazio** (conta MP sem AVK_ID) → `001`; quando CONTA_SPB está preenchido → `0001` (comportamento anterior).  
Assim, contas sem AVK_ID passam a ser explicitamente associadas ao placeholder de agência 001 (banco digital).

### 4. Tabela de Extrato (TBL_QS_EXTRATO_FINCH)

- **Antes:** NUMERO_AGENCIA era sempre `0001` quando havia movimento. NUMERO_CONTA = COALESCE(CONTA_SPB, CUS_CUST_ID).
- **Agora:**
  - **NUMERO_CONTA:** inalterado — COALESCE(CONTA_SPB, CUS_CUST_ID).
  - **NUMERO_AGENCIA:** quando o titular tem **CONTA_SPB vazio** → `001`; quando tem CONTA_SPB preenchido → `0001`.  
As linhas de extrato de contas MP sem AVK_ID passam a levar agência 001 de forma explícita.

### 5. Tabela de Titulares (TBL_QS_TITULARES_FINCH)

- **Antes:** NUMERO_AGENCIA era sempre `0001`. NUMERO_CONTA = COALESCE(CONTA_SPB, CUS_CUST_ID).
- **Agora:**
  - **NUMERO_CONTA:** inalterado — COALESCE(CONTA_SPB, CUS_CUST_ID).
  - **NUMERO_AGENCIA:** quando **CONTA_SPB está vazio** → `001`; quando preenchido → `0001`.  
Os titulares com conta MP sem AVK_ID ficam com agência 001 e conta = CUS_CUST_ID.

### 6. Origem e Destino (TBL_QS_ORIGEM_DESTINO_FINCH)

- **Sem alteração** em relação à Versão Original. A lógica de relacionados e placeholders (9999, 99999999999999999999, NAO-CORRENTISTA) permanece a mesma.

### 7. Referência ISPB

- **ISPB 10573521** (Mercado Pago - Instituição de Pagamento) é a referência oficial; as tabelas atuais do step 003 não possuem coluna ISPB nos INSERTs. A alteração documenta e prepara o uso dos placeholders (agência 001, COMPE 323, nome completo) alinhados a essa instituição; se no futuro for criada coluna ISPB, o valor a ser usado é 10573521.

---

## Resumo para o email

**Antes:** Contas Mercado Pago sem AVK_ID (CONTA_SPB vazio) já eram identificadas por CUS_CUST_ID no número da conta, mas a agência era sempre 0001 e o nome da instituição era apenas “Mercado Pago”, sem distinção explícita para o caso “conta MP sem AVK”.

**Agora:** Quando a conta é Mercado Pago e CONTA_SPB está vazio, passamos a aplicar placeholders padrão da instituição: **agência 001** (banco digital), **COMPE 323**, **nome “Mercado Pago - Instituição de Pagamento”** (e referência ISPB 10573521). A identificação da conta continua sendo **CUS_CUST_ID** nesses casos. A alteração está apenas no step 003, em um arquivo separado (**003 - inserir tabelas finais - Placeholders MP sem AVK**), permitindo comparar e reverter usando a Versão Original quando necessário.
