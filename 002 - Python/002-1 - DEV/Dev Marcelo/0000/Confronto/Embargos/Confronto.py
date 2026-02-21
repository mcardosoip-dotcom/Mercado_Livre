"""
Script de Consolidação de Arquivos eLAW Contencioso
Autor: Marcelo Cardoso
Data: 2026-01-06

Objetivo:
    Consolidar arquivos parquet de Contencioso concatenando os arquivos atuais
    com os arquivos legados, e gerar um arquivo Excel de mapeamento com exemplos.
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# ================================================
# CONFIGURAÇÕES DE CAMINHOS
# ================================================

# Pasta de origem 1: Arquivos atuais
PASTA_ORIGEM_ATUAL = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW"

# Pasta de origem 2: Arquivos legados
PASTA_ORIGEM_LEGADO = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE\Legado_eLAW\Parquet"

# Pasta de destino: Onde serão salvos os arquivos consolidados
PASTA_DESTINO = r"H:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Marcelo\0000\Confronto"

# Pasta raiz do script: Onde o arquivo Python está localizado (para salvar os arquivos Excel)
PASTA_RAIZ_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Nomes fixos dos arquivos Excel (não devem mudar)
NOME_ARQUIVO_MAPEAMENTO = "Mapeamento_Colunas_Confronto.xlsx"
NOME_ARQUIVO_ANALISE = "Analise_Colunas_Confronto.xlsx"

# ================================================
# MAPEAMENTO DE ARQUIVOS
# ================================================

# Arquivos que serão consolidados (atual + legado)
ARQUIVOS_CONSOLIDAR = {
    "Database_eLAW_Contencioso_Brasil_Incoming": {
        "atual": "Database_eLAW_Contencioso_Brasil_Incoming.parquet",
        "legado": "Database_eLAW_Contencioso_Brasil_Incoming_legado.parquet"
    },
    "Database_eLAW_Contencioso_Brasil_Outgoing": {
        "atual": "Database_eLAW_Contencioso_Brasil_Outgoing.parquet",
        "legado": "Database_eLAW_Contencioso_Brasil_Outgoing_legado.parquet"
    },
    "Database_eLAW_Contencioso_Hispanos_Incoming": {
        "atual": "Database_eLAW_Contencioso_Hispanos_Incoming.parquet",
        "legado": "Database_eLAW_Contencioso_Hispanos_Incoming_legado.parquet"
    },
    "Database_eLAW_Contencioso_Hispanos_Outgoing": {
        "atual": "Database_eLAW_Contencioso_Hispanos_Outgoing.parquet",
        "legado": "Database_eLAW_Contencioso_Hispanos_Outgoing_legado.parquet"
    }
}

# Arquivos que serão apenas copiados (não têm versão legada)
ARQUIVOS_COPIAR = {
    "Database_eLAW_Contencioso_Brasil_Ongoing": "Database_eLAW_Contencioso_Brasil_Ongoing.parquet",
    "Database_eLAW_Contencioso_Hispanos_Ongoing": "Database_eLAW_Contencioso_Hispanos_Ongoing.parquet"
}

# ================================================
# FUNÇÕES AUXILIARES
# ================================================

def criar_pasta_se_nao_existir(caminho):
    """Cria a pasta se ela não existir."""
    Path(caminho).mkdir(parents=True, exist_ok=True)


def consolidar_arquivos(nome_base, caminho_atual, caminho_legado, caminho_destino):
    """
    Consolida dois arquivos parquet concatenando-os.
    
    Args:
        nome_base: Nome base do arquivo (sem extensão)
        caminho_atual: Caminho do arquivo atual
        caminho_legado: Caminho do arquivo legado
        caminho_destino: Caminho onde salvar o arquivo consolidado
    
    Returns:
        DataFrame consolidado ou None se houver erro
    """
    try:
        print(f"\n[LENDO] Arquivo atual: {os.path.basename(caminho_atual)}")
        df_atual = pd.read_parquet(caminho_atual)
        print(f"   [OK] Linhas no arquivo atual: {len(df_atual):,}")
        
        print(f"[LENDO] Arquivo legado: {os.path.basename(caminho_legado)}")
        df_legado = pd.read_parquet(caminho_legado)
        print(f"   [OK] Linhas no arquivo legado: {len(df_legado):,}")
        
        # Verifica compatibilidade de colunas
        colunas_atual = set(df_atual.columns)
        colunas_legado = set(df_legado.columns)
        
        if colunas_atual != colunas_legado:
            print(f"   [ATENCAO] Diferenças nas colunas detectadas!")
            apenas_atual = colunas_atual - colunas_legado
            apenas_legado = colunas_legado - colunas_atual
            if apenas_atual:
                print(f"      Colunas apenas no atual: {apenas_atual}")
            if apenas_legado:
                print(f"      Colunas apenas no legado: {apenas_legado}")
            print(f"   [INFO] Pandas ira alinhar automaticamente as colunas na concatenacao.")
        
        # Concatena os DataFrames
        print(f"[CONCATENANDO] Arquivos...")
        df_consolidado = pd.concat([df_atual, df_legado], ignore_index=True)
        print(f"   [OK] Total de linhas apos concatenacao: {len(df_consolidado):,}")
        
        # Converte colunas object que podem ter valores mistos (int/str) para string
        # Isso resolve problemas de compatibilidade ao salvar parquet
        print(f"[CONVERTENDO] Tipos de dados problemáticos...")
        for col in df_consolidado.columns:
            if df_consolidado[col].dtype == 'object':
                # Tenta converter para string, mantendo NaN como NaN
                df_consolidado[col] = df_consolidado[col].apply(
                    lambda x: str(x) if pd.notna(x) else None
                )
        
        # Salva o arquivo consolidado usando fastparquet como fallback se pyarrow falhar
        nome_saida = f"{nome_base}_consolidado.parquet"
        caminho_saida = os.path.join(caminho_destino, nome_saida)
        
        print(f"[SALVANDO] Arquivo consolidado: {nome_saida}")
        try:
            df_consolidado.to_parquet(caminho_saida, index=False, engine='pyarrow')
        except Exception as e1:
            print(f"   [AVISO] PyArrow falhou, tentando fastparquet: {e1}")
            try:
                df_consolidado.to_parquet(caminho_saida, index=False, engine='fastparquet')
            except Exception as e2:
                print(f"   [ERRO] Ambos os engines falharam: {e2}")
                raise
        print(f"   [OK] Arquivo salvo com sucesso!")
        
        return df_consolidado
        
    except FileNotFoundError as e:
        print(f"   [ERRO] Arquivo nao encontrado: {e}")
        return None
    except Exception as e:
        print(f"   [ERRO] Erro ao consolidar: {e}")
        return None


def copiar_arquivo(nome_arquivo, caminho_origem, caminho_destino):
    """
    Copia um arquivo da origem para o destino.
    
    Args:
        nome_arquivo: Nome do arquivo
        caminho_origem: Pasta de origem
        caminho_destino: Pasta de destino
    
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        caminho_completo_origem = os.path.join(caminho_origem, nome_arquivo)
        caminho_completo_destino = os.path.join(caminho_destino, nome_arquivo)
        
        if not os.path.exists(caminho_completo_origem):
            print(f"   [ERRO] Arquivo nao encontrado: {caminho_completo_origem}")
            return False
        
        print(f"[COPIANDO] Arquivo: {nome_arquivo}")
        import shutil
        shutil.copy2(caminho_completo_origem, caminho_completo_destino)
        print(f"   [OK] Arquivo copiado com sucesso!")
        return True
        
    except Exception as e:
        print(f"   [ERRO] Erro ao copiar: {e}")
        return False


