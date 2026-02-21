"""
Exemplo de uso da conexão com BigQuery
"""

from bigquery_connection import connect_bigquery
import pandas as pd

# ============================================
# CONFIGURAÇÃO
# ============================================

# Opção 1: Usar credenciais padrão do ambiente (Application Default Credentials)
# Configure as credenciais usando: gcloud auth application-default login
bq = connect_bigquery(project_id="seu-project-id-aqui")

# Opção 2: Usar arquivo de credenciais JSON
# bq = connect_bigquery(
#     credentials_path=r"C:\caminho\para\credentials.json",
#     project_id="seu-project-id-aqui"
# )

# ============================================
# EXEMPLOS DE USO
# ============================================

# 1. Executar query e obter DataFrame
print("\n=== Exemplo 1: Executar Query ===")
query = """
SELECT 
    column1,
    column2,
    COUNT(*) as total
FROM `project.dataset.table`
WHERE column1 IS NOT NULL
GROUP BY column1, column2
LIMIT 10
"""

try:
    df = bq.query_to_dataframe(query)
    print(f"Resultados: {len(df)} linhas")
    print(df.head())
except Exception as e:
    print(f"Erro: {e}")

# 2. Listar datasets disponíveis
print("\n=== Exemplo 2: Listar Datasets ===")
try:
    datasets = bq.list_datasets()
    print(f"Datasets encontrados: {len(datasets)}")
    for dataset in datasets:
        print(f"  - {dataset}")
except Exception as e:
    print(f"Erro: {e}")

# 3. Listar tabelas em um dataset
print("\n=== Exemplo 3: Listar Tabelas ===")
dataset_id = "seu-dataset-id"
try:
    tables = bq.list_tables(dataset_id)
    print(f"Tabelas no dataset '{dataset_id}': {len(tables)}")
    for table in tables:
        print(f"  - {table}")
except Exception as e:
    print(f"Erro: {e}")

# 4. Ver schema de uma tabela
print("\n=== Exemplo 4: Ver Schema ===")
dataset_id = "seu-dataset-id"
table_id = "sua-tabela-id"
try:
    schema = bq.get_table_schema(dataset_id, table_id)
    print(f"Schema da tabela {dataset_id}.{table_id}:")
    for field in schema:
        print(f"  - {field.name}: {field.field_type}")
except Exception as e:
    print(f"Erro: {e}")

# 5. Carregar DataFrame para BigQuery
print("\n=== Exemplo 5: Carregar DataFrame ===")
# Criar DataFrame de exemplo
df_exemplo = pd.DataFrame({
    'id': [1, 2, 3],
    'nome': ['João', 'Maria', 'Pedro'],
    'idade': [25, 30, 35]
})

dataset_id = "seu-dataset-id"
table_id = "sua-tabela-id"

try:
    # Carregar DataFrame para BigQuery
    # bq.load_dataframe_to_table(
    #     dataframe=df_exemplo,
    #     dataset_id=dataset_id,
    #     table_id=table_id,
    #     write_disposition='WRITE_TRUNCATE'  # ou 'WRITE_APPEND' para adicionar
    # )
    print("Exemplo comentado - descomente e ajuste os parâmetros para usar")
except Exception as e:
    print(f"Erro: {e}")

# 6. Executar query sem retornar DataFrame (para INSERT, UPDATE, DELETE, etc.)
print("\n=== Exemplo 6: Executar Query sem DataFrame ===")
query_insert = """
INSERT INTO `project.dataset.table` (col1, col2)
VALUES ('valor1', 'valor2')
"""

try:
    # job = bq.execute_query(query_insert)
    # print("Query executada com sucesso!")
    print("Exemplo comentado - descomente e ajuste a query para usar")
except Exception as e:
    print(f"Erro: {e}")

# Fechar conexão (opcional)
# bq.close()

print("\n✓ Exemplos concluídos!")


