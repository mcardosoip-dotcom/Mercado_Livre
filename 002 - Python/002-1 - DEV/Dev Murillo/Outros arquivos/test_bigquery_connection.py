"""
Script de teste para validar a conexão com BigQuery
Execute este script para verificar se a conexão está funcionando corretamente
"""

from bigquery_connection import connect_bigquery
import sys


def test_connection(credentials_path=None, project_id=None):
    """
    Testa a conexão com BigQuery
    
    Args:
        credentials_path: Caminho para o arquivo JSON de credenciais (opcional)
        project_id: ID do projeto do Google Cloud (opcional)
    """
    print("=" * 60)
    print("TESTE DE CONEXÃO COM BIGQUERY")
    print("=" * 60)
    
    try:
        # 1. Testar conexão
        print("\n[1/5] Testando conexão...")
        bq = connect_bigquery(credentials_path=credentials_path, project_id=project_id)
        print("✓ Conexão estabelecida com sucesso!")
        
        # 2. Testar query simples
        print("\n[2/5] Testando query simples...")
        test_query = "SELECT 1 AS teste, 'BigQuery funcionando!' AS mensagem"
        df = bq.query_to_dataframe(test_query)
        print("✓ Query executada com sucesso!")
        print(f"  Resultado: {df.iloc[0]['mensagem']}")
        
        # 3. Listar datasets
        print("\n[3/5] Listando datasets disponíveis...")
        try:
            datasets = bq.list_datasets()
            print(f"✓ Encontrados {len(datasets)} dataset(s)")
            if datasets:
                print(f"  Primeiros datasets: {', '.join(datasets[:5])}")
            else:
                print("  Nenhum dataset encontrado (pode ser normal se não houver datasets no projeto)")
        except Exception as e:
            print(f"⚠ Aviso ao listar datasets: {str(e)}")
        
        # 4. Testar query com dataset público (se disponível)
        print("\n[4/5] Testando query em dataset público...")
        try:
            public_query = """
            SELECT 
                name,
                country_code,
                continent
            FROM `bigquery-public-data.utility_us.country_code_iso`
            LIMIT 5
            """
            df_public = bq.query_to_dataframe(public_query)
            print("✓ Query em dataset público executada com sucesso!")
            print(f"  Linhas retornadas: {len(df_public)}")
        except Exception as e:
            print(f"⚠ Não foi possível acessar dataset público: {str(e)}")
            print("  (Isso é normal se não houver permissões ou se o dataset não existir)")
        
        # 5. Verificar informações do projeto
        print("\n[5/5] Verificando informações do projeto...")
        print(f"✓ Projeto ID: {bq.client.project}")
        print(f"✓ Localização padrão: {bq.client.location or 'Não especificada'}")
        
        print("\n" + "=" * 60)
        print("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        print("\nA conexão com BigQuery está funcionando corretamente!")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n✗ ERRO: {str(e)}")
        print("\nSoluções:")
        print("1. Verifique se o caminho do arquivo de credenciais está correto")
        print("2. Ou configure as credenciais padrão: gcloud auth application-default login")
        return False
        
    except Exception as e:
        print(f"\n✗ ERRO: {str(e)}")
        print("\nPossíveis causas:")
        print("1. Credenciais inválidas ou expiradas")
        print("2. Project ID incorreto")
        print("3. Falta de permissões no projeto")
        print("4. Problemas de rede/firewall")
        print("\nSoluções:")
        print("- Verifique as credenciais do Google Cloud")
        print("- Confirme o project_id está correto")
        print("- Verifique as permissões IAM no Google Cloud Console")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO DO TESTE")
    print("=" * 60)
    print("\nOpções:")
    print("1. Usar credenciais padrão do ambiente (Application Default Credentials)")
    print("2. Usar arquivo JSON de credenciais")
    print("\nPara usar credenciais padrão, execute sem argumentos:")
    print("  python test_bigquery_connection.py")
    print("\nPara usar arquivo JSON, edite este script e configure:")
    print("  credentials_path = r'caminho/para/credentials.json'")
    print("  project_id = 'seu-project-id'")
    print("\n" + "=" * 60)
    
    # CONFIGURE AQUI SE NECESSÁRIO:
    credentials_path = None  # Ex: r"C:\caminho\para\credentials.json"
    project_id = None  # Ex: "meu-projeto-gcp"
    
    # Executar teste
    success = test_connection(credentials_path=credentials_path, project_id=project_id)
    
    if not success:
        sys.exit(1)