def criar_arquivo_mapeamento(pasta_raiz_script, arquivos_consolidados):
    """
    Cria um arquivo Excel com mapeamento das colunas e 10 linhas de exemplo.
    
    Args:
        pasta_raiz_script: Pasta raiz do script onde salvar o arquivo Excel
        arquivos_consolidados: Dicionário com nome do arquivo e DataFrame correspondente
    """
    try:
        caminho_excel = os.path.join(pasta_raiz_script, NOME_ARQUIVO_MAPEAMENTO)
        
        print(f"\n[CRIANDO] Arquivo de mapeamento: {NOME_ARQUIVO_MAPEAMENTO}")
        
        with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer:
            # Contador para evitar nomes duplicados
            contador_abas = {}
            
            for nome_arquivo, df in arquivos_consolidados.items():
                if df is None or df.empty:
                    continue
                
                # Cria nome da aba mais curto e único
                # Remove prefixo comum e limita tamanho
                nome_aba_base = nome_arquivo.replace("Database_eLAW_Contencioso_", "")
                if nome_aba_base.endswith("_consolidado"):
                    nome_aba_base = nome_aba_base.replace("_consolidado", "")
                
                # Limita o nome da aba (Excel tem limite de 31 caracteres)
                nome_aba = nome_aba_base[:31] if len(nome_aba_base) > 31 else nome_aba_base
                
                # Garante unicidade
                if nome_aba in contador_abas:
                    contador_abas[nome_aba] += 1
                    nome_aba = f"{nome_aba[:27]}_{contador_abas[nome_aba]}"
                else:
                    contador_abas[nome_aba] = 1
                
                # Cria um DataFrame com informações de mapeamento
                # Primeira parte: Informações gerais
                info_geral = pd.DataFrame({
                    'Informação': ['Nome do Arquivo', 'Total de Linhas', 'Total de Colunas', 'Data de Consolidação'],
                    'Valor': [nome_arquivo, len(df), len(df.columns), datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
                })
                
                # Segunda parte: Lista de colunas
                colunas_df = pd.DataFrame({
                    'Número': range(1, len(df.columns) + 1),
                    'Nome da Coluna': df.columns.tolist(),
                    'Tipo de Dados': [str(dtype) for dtype in df.dtypes]
                })
                
                # Terceira parte: 10 linhas de exemplo
                exemplo_df = df.head(10).copy()
                
                # Escreve cada parte em uma aba separada ou combina tudo
                # Vamos criar uma estrutura mais organizada
                dados_mapeamento = []
                
                # Adiciona informações gerais
                dados_mapeamento.append(pd.DataFrame([['Nome do Arquivo', nome_arquivo]]))
                dados_mapeamento.append(pd.DataFrame([['Total de Linhas', len(df)]]))
                dados_mapeamento.append(pd.DataFrame([['Total de Colunas', len(df.columns)]]))
                dados_mapeamento.append(pd.DataFrame([['Data de Consolidação', datetime.now().strftime("%d/%m/%Y %H:%M:%S")]]))
                dados_mapeamento.append(pd.DataFrame([[]]))  # Linha em branco
                
                # Adiciona cabeçalho da lista de colunas
                dados_mapeamento.append(pd.DataFrame([['LISTA DE COLUNAS']]))
                dados_mapeamento.append(pd.DataFrame([['Número', 'Nome da Coluna', 'Tipo de Dados']]))
                
                # Adiciona lista de colunas
                for idx, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
                    dados_mapeamento.append(pd.DataFrame([[idx, col, str(dtype)]]))
                
                dados_mapeamento.append(pd.DataFrame([[]]))  # Linha em branco
                dados_mapeamento.append(pd.DataFrame([['EXEMPLO DE DADOS (10 primeiras linhas)']]))
                
                # Combina tudo
                df_info = pd.concat(dados_mapeamento, ignore_index=True)
                
                # Adiciona as 10 linhas de exemplo abaixo
                df_final = pd.concat([df_info, exemplo_df], ignore_index=True)
                
                # Escreve na aba
                df_final.to_excel(writer, sheet_name=nome_aba, index=False, header=False)
                
                print(f"   [OK] Aba '{nome_aba}' criada com sucesso!")
        
        print(f"   [OK] Arquivo Excel criado com sucesso: {caminho_excel}")
        
    except Exception as e:
        print(f"   [ERRO] Erro ao criar arquivo de mapeamento: {e}")
        import traceback
        traceback.print_exc()


def encontrar_coluna_processo_id(df):
    """
    Encontra a coluna de processo_id de forma case-insensitive.
    
    Args:
        df: DataFrame para buscar a coluna
    
    Returns:
        Nome da coluna encontrada ou None
    """
    # Busca case-insensitive
    for col in df.columns:
        if col.lower() == 'processo_id':
            return col
    return None


def criar_analise_colunas(pasta_raiz_script, df_final, nome_arquivo="Consolidado_Final"):
    """
    Cria um arquivo Excel com análise detalhada das colunas.
    
    Para cada coluna, mostra:
    - Total de registros
    - Quantidade de valores nulos
    - Quantidade de valores não-nulos
    - Percentual preenchido
    - Quantidade de valores únicos
    - Lista de valores únicos (se < 20)
    
    Args:
        pasta_raiz_script: Pasta raiz do script onde salvar o arquivo Excel
        df_final: DataFrame consolidado final para análise
        nome_arquivo: Nome do arquivo para identificar na análise
    """
    try:
        if df_final is None or df_final.empty:
            print(f"   [AVISO] DataFrame vazio ou None, nao e possivel criar analise de colunas.")
            return
        
        caminho_excel = os.path.join(pasta_raiz_script, NOME_ARQUIVO_ANALISE)
        
        print(f"\n[CRIANDO] Arquivo de analise de colunas: {NOME_ARQUIVO_ANALISE}")
        
        # Lista para armazenar os dados de análise
        dados_analise = []
        
        total_registros = len(df_final)
        
        print(f"[ANALISANDO] {len(df_final.columns)} colunas...")
        
        for col in df_final.columns:
            # Conta valores nulos e não-nulos
            valores_nulos = df_final[col].isna().sum()
            valores_nao_nulos = total_registros - valores_nulos
            percentual_preenchido = (valores_nao_nulos / total_registros * 100) if total_registros > 0 else 0
            
            # Conta valores únicos (excluindo nulos)
            valores_unicos_count = df_final[col].nunique()
            
            # Se tiver menos de 20 valores únicos, lista todos
            valores_unicos_lista = ""
            if valores_unicos_count < 20:
                valores_unicos = df_final[col].dropna().unique().tolist()
                # Limita o tamanho de cada valor para não exceder o limite do Excel
                valores_formatados = []
                for val in valores_unicos:
                    val_str = str(val)
                    if len(val_str) > 100:  # Limita a 100 caracteres por valor
                        val_str = val_str[:97] + "..."
                    valores_formatados.append(val_str)
                valores_unicos_lista = "; ".join(valores_formatados)
            else:
                valores_unicos_lista = f"({valores_unicos_count} valores únicos - >= 20)"
            
            # Adiciona à lista de análise
            dados_analise.append({
                'Nome da Coluna': col,
                'Total de Registros': total_registros,
                'Valores Nulos': valores_nulos,
                'Valores Não-Nulos': valores_nao_nulos,
                '% Preenchido': f"{percentual_preenchido:.2f}%",
                'Valores Únicos': valores_unicos_count,
                'Valores Únicos (< 20)': valores_unicos_lista
            })
        
        # Cria DataFrame com a análise
        df_analise = pd.DataFrame(dados_analise)
        
        # Salva em Excel
        with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer:
            # Cria nome da aba (limita a 31 caracteres)
            nome_aba = nome_arquivo.replace("Database_eLAW_Contencioso_", "")
            nome_aba = nome_aba[:31] if len(nome_aba) > 31 else nome_aba
            
            # Adiciona informações gerais no topo
            info_geral = pd.DataFrame({
                'Informação': ['Nome do Arquivo', 'Total de Linhas', 'Total de Colunas', 'Data de Análise'],
                'Valor': [nome_arquivo, total_registros, len(df_final.columns), datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
            })
            
            # Escreve informações gerais e análise na mesma aba
            info_geral.to_excel(writer, sheet_name=nome_aba, index=False, startrow=0)
            df_analise.to_excel(writer, sheet_name=nome_aba, index=False, startrow=len(info_geral) + 2)
            
            print(f"   [OK] Aba '{nome_aba}' criada com sucesso!")
        
        print(f"   [OK] Arquivo Excel de analise criado com sucesso: {caminho_excel}")
        
    except Exception as e:
        print(f"   [ERRO] Erro ao criar arquivo de analise de colunas: {e}")
        import traceback
        traceback.print_exc()


# ================================================
# FUNÇÃO PRINCIPAL
# ================================================

def main():
    """Função principal que executa todo o processo de consolidação."""
    
    print("=" * 70)
    print("CONSOLIDAÇÃO DE ARQUIVOS eLAW CONTENCIOSO")
    print("=" * 70)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Cria pasta de destino se não existir
    criar_pasta_se_nao_existir(PASTA_DESTINO)
    print(f"[PASTA] Destino: {PASTA_DESTINO}")
    
    # Dicionário para armazenar DataFrames consolidados (para o mapeamento)
    arquivos_consolidados = {}
    
    # ============================================
    # ETAPA 1: Consolidar arquivos (atual + legado)
    # ============================================
    print("\n" + "=" * 70)
    print("ETAPA 1: CONSOLIDAÇÃO DE ARQUIVOS")
    print("=" * 70)
    
    for nome_base, arquivos in ARQUIVOS_CONSOLIDAR.items():
        caminho_atual = os.path.join(PASTA_ORIGEM_ATUAL, arquivos["atual"])
        caminho_legado = os.path.join(PASTA_ORIGEM_LEGADO, arquivos["legado"])
        
        df_consolidado = consolidar_arquivos(nome_base, caminho_atual, caminho_legado, PASTA_DESTINO)
        arquivos_consolidados[nome_base] = df_consolidado
    
    # ============================================
    # ETAPA 2: Copiar arquivos sem versão legada
    # ============================================
    print("\n" + "=" * 70)
    print("ETAPA 2: CÓPIA DE ARQUIVOS SEM VERSÃO LEGADA")
    print("=" * 70)
    
    for nome_base, nome_arquivo in ARQUIVOS_COPIAR.items():
        copiar_arquivo(nome_arquivo, PASTA_ORIGEM_ATUAL, PASTA_DESTINO)
        
        # Lê o arquivo copiado para incluir no mapeamento
        caminho_arquivo = os.path.join(PASTA_DESTINO, nome_arquivo)
        if os.path.exists(caminho_arquivo):
            try:
                df = pd.read_parquet(caminho_arquivo)
                arquivos_consolidados[nome_base] = df
            except Exception as e:
                print(f"   [AVISO] Nao foi possivel ler o arquivo para mapeamento: {e}")
    
    # ============================================
    # ETAPA 3: Consolidar todos os arquivos e remover duplicatas por processo_id
    # ============================================
    print("\n" + "=" * 70)
    print("ETAPA 3: CONSOLIDAÇÃO FINAL E REMOÇÃO DE DUPLICATAS")
    print("=" * 70)
    
    # Lista todos os arquivos parquet na pasta de destino
    arquivos_parquet = []
    for arquivo in os.listdir(PASTA_DESTINO):
        if arquivo.endswith('.parquet') and arquivo != 'Database_eLAW_Contencioso_Consolidado_Final.parquet':
            caminho_completo = os.path.join(PASTA_DESTINO, arquivo)
            arquivos_parquet.append(caminho_completo)
    
    # Inicializa df_final como None
    df_final = None
    
    if not arquivos_parquet:
        print("   [AVISO] Nenhum arquivo parquet encontrado para consolidacao final.")
    else:
        print(f"[LENDO] {len(arquivos_parquet)} arquivos parquet para consolidacao final...")
        
        lista_dataframes = []
        total_linhas_antes = 0
        
        for caminho_arquivo in arquivos_parquet:
            try:
                nome_arquivo = os.path.basename(caminho_arquivo)
                print(f"   [LENDO] {nome_arquivo}...")
                df = pd.read_parquet(caminho_arquivo)
                total_linhas_antes += len(df)
                lista_dataframes.append(df)
                print(f"      [OK] {len(df):,} linhas")
            except Exception as e:
                print(f"      [ERRO] Erro ao ler {nome_arquivo}: {e}")
        
        if lista_dataframes:
            print(f"\n[CONCATENANDO] Todos os arquivos...")
            df_final = pd.concat(lista_dataframes, ignore_index=True)
            print(f"   [OK] Total de linhas apos concatenacao: {len(df_final):,}")
            
            # Converte colunas object para string se necessário
            print(f"[CONVERTENDO] Tipos de dados...")
            for col in df_final.columns:
                if df_final[col].dtype == 'object':
                    df_final[col] = df_final[col].apply(
                        lambda x: str(x) if pd.notna(x) else None
                    )
            
            # Verifica se a coluna processo_id existe (case-insensitive)
            coluna_processo_id = encontrar_coluna_processo_id(df_final)
            if coluna_processo_id is None:
                print(f"   [AVISO] Coluna 'processo_id' (ou 'Processo_id') nao encontrada no DataFrame!")
                print(f"   [INFO] Colunas disponiveis: {list(df_final.columns)[:10]}...")
                print(f"   [INFO] Arquivo sera salvo sem remover duplicatas por processo_id.")
            else:
                print(f"\n[REMOVENDO] Duplicatas por {coluna_processo_id}...")
                linhas_antes = len(df_final)
                
                # Remove duplicatas mantendo a primeira ocorrência
                df_final = df_final.drop_duplicates(subset=[coluna_processo_id], keep='first')
                
                linhas_depois = len(df_final)
                duplicatas_removidas = linhas_antes - linhas_depois
                
                print(f"   [OK] Linhas antes: {linhas_antes:,}")
                print(f"   [OK] Linhas depois: {linhas_depois:,}")
                print(f"   [OK] Duplicatas removidas: {duplicatas_removidas:,}")
            
            # Salva o arquivo final consolidado
            nome_final = "Database_eLAW_Contencioso_Consolidado_Final.parquet"
            caminho_final = os.path.join(PASTA_DESTINO, nome_final)
            
            print(f"\n[SALVANDO] Arquivo final consolidado: {nome_final}")
            try:
                df_final.to_parquet(caminho_final, index=False, engine='pyarrow')
            except Exception as e1:
                print(f"   [AVISO] PyArrow falhou, tentando fastparquet: {e1}")
                try:
                    df_final.to_parquet(caminho_final, index=False, engine='fastparquet')
                except Exception as e2:
                    print(f"   [ERRO] Ambos os engines falharam: {e2}")
                    raise
            
            print(f"   [OK] Arquivo final salvo com sucesso!")
            print(f"   [INFO] Total de linhas no arquivo final: {len(df_final):,}")
            
            # Adiciona o DataFrame final ao dicionário para o mapeamento
            arquivos_consolidados['Consolidado_Final'] = df_final
    
    # ============================================
    # ETAPA 4: Criar arquivo de mapeamento
    # ============================================
    print("\n" + "=" * 70)
    print("ETAPA 4: CRIAÇÃO DO ARQUIVO DE MAPEAMENTO")
    print("=" * 70)
    
    # Filtra apenas os DataFrames válidos
    arquivos_validos = {k: v for k, v in arquivos_consolidados.items() if v is not None and not v.empty}
    
    if arquivos_validos:
        criar_arquivo_mapeamento(PASTA_RAIZ_SCRIPT, arquivos_validos)
    else:
        print("   [AVISO] Nenhum arquivo valido para criar o mapeamento.")
    
    # ============================================
    # ETAPA 5: Criar análise de colunas
    # ============================================
    print("\n" + "=" * 70)
    print("ETAPA 5: CRIAÇÃO DA ANÁLISE DE COLUNAS")
    print("=" * 70)
    
    if df_final is not None and not df_final.empty:
        criar_analise_colunas(PASTA_RAIZ_SCRIPT, df_final, "Database_eLAW_Contencioso_Consolidado_Final")
    else:
        print("   [AVISO] DataFrame final nao disponivel para criar analise de colunas.")
    
    # ============================================
    # RESUMO FINAL
    # ============================================
    print("\n" + "=" * 70)
    print("RESUMO FINAL")
    print("=" * 70)
    
    arquivos_sucesso = sum(1 for v in arquivos_consolidados.values() if v is not None and not v.empty)
    arquivos_total = len(arquivos_consolidados)
    
    print(f"[OK] Arquivos processados com sucesso: {arquivos_sucesso}/{arquivos_total}")
    print(f"[PASTA] Destino: {PASTA_DESTINO}")
    print(f"[ARQUIVO] Mapeamento: {os.path.join(PASTA_RAIZ_SCRIPT, NOME_ARQUIVO_MAPEAMENTO)}")
    print(f"[ARQUIVO] Analise de Colunas: {os.path.join(PASTA_RAIZ_SCRIPT, NOME_ARQUIVO_ANALISE)}")
    
    # Verifica se o arquivo final foi criado
    arquivo_final = os.path.join(PASTA_DESTINO, "Database_eLAW_Contencioso_Consolidado_Final.parquet")
    if os.path.exists(arquivo_final):
        try:
            df_final_check = pd.read_parquet(arquivo_final)
            print(f"[ARQUIVO] Final consolidado: Database_eLAW_Contencioso_Consolidado_Final.parquet ({len(df_final_check):,} linhas)")
        except:
            pass
    
    print("\n[SUCESSO] Processo concluido!")


if __name__ == "__main__":
    main()
