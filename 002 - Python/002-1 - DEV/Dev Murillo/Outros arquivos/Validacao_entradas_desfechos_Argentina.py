# ================================================
# Validação: quantidade de processo_id distintos por mês - Argentina (parquets)
# Período: 01/2024 a 12/2025 (2024 inteiro para bater com relatório)
# Agrupado por empresa tratada (derivada de empresa_responsavel)
# ================================================

import os
import pandas as pd
from datetime import datetime

# --- Configuração ---
PASTA_ELAW = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW"
PAIS_FILTRO = "Argentina"
MES_INICIO = (2024, 1)   # 2024 inteiro
MES_FIM = (2025, 12)     # 12/2025

# Parquets de contencioso hispanos (fontes para Argentina)
PREFIXO_HISPANOS = "Database_eLAW_Contencioso_Hispanos_"
COL_PAIS = "pais"
COL_PROCESSO_ID = "processo_id"
COL_DATA = "data_registrado"
COL_EMPRESA = "empresa_responsavel"  # coluna usada para derivar "empresa tratada"


def normalizar_empresa_tratada(serie):
    """Agrupa empresa_responsavel em Mercado Libre, Mercado Pago ou Outros."""
    def _tratar(val):
        if pd.isna(val) or str(val).strip() == "":
            return "Não informado"
        s = str(val).strip().upper()
        if "MERCADO LIBRE" in s or "MELILOG" in s or "EBAZAR" in s or "FIRST LABEL" in s:
            return "Mercado Libre"
        if "MERCADO PAGO" in s or "MERCADO PAGO" in s:
            return "Mercado Pago"
        return "Outros"
    return serie.apply(_tratar)


def parse_data_registrado(serie):
    """Converte coluna data_registrado (dd/mm/yyyy) para datetime."""
    return pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")


def main():
    print("=" * 70)
    print("VALIDAÇÃO ENTRADAS E DESFECHOS - ARGENTINA (parquets)")
    print("=" * 70)
    print(f"Pasta: {PASTA_ELAW}")
    print(f"País: {PAIS_FILTRO} | Período: {MES_INICIO[0]}-{MES_INICIO[1]:02d} a {MES_FIM[0]}-{MES_FIM[1]:02d}")
    print("=" * 70)

    if not os.path.isdir(PASTA_ELAW):
        print(f"Erro: Pasta não encontrada: {PASTA_ELAW}")
        return

    # Listar parquets Hispanos
    arquivos = [
        f for f in os.listdir(PASTA_ELAW)
        if f.endswith(".parquet") and PREFIXO_HISPANOS in f
    ]
    if not arquivos:
        print(f"Nenhum parquet '{PREFIXO_HISPANOS}*' encontrado em {PASTA_ELAW}")
        return

    dfs = []
    for nome in sorted(arquivos):
        path = os.path.join(PASTA_ELAW, nome)
        try:
            df = pd.read_parquet(path, engine="pyarrow")
            if COL_PAIS not in df.columns or COL_PROCESSO_ID not in df.columns or COL_DATA not in df.columns:
                print(f"  Aviso: {nome} sem colunas esperadas (pais, processo_id, data_registrado). Pulando.")
                continue
            if COL_EMPRESA not in df.columns:
                df[COL_EMPRESA] = ""
            df["_fonte"] = nome
            dfs.append(df)
        except Exception as e:
            print(f"  Erro ao ler {nome}: {e}")

    if not dfs:
        print("Nenhum parquet válido carregado.")
        return

    base = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal de linhas (todos os países) nos parquets Hispanos: {len(base):,}")

    # Filtro Argentina
    base = base[base[COL_PAIS].astype(str).str.strip().str.lower() == PAIS_FILTRO.lower()]
    print(f"Linhas após filtro país = '{PAIS_FILTRO}': {len(base):,}")

    # Empresa tratada (derivada de empresa_responsavel)
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
        print(f"Nenhum registro no período {MES_INICIO[0]}-{MES_INICIO[1]:02d} a {MES_FIM[0]}-{MES_FIM[1]:02d}.")
        return

    # processo_id numérico
    processo_id_str = base[COL_PROCESSO_ID].astype(str).str.strip()
    base["_pid"] = pd.to_numeric(processo_id_str, errors="coerce")
    base = base.dropna(subset=["_pid"])
    base["_pid"] = base["_pid"].astype("Int64")

    # Agrupar por mês E por empresa tratada: quantidade de processo_id distintos
    contagem = (
        base.groupby(["_ano_mes", "empresa_tratada"], as_index=False)["_pid"]
        .nunique()
        .rename(columns={"_ano_mes": "ano_mes", "_pid": "processo_id_distintos"})
    )
    contagem["ano_mes"] = contagem["ano_mes"].astype(str)

    print("\n--- processo_id distintos por mês e por empresa tratada (Argentina) ---\n")
    print(contagem.to_string(index=False))

    # Tabela dinâmica (mês x empresa tratada) para comparar com o gráfico
    pivot = contagem.pivot(index="ano_mes", columns="empresa_tratada", values="processo_id_distintos").fillna(0).astype(int)
    # Ordenar colunas: Mercado Libre, Mercado Pago, Outros, Não informado
    ordem_col = [c for c in ["Mercado Libre", "Mercado Pago", "Outros", "Não informado"] if c in pivot.columns]
    ordem_col += [c for c in pivot.columns if c not in ordem_col]
    pivot = pivot.reindex(columns=ordem_col)
    print("\n--- Tabela dinâmica (mês x empresa tratada) — para comparar com o gráfico ---\n")
    print(pivot.to_string())
    print("\n" + "=" * 70)
    print("(Valores = processo_id distintos naquele mês para aquela empresa; mesmo processo em 2 meses conta 2x)")
    print("=" * 70)


if __name__ == "__main__":
    main()
