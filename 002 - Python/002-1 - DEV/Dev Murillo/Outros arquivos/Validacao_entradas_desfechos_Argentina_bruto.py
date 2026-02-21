# ================================================
# Validação: mesma análise do script de parquet, usando dado BRUTO (Excel em STAGE)
# Fonte: Excel definidos em Mapeamento_de_fontes.xlsx (Contencioso_Hispanos)
# Período: 01/2024 a 12/2025 | Agrupado por empresa tratada
# ================================================

import os
import re
import unicodedata
import pandas as pd
from datetime import datetime

# --- Configuração ---
CAMINHO_MAPEAMENTO = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\MAIN\CARGA DE TABELAS\eLAW\Mapeamento_de_fontes.xlsx"
PAIS_FILTRO = "Argentina"
MES_INICIO = (2024, 1)
MES_FIM = (2025, 12)
SKIPROWS = 5  # mesmo que o ETL que gera o parquet

# Nomes normalizados que precisamos (como no parquet)
COL_PAIS = "pais"
COL_PROCESSO_ID = "processo_id"
COL_DATA = "data_registrado"
COL_EMPRESA = "empresa_responsavel"
PREFIXO_HISPANOS = "Contencioso_Hispanos"


def normalizar_nome_coluna(texto):
    """Igual ao ETL: remove acentos, não-alfanum -> _, lower, strip _."""
    if not isinstance(texto, str):
        texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"\W+", "_", texto)
    return texto.strip("_").lower()


def achar_coluna(df, nome_normalizado):
    """Retorna o nome da primeira coluna cujo nome normalizado é o desejado."""
    for c in df.columns:
        if normalizar_nome_coluna(c) == nome_normalizado:
            return c
    return None


def normalizar_empresa_tratada(serie):
    """Agrupa empresa_responsavel em Mercado Libre, Mercado Pago ou Outros."""
    def _tratar(val):
        if pd.isna(val) or str(val).strip() == "":
            return "Não informado"
        s = str(val).strip().upper()
        if "MERCADO LIBRE" in s or "MELILOG" in s or "EBAZAR" in s or "FIRST LABEL" in s:
            return "Mercado Libre"
        if "MERCADO PAGO" in s:
            return "Mercado Pago"
        return "Outros"
    return serie.apply(_tratar)


def parse_data_registrado(serie):
    """Converte data para datetime (Excel pode vir como datetime ou string)."""
    return pd.to_datetime(serie, dayfirst=True, errors="coerce")


