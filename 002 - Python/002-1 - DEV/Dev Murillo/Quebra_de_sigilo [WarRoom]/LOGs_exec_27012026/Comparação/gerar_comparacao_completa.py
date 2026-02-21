"""
Script para comparar execuções da Versão Original vs POC do Quebra de Sigilo
Gera relatório HTML com duas tabelas separadas e comparação de análises
"""

import re
from datetime import datetime
from pathlib import Path
import pandas as pd

# Configurações
BASE_DIR = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
LOGS_ORIGINAL = BASE_DIR / "LOGS-Versão Original"
LOGS_POC = BASE_DIR / "LOGS-Versão POC"
ANALISES_DIR = BASE_DIR / "Analises"
ANALISE_ORIGINAL = ANALISES_DIR / "Analise Original QS.xlsx"
ANALISE_POC = ANALISES_DIR / "Analise POC QS.xlsx"
OUTPUT_DIR = BASE_DIR / "Comparação"
OUTPUT_HTML = OUTPUT_DIR / "Comparacao_Versao_Original_vs_POC.html"

OUTPUT_DIR.mkdir(exist_ok=True)


def parse_log_file(log_file):
    """Extrai informações de performance de um arquivo de log"""
    data = {
        'start_time': None,
        'end_time': None,
        'duration_seconds': 0,
        'total_cost': 0.0,
        'query_count': 0,
        'status': 'UNKNOWN',
        'queries': []
    }
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Erro ao ler {log_file}: {e}")
        return data
    
    times = []
    costs = []
    
    for line in lines:
        # Extrair timestamps
        time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if time_match:
            try:
                times.append(datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S'))
            except:
                pass
        
        # Extrair custos
        cost_match = re.search(r'COST-BQ-EXECUTE: \$([\d.]+)', line)
        if cost_match:
            try:
                costs.append(float(cost_match.group(1)))
            except:
                pass
        
        # Status
        if 'FINISH' in line or 'Finished correctly' in line:
            data['status'] = 'SUCCESS'
        elif 'ERROR' in line or 'FAILED' in line:
            data['status'] = 'ERROR'
    
    if times:
        data['start_time'] = min(times)
        data['end_time'] = max(times)
        if data['start_time'] and data['end_time']:
            delta = data['end_time'] - data['start_time']
            data['duration_seconds'] = delta.total_seconds()
    
    data['total_cost'] = sum(costs)
    data['query_count'] = len(costs)
    
    return data


def parse_all_logs():
    """Processa todos os logs de ambas as versões"""
    original_logs = {}
    poc_logs = {}
    
    # Processar logs da versão original
    if LOGS_ORIGINAL.exists():
        for log_file in sorted(LOGS_ORIGINAL.glob("*.txt")):
            name = log_file.stem
            original_logs[name] = parse_log_file(log_file)
    
    # Processar logs da versão POC
    if LOGS_POC.exists():
        for log_file in sorted(LOGS_POC.glob("*.txt")):
            name = log_file.stem
            poc_logs[name] = parse_log_file(log_file)
    
    return original_logs, poc_logs


def read_analysis_excel(excel_file):
    """Lê arquivo Excel de análise e retorna DataFrame"""
    if not excel_file.exists():
        return None
    
    try:
        # Tentar ler todas as abas
        excel_data = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
        return excel_data
    except Exception as e:
        print(f"Erro ao ler {excel_file}: {e}")
        try:
            # Tentar ler apenas a primeira aba
            df = pd.read_excel(excel_file, engine='openpyxl')
            return {'Sheet1': df}
        except:
            return None


def format_duration(seconds):
    """Formata duração em formato legível"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        minutes = (seconds % 3600) / 60
        return f"{int(hours)}h {int(minutes)}min"


def format_cost(cost):
    """Formata custo em dólares"""
    if cost < 0.01:
        return f"${cost:.8f}"
    elif cost < 1:
        return f"${cost:.6f}"
    else:
        return f"${cost:.2f}"


def generate_html_report(original_logs, poc_logs, original_analysis, poc_analysis):
    """Gera relatório HTML de comparação"""
    
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparação: Versão Original vs POC - Quebra de Sigilo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .metric-card {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
            min-width: 200px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .metric-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .metric-card .value {
            font-size: 2em;
            font-weight: bold;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
        }
        .info-box h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .status-success {
            color: #28a745;
            font-weight: bold;
        }
        .status-error {
            color: #dc3545;
            font-weight: bold;
        }
        .comparison-table {
            font-size: 0.95em;
        }
        .table-container {
            margin: 30px 0;
        }
        .table-title {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 15px;
            font-weight: 600;
        }
        ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        li {
            margin-bottom: 8px;
        }
        small {
            font-size: 0.85em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Comparação: Versão Original vs POC</h1>
            <p>Quebra de Sigilo - Análise de Performance e Resultados</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Data: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
        </div>
        <div class="content">
"""
    
    # Seção 1: Resumo Executivo
    html += """
            <div class="section">
                <h2 class="section-title">📊 Resumo Executivo</h2>
                <div class="summary-grid">
"""
    
    # Calcular totais
    total_original_time = sum(log.get('duration_seconds', 0) for log in original_logs.values())
    total_poc_time = sum(log.get('duration_seconds', 0) for log in poc_logs.values())
    total_original_cost = sum(log.get('total_cost', 0) for log in original_logs.values())
    total_poc_cost = sum(log.get('total_cost', 0) for log in poc_logs.values())
    total_original_queries = sum(log.get('query_count', 0) for log in original_logs.values())
    total_poc_queries = sum(log.get('query_count', 0) for log in poc_logs.values())
    
    html += f"""
                    <div class="metric-card">
                        <h3>Tempo Total - Original</h3>
                        <div class="value">{format_duration(total_original_time)}</div>
                        <p style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">{len(original_logs)} etapas</p>
                    </div>
                    <div class="metric-card">
                        <h3>Tempo Total - POC</h3>
                        <div class="value">{format_duration(total_poc_time)}</div>
                        <p style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">{len(poc_logs)} blocos</p>
                    </div>
                    <div class="metric-card">
                        <h3>Custo Total - Original</h3>
                        <div class="value">{format_cost(total_original_cost)}</div>
                        <p style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">{total_original_queries} queries</p>
                    </div>
                    <div class="metric-card">
                        <h3>Custo Total - POC</h3>
                        <div class="value">{format_cost(total_poc_cost)}</div>
                        <p style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">{total_poc_queries} queries</p>
                    </div>
"""
    
    html += """
                </div>
            </div>
"""
    
    # Seção 2: Tabela Versão Original
    html += """
            <div class="section">
                <h2 class="section-title">📋 Versão Original - Performance por Etapa</h2>
                <div class="table-container">
                    <div class="table-title">Detalhamento das Etapas da Versão Original</div>
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Etapa</th>
                                <th>Status</th>
                                <th>Duração</th>
                                <th>Custo Total</th>
                                <th>Nº Queries</th>
                                <th>Início</th>
                                <th>Fim</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    for etapa_name in sorted(original_logs.keys()):
        log = original_logs[etapa_name]
        status_class = 'status-success' if log.get('status') == 'SUCCESS' else 'status-error'
        status_text = log.get('status', 'UNKNOWN')
        
        start_str = log['start_time'].strftime('%d/%m/%Y %H:%M:%S') if log.get('start_time') else 'N/A'
        end_str = log['end_time'].strftime('%d/%m/%Y %H:%M:%S') if log.get('end_time') else 'N/A'
        
        html += f"""
                            <tr>
                                <td><strong>{etapa_name}</strong></td>
                                <td class="{status_class}">{status_text}</td>
                                <td>{format_duration(log.get('duration_seconds', 0))}</td>
                                <td>{format_cost(log.get('total_cost', 0))}</td>
                                <td>{log.get('query_count', 0)}</td>
                                <td><small>{start_str}</small></td>
                                <td><small>{end_str}</small></td>
                            </tr>
"""
    
    html += """
                        </tbody>
                    </table>
                </div>
            </div>
"""
    
    # Seção 3: Tabela Versão POC
    html += """
            <div class="section">
                <h2 class="section-title">📋 Versão POC - Performance por Bloco</h2>
                <div class="table-container">
                    <div class="table-title">Detalhamento dos Blocos da Versão POC</div>
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Bloco</th>
                                <th>Descrição</th>
                                <th>Status</th>
                                <th>Duração</th>
                                <th>Custo Total</th>
                                <th>Nº Queries</th>
                                <th>Início</th>
                                <th>Fim</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    # Descrições dos blocos
    blocos_desc = {
        'BLOCO_01 - Preparacao_Base_Investigados': 'Preparação da base de investigados a partir da planilha',
        'BLOCO_02 - Coleta_Informacoes_Reguladas': 'Coleta de informações da base regulada LK_REG_REGULATED_BASE_MLB',
        'BLOCO_03 - Processamento_Titulares2': 'Processamento de titulares e identificação de correspondentes',
        'BLOCO_04 - Coleta_Movimentacoes': 'Coleta de movimentações financeiras no período',
        'BLOCO_05 - Processamento_Relacionados': 'Processamento de relacionados (Payout, Payin, Payments, Withdrawal)',
        'BLOCO_06 - Consolidacao_Relacionados': 'Consolidação de todos os relacionados em uma única tabela',
        'BLOCO_07 - Insercao_Tabelas_Finais': 'Inserção nas tabelas finais para geração de arquivos'
    }
    
    for etapa_name in sorted(poc_logs.keys()):
        log = poc_logs[etapa_name]
        status_class = 'status-success' if log.get('status') == 'SUCCESS' else 'status-error'
        status_text = log.get('status', 'UNKNOWN')
        descricao = blocos_desc.get(etapa_name, 'Processamento de dados')
        
        start_str = log['start_time'].strftime('%d/%m/%Y %H:%M:%S') if log.get('start_time') else 'N/A'
        end_str = log['end_time'].strftime('%d/%m/%Y %H:%M:%S') if log.get('end_time') else 'N/A'
        
        html += f"""
                            <tr>
                                <td><strong>{etapa_name.replace('BLOCO_', '').replace('_', ' ')}</strong></td>
                                <td><small>{descricao}</small></td>
                                <td class="{status_class}">{status_text}</td>
                                <td>{format_duration(log.get('duration_seconds', 0))}</td>
                                <td>{format_cost(log.get('total_cost', 0))}</td>
                                <td>{log.get('query_count', 0)}</td>
                                <td><small>{start_str}</small></td>
                                <td><small>{end_str}</small></td>
                            </tr>
"""
    
    html += """
                        </tbody>
                    </table>
                </div>
            </div>
"""
    
    # Seção 4: Comparação de Análises
    html += """
            <div class="section">
                <h2 class="section-title">📈 Comparação de Análises das Tabelas Finais</h2>
"""
    
    if original_analysis and poc_analysis:
        # Comparar abas comuns
        common_sheets = set(original_analysis.keys()) & set(poc_analysis.keys())
        
        if common_sheets:
            for sheet_name in sorted(common_sheets):
                df_orig = original_analysis[sheet_name]
                df_poc = poc_analysis[sheet_name]
                
                html += f"""
                    <div class="info-box">
                        <h4>{sheet_name}</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>Métrica</th>
                                    <th>Versão Original</th>
                                    <th>Versão POC</th>
                                    <th>Diferença</th>
                                    <th>% Diferença</th>
                                </tr>
                            </thead>
                            <tbody>
"""
                
                # Comparar colunas numéricas comuns
                numeric_cols = set(df_orig.select_dtypes(include=['number']).columns) & \
                              set(df_poc.select_dtypes(include=['number']).columns)
                
                for col in sorted(numeric_cols)[:15]:  # Limitar a 15 colunas
                    val_orig = df_orig[col].sum() if len(df_orig) > 0 else 0
                    val_poc = df_poc[col].sum() if len(df_poc) > 0 else 0
                    diff = val_poc - val_orig
                    diff_pct = (diff / val_orig * 100) if val_orig != 0 else 0
                    
                    diff_class = 'status-success' if abs(diff_pct) < 1 else 'status-error' if abs(diff_pct) > 10 else ''
                    
                    html += f"""
                                <tr>
                                    <td><strong>{col}</strong></td>
                                    <td>{val_orig:,.0f}</td>
                                    <td>{val_poc:,.0f}</td>
                                    <td class="{diff_class}">{diff:+,.0f}</td>
                                    <td class="{diff_class}">{diff_pct:+.2f}%</td>
                                </tr>
"""
                
                html += """
                            </tbody>
                        </table>
                    </div>
"""
        else:
            html += """
                <div class="info-box">
                    <p>As análises não possuem abas comuns para comparação direta.</p>
                    <p>Por favor, verifique os arquivos Excel manualmente:</p>
                    <ul>
                        <li><strong>Analise Original QS.xlsx</strong></li>
                        <li><strong>Analise POC QS.xlsx</strong></li>
                    </ul>
                </div>
"""
    else:
        html += """
                <div class="info-box">
                    <p>Arquivos de análise não disponíveis ou não puderam ser lidos.</p>
                    <p>Arquivos esperados:</p>
                    <ul>
                        <li><strong>Analise Original QS.xlsx</strong></li>
                        <li><strong>Analise POC QS.xlsx</strong></li>
                    </ul>
                </div>
"""
    
    html += """
            </div>
"""
    
    # Seção 5: Observações
    html += """
            <div class="section">
                <h2 class="section-title">📝 Observações e Conclusões</h2>
                <div class="info-box">
                    <h4>Principais Diferenças Identificadas:</h4>
                    <ul>
                        <li><strong>Arquitetura Modular:</strong> A versão POC utiliza uma arquitetura modular com blocos separados (BLOCO_01 a BLOCO_07), facilitando manutenção, depuração e monitoramento individual de cada etapa</li>
                        <li><strong>Coleta de Informações Reguladas:</strong> Melhorias na coleta usando LK_REG_REGULATED_BASE_MLB como fonte única consolidada, substituindo múltiplas consultas</li>
                        <li><strong>Processamento de Relacionados:</strong> Otimizações no processamento com tabelas particionadas para PIX e melhor tratamento de dados</li>
                        <li><strong>Filtro de Movimentações:</strong> Uso de DATA_ABERTURA como data inicial para movimentações, evitando buscas desnecessárias antes da criação da conta</li>
                        <li><strong>Consolidação:</strong> Processo de consolidação de relacionados mais eficiente com UNION DISTINCT otimizado</li>
                    </ul>
                </div>
                <div class="info-box">
                    <h4>Recomendações:</h4>
                    <ul>
                        <li><strong>Validação de Dados:</strong> Analisar as diferenças nas análises das tabelas finais para garantir que os resultados sejam equivalentes entre as versões</li>
                        <li><strong>Validação de Performance:</strong> Validar que todas as melhorias de performance não comprometem a qualidade dos dados</li>
                        <li><strong>Migração:</strong> Considerar a migração completa para a versão POC após validação completa dos resultados</li>
                        <li><strong>Monitoramento:</strong> Implementar monitoramento individual de cada bloco para facilitar identificação de problemas</li>
                    </ul>
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Função principal"""
    print("=" * 60)
    print("Comparação: Versão Original vs POC - Quebra de Sigilo")
    print("=" * 60)
    
    print("\nProcessando logs...")
    original_logs, poc_logs = parse_all_logs()
    
    print(f"\nLogs Original: {len(original_logs)} arquivos")
    for name in sorted(original_logs.keys()):
        log = original_logs[name]
        print(f"  - {name}: {format_duration(log.get('duration_seconds', 0))}, {format_cost(log.get('total_cost', 0))}")
    
    print(f"\nLogs POC: {len(poc_logs)} arquivos")
    for name in sorted(poc_logs.keys()):
        log = poc_logs[name]
        print(f"  - {name}: {format_duration(log.get('duration_seconds', 0))}, {format_cost(log.get('total_cost', 0))}")
    
    print("\nLendo análises...")
    original_analysis = read_analysis_excel(ANALISE_ORIGINAL)
    poc_analysis = read_analysis_excel(ANALISE_POC)
    
    if original_analysis:
        print(f"Análise Original: {len(original_analysis)} abas")
    if poc_analysis:
        print(f"Análise POC: {len(poc_analysis)} abas")
    
    print("\nGerando relatório HTML...")
    html = generate_html_report(original_logs, poc_logs, original_analysis, poc_analysis)
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ Relatório gerado com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_HTML}")
    print(f"🌐 Abra no navegador para visualizar")
    print("=" * 60)


if __name__ == "__main__":
    main()
