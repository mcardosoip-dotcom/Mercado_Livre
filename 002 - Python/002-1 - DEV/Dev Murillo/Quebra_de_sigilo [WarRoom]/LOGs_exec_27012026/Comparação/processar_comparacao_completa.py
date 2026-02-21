"""
Script completo para processar análises e atualizar HTML principal
"""

import pandas as pd
from pathlib import Path
import re

BASE_DIR = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
ANALISES_DIR = BASE_DIR / "Analises"
ANALISE_ORIGINAL = ANALISES_DIR / "Analise Original QS.xlsx"
ANALISE_POC = ANALISES_DIR / "Analise POC QS.xlsx"
HTML_PRINCIPAL = BASE_DIR / "Comparação" / "Comparacao_Versao_Original_vs_POC.html"

def format_number(val):
    """Formata número para exibição"""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, float)):
        if abs(val) >= 1000000:
            return f"{val/1000000:.2f}M"
        elif abs(val) >= 1000:
            return f"{val/1000:.2f}K"
        else:
            return f"{val:,.0f}" if val == int(val) else f"{val:,.2f}"
    return str(val)

def format_percent(val):
    """Formata percentual"""
    if pd.isna(val):
        return "N/A"
    return f"{val:.2f}%"

def processar_analises():
    """Processa os Excel e retorna HTML da comparação"""
    
    try:
        # Ler Original
        print("📥 Lendo Analise Original QS.xlsx...")
        original_data = pd.read_excel(ANALISE_ORIGINAL, sheet_name=None, engine='openpyxl')
        orig_df = list(original_data.values())[0]
        print(f"   ✅ {len(orig_df)} linhas, {len(orig_df.columns)} colunas")
        
        # Ler POC
        print("📥 Lendo Analise POC QS.xlsx...")
        poc_data = pd.read_excel(ANALISE_POC, sheet_name=None, engine='openpyxl')
        poc_df = list(poc_data.values())[0]
        print(f"   ✅ {len(poc_df)} linhas, {len(poc_df.columns)} colunas")
        
        # Garantir que as colunas são as mesmas
        common_cols = set(orig_df.columns) & set(poc_df.columns)
        print(f"\n📊 Comparando {len(common_cols)} colunas comuns...")
        
        html_parts = []
        html_parts.append("""
            <div class="section">
                <h2 class="section-title">📈 Comparação Detalhada das Análises</h2>
                <div class="info-box">
                    <h4>📊 Resumo da Comparação</h4>
                    <p>Comparação realizada entre os arquivos <strong>Analise Original QS.xlsx</strong> e <strong>Analise POC QS.xlsx</strong> gerados com os mesmos inputs.</p>
                    <p style="margin-top: 10px;"><strong>Total de tabelas analisadas:</strong> """ + str(len(orig_df)) + """</p>
                    <p><strong>Métricas comparadas:</strong> """ + str(len([c for c in common_cols if c not in ['NOME_TABELA', 'DESCRICAO']])) + """</p>
                </div>
""")
        
        # Comparar por tabela
        for idx in range(len(orig_df)):
            if idx >= len(poc_df):
                break
                
            row_orig = orig_df.iloc[idx]
            row_poc = poc_df.iloc[idx]
            
            nome_tabela = row_orig.get('NOME_TABELA', f'Tabela {idx+1}')
            descricao = row_orig.get('DESCRICAO', '')
            
            html_parts.append(f"""
                <div class="info-box">
                    <h4>📋 {nome_tabela}</h4>
                    <p><em>{descricao}</em></p>
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
            
            # Comparar todas as colunas numéricas
            comparacoes = []
            for col in sorted(common_cols):
                if col in ['NOME_TABELA', 'DESCRICAO']:
                    continue
                
                val_orig = row_orig.get(col, 0)
                val_poc = row_poc.get(col, 0)
                
                # Converter para numérico se necessário
                try:
                    val_orig = float(val_orig) if pd.notna(val_orig) else 0
                    val_poc = float(val_poc) if pd.notna(val_poc) else 0
                except:
                    continue
                
                diff = val_poc - val_orig
                
                # Calcular diferença percentual
                if val_orig != 0:
                    diff_pct = (diff / val_orig) * 100
                elif val_poc != 0:
                    diff_pct = 100.0  # POC tem valor, Original não
                else:
                    diff_pct = 0.0  # Ambos zero
                
                # Determinar status
                if abs(diff_pct) < 0.01:
                    status = "✅ Igual"
                    status_class = "status-success"
                elif abs(diff_pct) < 0.1:
                    status = "✅ Muito próximo"
                    status_class = "status-success"
                elif abs(diff_pct) < 1:
                    status = "⚠️ Pequena diferença"
                    status_class = "status-warning"
                elif abs(diff_pct) < 5:
                    status = "⚠️ Diferença moderada"
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
            
            # Ordenar por diferença percentual absoluta
            comparacoes.sort(key=lambda x: abs(x['diff_pct']), reverse=True)
            
            for comp in comparacoes:
                # Formatar valores
                if 'PCT' in comp['col'].upper() or 'PERCENT' in comp['col'].upper() or 'MEDIA' in comp['col'].upper():
                    orig_str = format_percent(comp['orig'])
                    poc_str = format_percent(comp['poc'])
                    diff_str = f"{comp['diff']:+.4f}" if abs(comp['diff']) < 1 else format_number(comp['diff'])
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
                                <td>{comp['diff_pct']:+.4f}%</td>
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
        
        return ''.join(html_parts)
        
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return None

def atualizar_html_principal():
    """Atualiza o HTML principal com a comparação real"""
    
    print("\n" + "="*60)
    print("Processando análises e atualizando HTML...")
    print("="*60)
    
    # Processar análises
    html_comparacao = processar_analises()
    
    if not html_comparacao:
        print("❌ Não foi possível processar as análises")
        return
    
    # Ler HTML atual
    print("\n📄 Lendo HTML principal...")
    with open(HTML_PRINCIPAL, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Encontrar e substituir a seção de comparação
    # Procurar pela seção "Comparação de Análises"
    pattern = r'(<!-- Seção 4: Comparação de Análises -->.*?<!-- Seção 5: Observações)'
    
    nova_secao = '<!-- Seção 4: Comparação de Análises -->' + html_comparacao + '\n            <!-- Seção 5: Observações'
    
    html_atualizado = re.sub(pattern, nova_secao, html_content, flags=re.DOTALL)
    
    # Salvar HTML atualizado
    print("💾 Salvando HTML atualizado...")
    with open(HTML_PRINCIPAL, 'w', encoding='utf-8') as f:
        f.write(html_atualizado)
    
    print(f"\n✅ HTML atualizado com sucesso!")
    print(f"📄 Arquivo: {HTML_PRINCIPAL}")
    print("="*60)

if __name__ == "__main__":
    atualizar_html_principal()
