"""
Script para processar e comparar as análises dos Excel
"""

import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(r"g:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev Murillo\Quebra_de_sigilo [WarRoom]\LOGs_exec_27012026")
ANALISES_DIR = BASE_DIR / "Analises"
ANALISE_ORIGINAL = ANALISES_DIR / "Analise Original QS.xlsx"
ANALISE_POC = ANALISES_DIR / "Analise POC QS.xlsx"
OUTPUT_JSON = BASE_DIR / "Comparação" / "comparacao_analises.json"

def processar_analises():
    """Processa os arquivos Excel e gera comparação"""
    
    resultado = {
        'original': {},
        'poc': {},
        'comparacao': {}
    }
    
    try:
        # Ler Original
        print("Lendo Analise Original QS.xlsx...")
        original_data = pd.read_excel(ANALISE_ORIGINAL, sheet_name=None, engine='openpyxl')
        
        for sheet_name, df in original_data.items():
            # Converter para dict
            resultado['original'][sheet_name] = df.to_dict('records')
            print(f"  - {sheet_name}: {len(df)} linhas")
        
        # Ler POC
        print("\nLendo Analise POC QS.xlsx...")
        poc_data = pd.read_excel(ANALISE_POC, sheet_name=None, engine='openpyxl')
        
        for sheet_name, df in poc_data.items():
            # Converter para dict
            resultado['poc'][sheet_name] = df.to_dict('records')
            print(f"  - {sheet_name}: {len(df)} linhas")
        
        # Comparar abas comuns
        print("\nComparando abas...")
        common_sheets = set(original_data.keys()) & set(poc_data.keys())
        
        for sheet_name in common_sheets:
            df_orig = original_data[sheet_name]
            df_poc = poc_data[sheet_name]
            
            comparacao = {
                'aba': sheet_name,
                'linhas_original': len(df_orig),
                'linhas_poc': len(df_poc),
                'metricas': []
            }
            
            # Comparar colunas numéricas
            numeric_cols = set(df_orig.select_dtypes(include=['number']).columns) & \
                          set(df_poc.select_dtypes(include=['number']).columns)
            
            for col in sorted(numeric_cols):
                val_orig = df_orig[col].sum() if len(df_orig) > 0 else 0
                val_poc = df_poc[col].sum() if len(df_poc) > 0 else 0
                diff = val_poc - val_orig
                diff_pct = (diff / val_orig * 100) if val_orig != 0 else 0
                
                comparacao['metricas'].append({
                    'metrica': col,
                    'original': float(val_orig),
                    'poc': float(val_poc),
                    'diferenca': float(diff),
                    'diferenca_pct': float(diff_pct)
                })
            
            resultado['comparacao'][sheet_name] = comparacao
            print(f"  - {sheet_name}: {len(comparacao['metricas'])} métricas comparadas")
        
        # Salvar JSON
        OUTPUT_JSON.parent.mkdir(exist_ok=True)
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ Comparação salva em: {OUTPUT_JSON}")
        return resultado
        
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    processar_analises()
