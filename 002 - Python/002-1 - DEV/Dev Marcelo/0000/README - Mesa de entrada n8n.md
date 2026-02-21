# Workflow n8n: Mesa de entrada (MySQL → BigQuery)

Workflow equivalente ao processo Python em `P01 - Rotina/MAIN/CARGA DE TABELAS/Mesa de entrada`: extrai dados do MySQL (mesa_entrada) e carrega no BigQuery.

## O que o workflow faz

1. **Lista de tarefas (queries + tabelas BQ)** – Define as 11 consultas SQL e o nome da tabela de destino no BigQuery. Usa **VerdiCode** (Python) no ambiente Verdi. A versão em Python está em `tarefas.py` para referência.
2. **Loop** – Processa uma tarefa por vez (Split In Batches).
3. **BigQuery - Truncar tabela** – Limpa a tabela antes da carga (carga completa, equivalente ao fluxo Parquet).
4. **Passar contexto para MySQL** – Mantém `query` e `tableName` disponíveis para o MySQL.
5. **MySQL** – Executa a query no banco `mesa_entrada` (host 10.82.128.122).
6. **BigQuery - Carregar tabela** – Insere os dados na tabela correspondente no dataset `mesa_entrada`.
7. **Log** – Registra quantas linhas foram carregadas por tabela.

## Como usar no n8n

1. **Importar o workflow**  
   No n8n: Workflows → Import from File → selecione `Mesa de entrada - MySQL para BigQuery.json`.

2. **Credenciais MySQL**  
   - Crie uma credencial **MySQL** no n8n.  
   - Host: `10.82.128.122`  
   - Porta: `3306`  
   - Database: `mesa_entrada`  
   - User: `lhub_readonly`  
   - Password: (a mesma usada no Python, ex.: variável de ambiente ou secret).  
   - Associe essa credencial ao nó **"MySQL - Extrair dados"**.

3. **Credenciais BigQuery**  
   - Crie uma credencial **Google BigQuery** (OAuth2 ou Service Account).  
   - Associe aos nós **"BigQuery - Truncar tabela"** e **"BigQuery - Carregar tabela"**.

4. **Project ID**  
   - O workflow já usa o projeto `ddme000426-gopr4nla6zo-furyid` (referência do `002 - Carga_Bucket.py`). Altere nos nós BigQuery se precisar de outro projeto.

5. **Dataset e tabelas no BigQuery**  
   - O workflow usa o dataset **`mesa_entrada`**. Crie esse dataset no BigQuery se ainda não existir.  
   - As tabelas podem ser criadas na primeira execução (se o BigQuery estiver configurado para isso) ou você pode criar antes com o schema desejado. Nomes das tabelas:  
     `vista_entradas`, `dw_hist_casos_x_estado`, `tab_entradas`, `vista_cantidad_casos_usuarios`, `vista_usuarios`, `v_metricas_qa`, `estados`, `tipo_documentos`, `metricas_big_query`, `origenes`, `entradas_estados`.

6. **Executar**  
   - Use o trigger **"Executar workflow"** (manual) ou troque por um **Schedule Trigger** (ex.: diário) se quiser automatizar.

## Diferenças em relação ao Python

- **Python**: MySQL → Parquet → upload para GCS (buckets prod/dev).  
- **n8n**: MySQL → BigQuery direto (sem Parquet nem GCS).  
- Se precisar também do upload para GCS, dá para adicionar um branch no n8n com o nó **Google Cloud Storage** após o MySQL.

## Observações

- Os nós estão com **"Continue On Fail"** (onError: continueRegularOutput) para que uma falha em uma tabela não pare as demais.  
- Para cargas grandes, avalie usar **load job** no BigQuery (via HTTP/API no n8n) em vez de insert por linha; o nó atual faz insert por item (linha a linha ou em lote conforme o n8n).
