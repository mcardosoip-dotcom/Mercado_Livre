import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# Diretório onde estão as bases
diretorio_bases = r"C:\Users\mcard\Desktop\eLAW Bases"

# Nomes das bases a procurar (parcial - sem o número variável no final)
nomes_bases = [
    "Extracao_de_Informacoes_Multas_Procon_(Ativos)",
    "Tarefas_Agendamento_Clean_-_Confirmados_2025",
    "Tarefas_Agendamento_Clean_-_Pendentes_2025"
]

# Diretório para salvar o resultado
diretorio_saida = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Marcelo\eLAW\Validação corte em bases"

# Campos de data específicos para cada tipo de arquivo
CAMPOS_DATA_AGENDAMENTOS = [
    "Data Audiencia Inicial",
    "Data de Agendamento da Tarefa",
    "Data de Confirmação",
    "Data Registrado"
]

CAMPOS_DATA_MULTAS = [
    "Data",
    "Data Registrado"
]

def encontrar_arquivos(diretorio, nomes_parciais):
    """
    Encontra arquivos que contenham os nomes parciais especificados.
    """
    arquivos_encontrados = {}
    
    if not os.path.exists(diretorio):
        print(f"❌ Diretório não encontrado: {diretorio}")
        return arquivos_encontrados
    
    # Lista todos os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        
        # Verifica se é um arquivo Excel
        if arquivo.lower().endswith(('.xlsx', '.xls')):
            # Verifica se o nome do arquivo contém algum dos nomes procurados
            for nome_base in nomes_parciais:
                if nome_base.lower() in arquivo.lower():
                    arquivos_encontrados[nome_base] = caminho_completo
                    print(f"✅ Arquivo encontrado: {arquivo}")
                    break
    
    return arquivos_encontrados

def identificar_colunas_data(df, nome_base):
    """
    Identifica colunas de data específicas baseadas no tipo de arquivo.
    """
    colunas_data_encontradas = []
    
    # Determina quais campos procurar baseado no tipo de arquivo
    if "Extracao_de_Informacoes_Multas" in nome_base:
        campos_procurar = CAMPOS_DATA_MULTAS
    elif "Tarefas_Agendamento" in nome_base:
        campos_procurar = CAMPOS_DATA_AGENDAMENTOS
    else:
        # Fallback: procura por qualquer coluna com "data"
        campos_procurar = None
    
    # Busca pelos campos específicos
    if campos_procurar:
        for campo in campos_procurar:
            # Busca exata (case insensitive) ou parcial
            for col in df.columns:
                col_str = str(col).strip()
                # Compara exatamente (case insensitive) ou verifica se contém
                if col_str.lower() == campo.lower() or campo.lower() in col_str.lower():
                    if col not in colunas_data_encontradas:
                        colunas_data_encontradas.append(col)
                        break
    else:
        # Fallback: procura por qualquer coluna com "data"
        for col in df.columns:
            if 'data' in str(col).lower():
                colunas_data_encontradas.append(col)
    
    return colunas_data_encontradas

def extrair_min_max_datas(df, coluna):
    """
    Extrai a data mínima e máxima de uma coluna.
    """
    try:
        # Tenta converter para datetime
        serie_datas = pd.to_datetime(df[coluna], errors='coerce')
        
        # Remove valores nulos
        serie_datas_validas = serie_datas.dropna()
        
        if len(serie_datas_validas) == 0:
            return None, None, 0
        
        data_min = serie_datas_validas.min()
        data_max = serie_datas_validas.max()
        total_registros = len(serie_datas_validas)
        
        return data_min, data_max, total_registros
    
    except Exception as e:
        print(f"  ⚠️ Erro ao processar coluna {coluna}: {e}")
        return None, None, 0

