import pandas as pd
from pathlib import Path
import re

base = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
orig_df = pd.read_excel(base / "Analises" / "Analise Original QS.xlsx", engine='openpyxl')
poc_df = pd.read_excel(base / "Analises" / "Analise POC QS.xlsx", engine='openpyxl')

html_file = base / "Comparação" / "Comparacao_Versao_Original_vs_POC.html"

def format_num(val):
    if pd.isna(val):
        return "N/A"
    if abs(val) >= 1000000:
        return f"{val/1000000:.2f}M"
    elif abs(val) >= 1000:
        return f"{val/1000:.2f}K"
    return f"{val:,.0f}" if val == int(val) else f"{val:,.2f}"

# Gerar HTML de comparação
html_comparacao = []
html_comparacao.append("""
                <div class="info-box" style="background: #e7f3ff; border-left: 4px solid #0066cc;">
                    <h4 style="color: #0066cc;">📊 Comparação Real dos Dados</h4>
                    <p>Comparação realizada processando os arquivos Excel com os mesmos inputs.</p>
                </div>
""")

for i in range(len(orig_df)):
    row_o = orig_df.iloc[i]
    row_p = poc_df.iloc[i]
    
    nome_tabela = row_o['NOME_TABELA']
    descricao = row_o['DESCRICAO']
    
    html_comparacao.append(f"""
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
    for col in orig_df.columns:
        if col in ['NOME_TABELA', 'DESCRICAO']:
            continue
        
        val_o = row_o.get(col, 0)
        val_p = row_p.get(col, 0)
        
        try:
            val_o = float(val_o) if pd.notna(val_o) else 0
            val_p = float(val_p) if pd.notna(val_p) else 0
        except:
            continue
        
        diff = val_p - val_o
        diff_pct = (diff / val_o * 100) if val_o != 0 else (100 if val_p != 0 else 0)
        
        if abs(diff_pct) < 0.01:
            status = "✅ Igual"
            status_class = "status-success"
        elif abs(diff_pct) < 0.1:
            status = "✅ Muito próximo"
            status_class = "status-success"
        elif abs(diff_pct) < 1:
            status = "⚠️ Pequena diferença"
            status_class = "status-warning"
        else:
            status = "🔍 Diferença significativa"
            status_class = "status-error"
        
        comparacoes.append((col, val_o, val_p, diff, diff_pct, status, status_class))
    
    # Ordenar por diferença percentual
    comparacoes.sort(key=lambda x: abs(x[4]), reverse=True)
    
    for col, val_o, val_p, diff, diff_pct, status, status_class in comparacoes:
        if 'PCT' in col.upper() or 'MEDIA' in col.upper():
            orig_str = f"{val_o:.2f}%" if 'PCT' in col.upper() else f"{val_o:.2f}"
            poc_str = f"{val_p:.2f}%" if 'PCT' in col.upper() else f"{val_p:.2f}"
            diff_str = f"{diff:+.4f}" if abs(diff) < 1 else format_num(diff)
        else:
            orig_str = format_num(val_o)
            poc_str = format_num(val_p)
            diff_str = format_num(diff)
        
        html_comparacao.append(f"""
                            <tr>
                                <td><strong>{col}</strong></td>
                                <td>{orig_str}</td>
                                <td>{poc_str}</td>
                                <td>{diff_str}</td>
                                <td>{diff_pct:+.4f}%</td>
                                <td class="{status_class}">{status}</td>
                            </tr>
""")
    
    html_comparacao.append("""
                        </tbody>
                    </table>
                </div>
""")

html_comparacao_str = ''.join(html_comparacao)

# Ler HTML atual
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Encontrar e substituir a seção
pattern = r'(<div class="info-box">\s*<h4>📊 Resumo das Análises</h4>.*?<div class="info-box" style="background: #d4edda)'
replacement = r'<div class="info-box">\n                    <h4>📊 Resumo das Análises</h4>\n                    <p>As análises detalhadas das tabelas finais foram geradas executando a query <strong>RESUMO_TABELAS_FINAIS.sql</strong> sobre os resultados de ambas as versões, utilizando os mesmos inputs.</p>\n                    <p style="margin-top: 10px;"><strong>Arquivos disponíveis na pasta Analises:</strong></p>\n                    <ul>\n                        <li><strong>Analise Original QS.xlsx</strong> - Resultados da versão original</li>\n                        <li><strong>Analise POC QS.xlsx</strong> - Resultados da versão POC</li>\n                        <li><strong>Query.txt</strong> - Query SQL utilizada para gerar as análises</li>\n                    </ul>\n                </div>\n' + html_comparacao_str + '\n                <div class="info-box" style="background: #d4edda'

html_atualizado = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Salvar
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_atualizado)

print("✅ HTML atualizado com comparação real dos dados!")
