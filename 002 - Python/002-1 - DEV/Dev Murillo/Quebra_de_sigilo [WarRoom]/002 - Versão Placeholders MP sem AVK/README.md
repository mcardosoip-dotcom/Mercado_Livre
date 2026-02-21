# Versão Placeholders MP sem AVK

Versão alternativa ao pipeline da **000 - Versão Original**, com tratamento explícito de **contas Mercado Pago sem AVK_ID (CONTA_SPB vazio)** usando placeholders padrão da instituição.

## Uso

- **Steps 001 e 002:** utilizar os mesmos arquivos da pasta **000 - Versão Original** (`001 - Tabelas auxiliares` e `002 - Tabelas auxiliares 2`). Não há alteração nesses steps.
- **Step 003:** utilizar o arquivo **desta pasta**: `003 - inserir tabelas finais - Placeholders MP sem AVK` em substituição ao `003 - inserir tabelas finais` da Versão Original.

## Placeholders aplicados quando CONTA_SPB está vazio

| Campo / conceito | Valor |
|------------------|--------|
| Agência | 001 (banco digital) |
| Código COMPE | 323 |
| Nome da instituição | Mercado Pago - Instituição de Pagamento |
| ISPB | 10573521 (referência; não há coluna ISPB nos INSERTs atuais) |
| Identificação da conta (NUMERO_CONTA) | Mantida como **CUS_CUST_ID** quando CONTA_SPB é nulo |

## Comparação

Ver o documento **ANTES_DEPOIS_Placeholders_MP_sem_AVK.md** para o texto detalhado (antes x depois) para uso em email ou documentação.
