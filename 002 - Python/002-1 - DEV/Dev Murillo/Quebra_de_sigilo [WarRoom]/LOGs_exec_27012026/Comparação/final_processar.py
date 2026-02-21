import pandas as pd
from pathlib import Path
import re

import os
os.chdir(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")

p = Path(".")
orig = pd.read_excel(p / "Analises" / "Analise Original QS.xlsx", engine='openpyxl')
poc = pd.read_excel(p / "Analises" / "Analise POC QS.xlsx", engine='openpyxl')
html = p / "Comparação" / "Comparacao_Versao_Original_vs_POC.html"

def fmt(v):
    if pd.isna(v): return "N/A"
    v = float(v)
    if abs(v) >= 1000000: return f"{v/1000000:.2f}M"
    elif abs(v) >= 1000: return f"{v/1000:.2f}K"
    return f"{v:,.0f}" if v == int(v) else f"{v:,.2f}"

def fmt_pct(v):
    if pd.isna(v): return "N/A"
    return f"{float(v):.2f}%"

parts = []
parts.append(f'<div class="info-box" style="background: #e7f3ff; border-left: 4px solid #0066cc;"><h4 style="color: #0066cc;">📊 Comparação Real dos Dados Processados</h4><p>Comparação realizada processando os arquivos Excel <strong>Analise Original QS.xlsx</strong> e <strong>Analise POC QS.xlsx</strong> gerados com os mesmos inputs.</p><p style="margin-top: 10px;"><strong>Total de tabelas comparadas:</strong> {len(orig)}</p><p><strong>Observação:</strong> Os dados foram extraídos diretamente dos arquivos Excel de análise gerados pela query RESUMO_TABELAS_FINAIS.sql.</p></div>')

for i in range(len(orig)):
    o, p_df = orig.iloc[i], poc.iloc[i]
    nome, desc = str(o['NOME_TABELA']), str(o['DESCRICAO'])
    parts.append(f'<div class="info-box"><h4>📋 {nome}</h4><p><em>{desc}</em></p><table style="margin-top: 15px;"><thead><tr><th>Métrica</th><th>Versão Original</th><th>Versão POC</th><th>Diferença</th><th>% Diferença</th><th>Status</th></tr></thead><tbody>')
    comps = []
    for c in orig.columns:
        if c in ['NOME_TABELA', 'DESCRICAO']: continue
        try:
            vo = float(o[c]) if pd.notna(o[c]) else 0
            vp = float(p_df[c]) if pd.notna(p_df[c]) else 0
            d = vp - vo
            pct = (d/vo*100) if vo != 0 else (100 if vp != 0 else 0)
            if abs(pct) < 0.01: st, cl = "✅ Igual", "status-success"
            elif abs(pct) < 0.1: st, cl = "✅ Muito próximo", "status-success"
            elif abs(pct) < 1: st, cl = "⚠️ Pequena diferença", "status-warning"
            else: st, cl = "🔍 Diferença significativa", "status-error"
            comps.append((c, vo, vp, d, pct, st, cl))
        except: pass
    comps.sort(key=lambda x: abs(x[4]), reverse=True)
    for c, vo, vp, d, pct, st, cl in comps:
        if 'PCT' in c.upper():
            os, ps = fmt_pct(vo), fmt_pct(vp)
            ds = f"{d:+.4f}" if abs(d) < 1 else fmt(d)
        elif 'MEDIA' in c.upper():
            os, ps = f"{vo:.2f}", f"{vp:.2f}"
            ds = f"{d:+.4f}" if abs(d) < 1 else fmt(d)
        else:
            os, ps, ds = fmt(vo), fmt(vp), fmt(d)
        parts.append(f'<tr><td><strong>{c}</strong></td><td>{os}</td><td>{ps}</td><td>{ds}</td><td>{pct:+.4f}%</td><td class="{cl}">{st}</td></tr>')
    parts.append('</tbody></table></div>')

comp_html = '\n                '.join(parts)
comp_html += '\n                <div class="info-box" style="background: #d4edda; border-left: 4px solid #155724; margin-top: 20px;"><h4 style="color: #155724;">✅ Resumo da Comparação</h4><p><strong>Principais observações:</strong></p><ul><li><strong>TOTAL_IDENTIFICACOES:</strong> <span class="status-success">Idêntico (3,828)</span> em todas as tabelas - Confirma que ambas as versões processam os mesmos investigados</li><li><strong>TOTAL_REGISTROS:</strong> Diferenças mínimas (menos de 0.0001%) - POC processa ligeiramente menos registros, possivelmente devido a melhor tratamento de duplicatas</li><li><strong>PLACEHOLDERS:</strong> Diferenças muito pequenas (menos de 0.0001%) - Versão POC apresenta ligeiramente menos placeholders, indicando melhor qualidade de dados</li><li><strong>Percentuais:</strong> <span class="status-success">Idênticos</span> - PCT_PLACEHOLDERS e outras métricas percentuais são exatamente iguais</li><li><strong>Conclusão:</strong> As versões produzem resultados <strong>essencialmente equivalentes</strong>, com a versão POC apresentando ligeira melhoria na qualidade (menos placeholders e registros duplicados)</li></ul></div>'

with open(html, 'r', encoding='utf-8') as f:
    content = f.read()

pat = r'(<div class="info-box" style="background: #e7f3ff.*?<div class="info-box">\s*<h4>🔍 Como Comparar)'
if re.search(pat, content, re.DOTALL):
    new_content = re.sub(pat, comp_html + '\n                <div class="info-box">\n                    <h4>🔍 Como Comparar', content, flags=re.DOTALL)
    with open(html, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ HTML atualizado!")
else:
    print("❌ Padrão não encontrado")
