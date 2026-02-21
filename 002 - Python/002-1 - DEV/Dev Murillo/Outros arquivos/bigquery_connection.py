"""
Módulo para conexão com Google BigQuery
"""

from google.cloud import bigquery
from google.cloud.bigquery import DatasetReference
from google.oauth2 import service_account
import pandas as pd
import os
from typing import Optional


class BigQueryConnection:
    """
    Classe para gerenciar conexões com BigQuery
    """
    
    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        """
        Inicializa a conexão com BigQuery
        
        Args:
            credentials_path: Caminho para o arquivo JSON de credenciais do Google Cloud
                             Se None, usa as credenciais padrão do ambiente
            project_id: ID do projeto do Google Cloud. Se None, usa o padrão das credenciais
        """
        self.credentials_path = credentials_path
        self.project_id = project_id
        self.client = None
        self._connect()
    
    def _connect(self):
        """Estabelece a conexão com BigQuery"""
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                # Usa credenciais de arquivo JSON
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                if self.project_id:
                    self.client = bigquery.Client(credentials=credentials, project=self.project_id)
                else:
                    self.client = bigquery.Client(credentials=credentials)
            else:
                # Usa credenciais padrão do ambiente (Application Default Credentials)
                if self.project_id:
                    self.client = bigquery.Client(project=self.project_id)
                else:
                    self.client = bigquery.Client()
            
            # Valida a conexão tentando acessar o projeto
            _ = self.client.project
            print("✓ Conexão com BigQuery estabelecida com sucesso!")
            print(f"  Projeto: {self.client.project}")
            
        except FileNotFoundError as e:
            error_msg = f"Arquivo de credenciais não encontrado: {self.credentials_path}"
            print(f"✗ {error_msg}")
            raise FileNotFoundError(error_msg) from e
        except Exception as e:
            error_msg = f"Erro ao conectar com BigQuery: {str(e)}"
            print(f"✗ {error_msg}")
            print("  Verifique:")
            print("  - Se as credenciais estão corretas")
            print("  - Se o project_id está correto")
            print("  - Se você tem permissões no projeto")
            raise Exception(error_msg) from e
    
    def execute_query(self, query: str, use_legacy_sql: bool = False) -> bigquery.QueryJob:
        """
        Executa uma query SQL no BigQuery
        
        Args:
            query: Query SQL a ser executada
            use_legacy_sql: Se True, usa SQL legado (padrão: False)
        
        Returns:
            QueryJob object
        """
        if not self.client:
            raise Exception("Cliente BigQuery não inicializado")
        
        job_config = bigquery.QueryJobConfig(use_legacy_sql=use_legacy_sql)
        query_job = self.client.query(query, job_config=job_config)
        
        # Aguarda a conclusão do job
        query_job.result()
        
        return query_job
    
    def query_to_dataframe(self, query: str, use_legacy_sql: bool = False) -> pd.DataFrame:
        """
        Executa uma query SQL e retorna os resultados como DataFrame do pandas
        
        Args:
            query: Query SQL a ser executada
            use_legacy_sql: Se True, usa SQL legado (padrão: False)
        
        Returns:
            DataFrame com os resultados da query
        """
        query_job = self.execute_query(query, use_legacy_sql)
        return query_job.to_dataframe()
    
    def list_datasets(self) -> list:
        """
        Lista todos os datasets no projeto
        
        Returns:
            Lista de datasets
        """
        if not self.client:
            raise Exception("Cliente BigQuery não inicializado")
        
        datasets = list(self.client.list_datasets())
        return [dataset.dataset_id for dataset in datasets]
    
    def list_tables(self, dataset_id: str) -> list:
        """
        Lista todas as tabelas em um dataset
        
        Args:
            dataset_id: ID do dataset
        
        Returns:
            Lista de tabelas
        """
        if not self.client:
            raise Exception("Cliente BigQuery não inicializado")
        
        dataset_ref = DatasetReference(self.client.project, dataset_id)
        tables = list(self.client.list_tables(dataset_ref))
        return [table.table_id for table in tables]
    
    def get_table_schema(self, dataset_id: str, table_id: str) -> list:
        """
        Retorna o schema de uma tabela
        
        Args:
            dataset_id: ID do dataset
            table_id: ID da tabela
        
        Returns:
            Lista de campos do schema
        """
        if not self.client:
            raise Exception("Cliente BigQuery não inicializado")
        
        table_ref = DatasetReference(self.client.project, dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        return table.schema
    
    def load_dataframe_to_table(self, 
                                dataframe: pd.DataFrame, 
                                dataset_id: str, 
                                table_id: str,
                                write_disposition: str = 'WRITE_TRUNCATE',
                                create_disposition: str = 'CREATE_IF_NEEDED') -> bigquery.LoadJob:
        """
        Carrega um DataFrame do pandas para uma tabela no BigQuery
        
        Args:
            dataframe: DataFrame do pandas a ser carregado
            dataset_id: ID do dataset de destino
            table_id: ID da tabela de destino
            write_disposition: 'WRITE_TRUNCATE', 'WRITE_APPEND' ou 'WRITE_EMPTY'
            create_disposition: 'CREATE_IF_NEEDED' ou 'CREATE_NEVER'
        
        Returns:
            LoadJob object
        """
        if not self.client:
            raise Exception("Cliente BigQuery não inicializado")
        
        table_ref = DatasetReference(self.client.project, dataset_id).table(table_id)
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            create_disposition=create_disposition,
            autodetect=True  # Detecta o schema automaticamente
        )
        
        load_job = self.client.load_table_from_dataframe(
            dataframe, table_ref, job_config=job_config
        )
        
        # Aguarda a conclusão do job
        load_job.result()
        
        print(f"✓ Dados carregados com sucesso na tabela {dataset_id}.{table_id}")
        print(f"  Linhas carregadas: {load_job.output_rows}")
        
        return load_job
    
    def close(self):
        """Fecha a conexão (BigQuery client não precisa ser fechado explicitamente)"""
        self.client = None
        print("Conexão com BigQuery fechada")


