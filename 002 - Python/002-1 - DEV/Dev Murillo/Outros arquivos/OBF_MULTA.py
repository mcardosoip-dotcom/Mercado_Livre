import pandas as pd
import re
from pathlib import Path

parquet_path = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW\Database_eLAW_Obrigacoes_de_Fazer.parquet"
col_json_like = "descricao_evento_concluido"  # já confirmado

# 1) Ler parquet
df = pd.read_parquet(parquet_path, engine="pyarrow")

print("\n>>> Colunas do parquet:")
for c in df.columns:
    print("-", c)

if col_json_like not in df.columns:
    raise RuntimeError(f"Coluna '{col_json_like}' não existe no arquivo.")

# 2) Função robusta para parsear "chave: valor;" (sem depender de JSON válido)
# - Aceita quebras de linha, espaços extras, aspas, ; duplicados
# - Divide por ';' e depois separa a primeira ocorrência de ':' em cada trecho
def parse_kv_semiestruturado(raw):
    if pd.isna(raw):
        return None
    s = str(raw)

    # normalizações leves
    s = s.replace("\r", " ").replace("\n", " ")
    # remove chaves/colchetes soltos no começo/fim, caso venham embrulhados
    s = s.strip().strip("{}[]()")
    # colapsa múltiplos ; em um só
    s = re.sub(r";{2,}", ";", s)

    # separa por ';'
    partes = [p.strip() for p in s.split(";") if p.strip()]
    d = {}
    for p in partes:
        if ":" not in p:
            # alguns trechos podem não ter ':', ignoramos
            continue
        k, v = p.split(":", 1)  # só a primeira ocorrência de ':'
        k = k.strip().strip('"').strip("'")
        v = v.strip().strip('"').strip("'")
        if not k:
            continue
        # evita duplicar chaves vazias; se repetir chave, mantém a primeira não-vazia
        if k not in d or not d[k]:
            d[k] = v
    return d if d else None

# 3) Aplicar parsing
parsed = df[col_json_like].apply(parse_kv_semiestruturado)
valid = parsed.dropna()
if valid.empty:
    raise RuntimeError(f"Nenhuma linha de '{col_json_like}' apresentou pares 'chave: valor;'. Verifique o conteúdo.")

# 4) Normalizar em colunas
json_df = pd.json_normalize(valid)
json_df.index = valid.index  # realinha pelos índices originais

# prefixo para evitar colisões com colunas existentes
prefixo = f"{col_json_like}."
json_df = json_df.add_prefix(prefixo)

# 5) Juntar ao dataframe original
df_expandido = df.join(json_df)

# 6) Listar as novas colunas criadas
novas_colunas = [c for c in df_expandido.columns if c.startswith(prefixo)]
print(f"\n>>> {len(novas_colunas)} novas colunas criadas a partir de '{col_json_like}':")
for c in novas_colunas[:50]:
    print("-", c)
if len(novas_colunas) > 50:
    print("... (+ mais colunas)")

# # 7) Salvar resultado
# saida_parquet = Path(parquet_path).with_suffix(".expandido.parquet")
# df_expandido.to_parquet(saida_parquet, engine="pyarrow", index=False)
# print(f"\n>>> Arquivo expandido salvo em: {saida_parquet}")

# # (Opcional) salvar só as colunas novas para inspecionar rapidamente em CSV:
# # df_expandido[novas_colunas].to_csv(Path(parquet_path).with_suffix(".json_cols.csv"), index=False, encoding="utf-8-sig")
