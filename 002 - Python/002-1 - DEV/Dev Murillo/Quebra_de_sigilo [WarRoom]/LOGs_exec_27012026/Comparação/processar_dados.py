import pandas as pd
from pathlib import Path
import json

base = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
orig_df = pd.read_excel(base / "Analises" / "Analise Original QS.xlsx", engine='openpyxl')
poc_df = pd.read_excel(base / "Analises" / "Analise POC QS.xlsx", engine='openpyxl')

resultado = {}
for i in range(len(orig_df)):
    nome = orig_df.iloc[i]['NOME_TABELA']
    resultado[nome] = {}
    for col in orig_df.columns:
        if col not in ['NOME_TABELA', 'DESCRICAO']:
            try:
                o = float(orig_df.iloc[i][col]) if pd.notna(orig_df.iloc[i][col]) else 0
                p = float(poc_df.iloc[i][col]) if pd.notna(poc_df.iloc[i][col]) else 0
                resultado[nome][col] = {'original': o, 'poc': p, 'diff': p-o, 'diff_pct': ((p-o)/o*100) if o != 0 else 0}
            except:
                pass

with open(base / "Comparação" / "dados_comparacao.json", 'w', encoding='utf-8') as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("✅ Dados processados e salvos em dados_comparacao.json")
for nome in resultado:
    print(f"  - {nome}: {len(resultado[nome])} métricas")
