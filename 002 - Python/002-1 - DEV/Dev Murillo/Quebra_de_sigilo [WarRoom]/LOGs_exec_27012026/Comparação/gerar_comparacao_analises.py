"""
Script para processar e comparar as análises dos Excel e gerar HTML
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
ANALISES_DIR = BASE_DIR / "Analises"
ANALISE_ORIGINAL = ANALISES_DIR / "Analise Original QS.xlsx"
ANALISE_POC = ANALISES_DIR / "Analise POC QS.xlsx"
OUTPUT_HTML = BASE_DIR / "Comparação" / "Comparacao_Analises_Detalhada.html"

def format_number(val):
    """Formata número para exibição"""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, float)):
        if val >= 1000000:
            return f"{val/1000000:.2f}M"
        elif val >= 1000:
            return f"{val/1000:.2f}K"
        else:
            return f"{val:,.0f}" if val == int(val) else f"{val:,.2f}"
    return str(val)

def format_percent(val):
    """Formata percentual"""
    if pd.isna(val):
        return "N/A"
    return f"{val:.2f}%"

def processar_e_gerar_html():
    """Processa os Excel e gera HTML com comparação"""
    
    html_parts = []
    
    try:
        # Ler Original
        print("📥 Lendo Analise Original QS.xlsx...")
        original_data = pd.read_excel(ANALISE_ORIGINAL, sheet_name=None, engine='openpyxl')
        print(f"   ✅ {len(original_data)} abas encontradas")
        
        # Ler POC
        print("📥 Lendo Analise POC QS.xlsx...")
        poc_data = pd.read_excel(ANALISE_POC, sheet_name=None, engine='openpyxl')
        print(f"   ✅ {len(poc_data)} abas encontradas")
        
        # Comparar abas comuns
        common_sheets = set(original_data.keys()) & set(poc_data.keys())
        print(f"\n📊 Comparando {len(common_sheets)} abas comuns...")
        
        html_parts.append("""
            <div class="section">
                <h2 class="section-title">📈 Comparação Detalhada das Análises</h2>
                <p style="margin-bottom: 20px;">Comparação realizada entre os arquivos <strong>Analise Original QS.xlsx</strong> e <strong>Analise POC QS.xlsx</strong> gerados com os mesmos inputs.</p>
""")
        
        for sheet_name in sorted(common_sheets):
            df_orig = original_data[sheet_name]
            df_poc = poc_data[sheet_name]
            
            print(f"\n  📋 Processando aba: {sheet_name}")
            print(f"     Original: {len(df_orig)} linhas, {len(df_orig.columns)} colunas")
            print(f"     POC: {len(df_poc)} linhas, {len(df_poc.columns)} colunas")
            
            html_parts.append(f"""
                <div class="info-box">
                    <h4>📊 {sheet_name}</h4>
                    <p><strong>Linhas:</strong> Original: {len(df_orig)}, POC: {len(df_poc)}</p>
                    <table style="margin-top: 15px;">
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th>Versão Original</th>
                                <th>Versão POC</th>
                                <th>Diferença</th>
                                <th>% Diferença</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