# Função auxiliar para uso rápido
def connect_bigquery(credentials_path: Optional[str] = None, project_id: Optional[str] = None) -> BigQueryConnection:
    """
    Função auxiliar para criar uma conexão com BigQuery rapidamente
    
    Args:
        credentials_path: Caminho para o arquivo JSON de credenciais
        project_id: ID do projeto do Google Cloud
    
    Returns:
        BigQueryConnection object
    
    Example:
        >>> bq = connect_bigquery(credentials_path="path/to/credentials.json", project_id="my-project")
        >>> df = bq.query_to_dataframe("SELECT * FROM dataset.table LIMIT 10")
    """
    return BigQueryConnection(credentials_path=credentials_path, project_id=project_id)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo 1: Usando credenciais padrão do ambiente
    # bq = connect_bigquery(project_id="seu-project-id")
    
    # Exemplo 2: Usando arquivo de credenciais
    # bq = connect_bigquery(
    #     credentials_path="path/to/credentials.json",
    #     project_id="seu-project-id"
    # )
    
    # Exemplo 3: Executar query e obter DataFrame
    # df = bq.query_to_dataframe("SELECT * FROM `dataset.table` LIMIT 10")
    # print(df.head())
    
    # Exemplo 4: Listar datasets
    # datasets = bq.list_datasets()
    # print("Datasets:", datasets)
    
    # Exemplo 5: Listar tabelas em um dataset
    # tables = bq.list_tables("dataset_id")
    # print("Tabelas:", tables)
    
    print("Módulo de conexão BigQuery criado com sucesso!")
    print("\nPara usar:")
    print("1. Instale as dependências: pip install google-cloud-bigquery pandas")
    print("2. Configure as credenciais do Google Cloud")
    print("3. Importe e use: from bigquery_connection import connect_bigquery")