def processar_arquivo(caminho_arquivo, nome_base):
    """
    Processa um arquivo Excel e retorna informações sobre colunas de data.
    """
    resultados = []
    
    try:
        print(f"\n📂 Processando: {os.path.basename(caminho_arquivo)}")
        
        # Tenta ler o arquivo (alguns arquivos eLAW têm skiprows=5)
        try:
            df = pd.read_excel(caminho_arquivo, skiprows=5)
            print(f"  ✅ Arquivo lido com skiprows=5")
        except:
            try:
                df = pd.read_excel(caminho_arquivo)
                print(f"  ✅ Arquivo lido sem skiprows")
            except Exception as e:
                print(f"  ❌ Erro ao ler arquivo: {e}")
                return resultados
        
        # Identifica colunas com DATA específicas para este tipo de arquivo
        colunas_data = identificar_colunas_data(df, nome_base)
        
        if not colunas_data:
            print(f"  ⚠️ Nenhuma coluna de data específica encontrada")
            return resultados
        
        print(f"  📊 Colunas de data encontradas: {len(colunas_data)}")
        print(f"  📋 Campos procurados: {colunas_data}")
        
        # Processa cada coluna de data
        for coluna in colunas_data:
            data_min, data_max, total_registros = extrair_min_max_datas(df, coluna)
            
            if data_min is not None and data_max is not None:
                resultados.append({
                    'Base': nome_base,
                    'Arquivo': os.path.basename(caminho_arquivo),
                    'Coluna': coluna,
                    'Data_Minima': data_min,
                    'Data_Maxima': data_max,
                    'Total_Registros_Validos': total_registros
                })
                print(f"    ✓ {coluna}: Min={data_min.date()}, Max={data_max.date()}, Registros={total_registros}")
            else:
                resultados.append({
                    'Base': nome_base,
                    'Arquivo': os.path.basename(caminho_arquivo),
                    'Coluna': coluna,
                    'Data_Minima': None,
                    'Data_Maxima': None,
                    'Total_Registros_Validos': 0
                })
                print(f"    ⚠️ {coluna}: Sem datas válidas")
    
    except Exception as e:
        print(f"  ❌ Erro ao processar arquivo: {e}")
    
    return resultados

def main():
    """
    Função principal que executa todo o processo.
    """
    print("=" * 80)
    print("🔍 VALIDAÇÃO DE DATAS - BASES eLAW")
    print("=" * 80)
    
    # Encontra os arquivos
    print("\n📁 Procurando arquivos...")
    arquivos = encontrar_arquivos(diretorio_bases, nomes_bases)
    
    if not arquivos:
        print("\n❌ Nenhum arquivo encontrado!")
        return
    
    print(f"\n✅ Total de arquivos encontrados: {len(arquivos)}")
    
    # Processa cada arquivo
    todos_resultados = []
    
    for nome_base, caminho_arquivo in arquivos.items():
        resultados = processar_arquivo(caminho_arquivo, nome_base)
        todos_resultados.extend(resultados)
    
    # Cria DataFrame com os resultados
    if todos_resultados:
        df_resultado = pd.DataFrame(todos_resultados)
        
        # Formata as datas para exibição
        df_resultado['Data_Minima_Formatada'] = df_resultado['Data_Minima'].apply(
            lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else 'N/A'
        )
        df_resultado['Data_Maxima_Formatada'] = df_resultado['Data_Maxima'].apply(
            lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else 'N/A'
        )
        
        # Reordena colunas para melhor visualização
        colunas_ordenadas = [
            'Base', 'Arquivo', 'Coluna', 
            'Data_Minima', 'Data_Maxima',
            'Data_Minima_Formatada', 'Data_Maxima_Formatada',
            'Total_Registros_Validos'
        ]
        df_resultado = df_resultado[colunas_ordenadas]
        
        # Garante que o diretório de saída existe
        os.makedirs(diretorio_saida, exist_ok=True)
        
        # Salva o resultado
        nome_arquivo_saida = "Validacao_Datas_Bases.xlsx"
        caminho_saida = os.path.join(diretorio_saida, nome_arquivo_saida)
        
        df_resultado.to_excel(caminho_saida, index=False)
        
        print("\n" + "=" * 80)
        print("✅ PROCESSAMENTO CONCLUÍDO!")
        print("=" * 80)
        print(f"\n📊 Total de colunas processadas: {len(df_resultado)}")
        print(f"💾 Arquivo salvo em: {caminho_saida}")
        
        # Exibe resumo
        print("\n📋 RESUMO:")
        print(df_resultado[['Base', 'Coluna', 'Data_Minima_Formatada', 'Data_Maxima_Formatada', 'Total_Registros_Validos']].to_string(index=False))
    
    else:
        print("\n⚠️ Nenhum resultado encontrado!")

if __name__ == "__main__":
    main()