""")
            
            # Comparar colunas numéricas
            numeric_cols = set(df_orig.select_dtypes(include=['number']).columns) & \
                          set(df_poc.select_dtypes(include=['number']).columns)
            
            # Também comparar colunas de texto que podem ter valores numéricos
            text_cols_orig = set(df_orig.select_dtypes(include=['object']).columns)
            text_cols_poc = set(df_poc.select_dtypes(include=['object']).columns)
            
            # Tentar converter colunas de texto que parecem numéricas
            for col in text_cols_orig & text_cols_poc:
                try:
                    # Tentar converter para numérico
                    df_orig[col + '_num'] = pd.to_numeric(df_orig[col], errors='coerce')
                    df_poc[col + '_num'] = pd.to_numeric(df_poc[col], errors='coerce')
                    if not df_orig[col + '_num'].isna().all():
                        numeric_cols.add(col)
                except:
                    pass
            
            comparacoes = []
            for col in sorted(numeric_cols):
                # Calcular totais ou médias dependendo do tipo de métrica
                if 'TOTAL' in col.upper() or 'QTD' in col.upper():
                    val_orig = df_orig[col].sum() if col in df_orig.columns else 0
                    val_poc = df_poc[col].sum() if col in df_poc.columns else 0
                elif 'PCT' in col.upper() or 'PERCENT' in col.upper() or 'MEDIA' in col.upper():
                    val_orig = df_orig[col].mean() if col in df_orig.columns and len(df_orig) > 0 else 0
                    val_poc = df_poc[col].mean() if col in df_poc.columns and len(df_poc) > 0 else 0
                else:
                    # Tentar ambos
                    val_orig = df_orig[col].sum() if col in df_orig.columns else 0
                    val_poc = df_poc[col].sum() if col in df_poc.columns else 0
                
                if pd.isna(val_orig):
                    val_orig = 0
                if pd.isna(val_poc):
                    val_poc = 0
                
                diff = val_poc - val_orig
                diff_pct = (diff / val_orig * 100) if val_orig != 0 else 0
                
                # Determinar status
                if abs(diff_pct) < 0.01:
                    status = "✅ Igual"
                    status_class = "status-success"
                elif abs(diff_pct) < 1:
                    status = "⚠️ Muito próximo"
                    status_class = "status-warning"
                elif abs(diff_pct) < 5:
                    status = "⚠️ Pequena diferença"
                    status_class = "status-warning"
                else:
                    status = "🔍 Diferença significativa"
                    status_class = "status-error"
                
                comparacoes.append({
                    'col': col,
                    'orig': val_orig,
                    'poc': val_poc,
                    'diff': diff,
                    'diff_pct': diff_pct,
                    'status': status,
                    'status_class': status_class
                })
            
            # Ordenar por diferença percentual absoluta (maiores diferenças primeiro)
            comparacoes.sort(key=lambda x: abs(x['diff_pct']), reverse=True)
            
            for comp in comparacoes:
                # Formatar valores
                if 'PCT' in comp['col'].upper() or 'PERCENT' in comp['col'].upper():
                    orig_str = format_percent(comp['orig'])
                    poc_str = format_percent(comp['poc'])
                    diff_str = f"{comp['diff']:+.2f}%"
                else:
                    orig_str = format_number(comp['orig'])
                    poc_str = format_number(comp['poc'])
                    diff_str = format_number(comp['diff'])
                
                html_parts.append(f"""
                            <tr>
                                <td><strong>{comp['col']}</strong></td>
                                <td>{orig_str}</td>
                                <td>{poc_str}</td>
                                <td>{diff_str}</td>
                                <td>{comp['diff_pct']:+.2f}%</td>
                                <td class="{comp['status_class']}">{comp['status']}</td>
                            </tr>
""")
            
            html_parts.append("""
                        </tbody>
                    </table>
                </div>
""")
        
        html_parts.append("""
            </div>
""")
        
        # Gerar HTML completo
        html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparação Detalhada das Análises - Original vs POC</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .info-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
        }}
        .info-box h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .status-success {{
            color: #28a745;
            font-weight: bold;
        }}
        .status-warning {{
            color: #ffc107;
            font-weight: bold;
        }}
        .status-error {{
            color: #dc3545;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Comparação Detalhada das Análises</h1>
            <p>Versão Original vs POC - Quebra de Sigilo</p>
        </div>
        <div class="content">
{''.join(html_parts)}
        </div>
    </div>
</body>
</html>
"""
        
        # Salvar HTML
        OUTPUT_HTML.parent.mkdir(exist_ok=True)
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        print(f"\n✅ HTML gerado com sucesso!")
        print(f"📄 Arquivo: {OUTPUT_HTML}")
        return OUTPUT_HTML
        
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    processar_e_gerar_html()