def main():
    print("=" * 70)
    print("VALIDAÇÃO ENTRADAS E DESFECHOS - ARGENTINA (DADO BRUTO - Excel STAGE)")
    print("=" * 70)

    if not os.path.isfile(CAMINHO_MAPEAMENTO):
        print(f"Erro: Mapeamento não encontrado: {CAMINHO_MAPEAMENTO}")
        return

    # Carregar mapeamento e filtrar apenas Contencioso Hispanos
    df_map = pd.read_excel(CAMINHO_MAPEAMENTO, sheet_name="Mapeamento", dtype=str)
    df_map.columns = [c.strip() for c in df_map.columns]
    for col in ["Endereco", "Arquivo", "Aba", "Arquivo final"]:
        if col not in df_map.columns:
            print(f"Erro: Coluna '{col}' não encontrada no mapeamento.")
            return
    df_map = df_map[df_map["Arquivo final"].str.contains(PREFIXO_HISPANOS, na=False)]
    if df_map.empty:
        print(f"Nenhuma linha no mapeamento com '{PREFIXO_HISPANOS}'.")
        return

    print(f"Período: {MES_INICIO[0]}-{MES_INICIO[1]:02d} a {MES_FIM[0]}-{MES_FIM[1]:02d} | País: {PAIS_FILTRO}")
    print("=" * 70)

    dfs = []
    for _, row in df_map.iterrows():
        endereco = (row["Endereco"] or "").strip()
        arquivo = (row["Arquivo"] or "").strip()
        aba = (row["Aba"] or "").strip()
        arquivo_final = (row["Arquivo final"] or "").strip()
        path = os.path.join(endereco, arquivo + ".xlsx")
        if not os.path.isfile(path):
            print(f"  Aviso: Arquivo não encontrado: {path}")
            continue
        try:
            # Tentar pela aba pelo nome; se falhar, usar primeira aba
            try:
                df = pd.read_excel(path, sheet_name=aba, skiprows=SKIPROWS)
            except Exception:
                df = pd.read_excel(path, sheet_name=0, skiprows=SKIPROWS)
            # Mapear colunas do Excel (nomes brutos) para os nomes que usamos
            col_pais = achar_coluna(df, COL_PAIS)
            col_pid = achar_coluna(df, COL_PROCESSO_ID)
            col_data = achar_coluna(df, COL_DATA)
            col_empresa = achar_coluna(df, COL_EMPRESA)
            if not col_pais or not col_pid or not col_data:
                print(f"  Aviso: {arquivo_final} sem colunas esperadas (pais, processo_id, data_registrado). Pulando.")
                continue
            df = df.rename(columns={
                col_pais: COL_PAIS,
                col_pid: COL_PROCESSO_ID,
                col_data: COL_DATA,
            })
            if col_empresa:
                df = df.rename(columns={col_empresa: COL_EMPRESA})
            else:
                df[COL_EMPRESA] = ""
            df["_fonte"] = arquivo_final
            dfs.append(df)
            print(f"  OK: {arquivo_final} ({len(df):,} linhas)")
        except Exception as e:
            print(f"  Erro ao ler {path}: {e}")

    if not dfs:
        print("Nenhum Excel válido carregado.")
        return

    base = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal de linhas (todos os países) nos Excel Hispanos: {len(base):,}")

    # Filtro Argentina
    base = base[base[COL_PAIS].astype(str).str.strip().str.lower() == PAIS_FILTRO.lower()]
    print(f"Linhas após filtro país = '{PAIS_FILTRO}': {len(base):,}")

    # Empresa tratada
    base["empresa_tratada"] = normalizar_empresa_tratada(base[COL_EMPRESA])
    print(f"Empresas tratadas encontradas: {base['empresa_tratada'].value_counts().to_dict()}")

    # Data
    base["_dt"] = parse_data_registrado(base[COL_DATA])
    base = base.dropna(subset=["_dt"])
    base["_ano_mes"] = base["_dt"].dt.to_period("M")

    # Período
    inicio = datetime(MES_INICIO[0], MES_INICIO[1], 1)
    fim = datetime(MES_FIM[0], MES_FIM[1], 1)
    base = base[(base["_dt"] >= inicio) & (base["_dt"] <= fim)]

    if base.empty:
        print(f"Nenhum registro no período.")
        return

    # processo_id numérico
    processo_id_str = base[COL_PROCESSO_ID].astype(str).str.strip()
    base["_pid"] = pd.to_numeric(processo_id_str, errors="coerce")
    base = base.dropna(subset=["_pid"])
    base["_pid"] = base["_pid"].astype("Int64")

    # Agrupar por mês e empresa tratada
    contagem = (
        base.groupby(["_ano_mes", "empresa_tratada"], as_index=False)["_pid"]
        .nunique()
        .rename(columns={"_ano_mes": "ano_mes", "_pid": "processo_id_distintos"})
    )
    contagem["ano_mes"] = contagem["ano_mes"].astype(str)

    print("\n--- processo_id distintos por mês e por empresa tratada (Argentina - BRUTO) ---\n")
    print(contagem.to_string(index=False))

    pivot = contagem.pivot(index="ano_mes", columns="empresa_tratada", values="processo_id_distintos").fillna(0).astype(int)
    ordem_col = [c for c in ["Mercado Libre", "Mercado Pago", "Outros", "Não informado"] if c in pivot.columns]
    ordem_col += [c for c in pivot.columns if c not in ordem_col]
    pivot = pivot.reindex(columns=ordem_col)
    print("\n--- Tabela dinâmica (mês x empresa tratada) — BRUTO ---\n")
    print(pivot.to_string())
    print("\n" + "=" * 70)
    print("(Valores = processo_id distintos naquele mês; mesmo processo em 2 meses conta 2x)")
    print("=" * 70)


if __name__ == "__main__":
    main()
