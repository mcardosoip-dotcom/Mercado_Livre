# ================================================
# EMBARGOS BRASIL - Versão Python
# Equivalente ao StepXX- SQL - Embargos Brasil.sql
# Em vez de consultar as tabelas STG no BigQuery, lê os parquets
# que alimentam essas tabelas (pasta 001-01 - eLAW).
#
# Parquets (fonte):
#   - Database_eLAW_Contencioso_Brasil_Incoming.parquet  -> STATUS = "Ativo"
#   - Database_eLAW_Contencioso_Brasil_Ongoing.parquet   -> STATUS = "Reativado"
#   - Database_eLAW_Contencioso_Brasil_Outgoing.parquet   -> STATUS = "Encerrado"
#
# Uso:
#   python embargos_brasil_parquets.py
#   Ou definir PASTA_ELAW no ambiente para outro caminho.
# ================================================

import os
from datetime import datetime

import pandas as pd

PASTA_ELAW = os.environ.get(
    "PASTA_ELAW",
    r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW",
)

ARQUIVOS = [
    ("Database_eLAW_Contencioso_Brasil_Incoming.parquet", "Ativo", "N"),
    ("Database_eLAW_Contencioso_Brasil_Ongoing.parquet", "Reativado", None),  # None = calculado
    ("Database_eLAW_Contencioso_Brasil_Outgoing.parquet", "Encerrado", "N"),
]

DATA_MINIMA = datetime(2023, 1, 1).date()


def parse_date_br(s: str):
    """Converte string dd/mm/yyyy em date. Retorna None se inválido."""
    if pd.isna(s) or s is None or str(s).strip() == "":
        return None
    s = str(s).strip()
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None


def carregar_parquet(caminho: str) -> pd.DataFrame | None:
    if not os.path.isfile(caminho):
        return None
    try:
        return pd.read_parquet(caminho)
    except Exception as e:
        print(f"[ERRO] Ao ler {caminho}: {e}")
        return None


def _col(df: pd.DataFrame, *nomes: str):
    """Retorna a série da primeira coluna que existir (case-insensitive)."""
    cols = {c.lower(): c for c in df.columns}
    for n in nomes:
        k = n.lower()
        if k in cols:
            return df[cols[k]]
    return None


def legales_reiteratorio_ongoing(row: pd.Series) -> str:
    """CASE WHEN Pais = "Brasil" AND STATUS = "Reativado" THEN 'S' ELSE 'N' END"""
    p = (row.get("Pais") or "").strip()
    s = (row.get("STATUS") or "").strip()
    return "S" if p == "Brasil" and s == "Reativado" else "N"


def tipo_resposta(row: pd.Series) -> str | None:
    """CASE WHEN PROCESSO_APRESENTADA_RESPOSTA_NEGATIVA = "Sim" THEN "Sem informação" WHEN = "Não" THEN "Com informação" ELSE NULL"""
    v = (row.get("PROCESSO_APRESENTADA_RESPOSTA_NEGATIVA") or "").strip()
    if v == "Sim":
        return "Sem informação"
    if v == "Não":
        return "Com informação"
    return None


def build_union_elaw() -> pd.DataFrame:
    """Monta o union das 3 bases (equivalente ao subselect do SQL)."""
    partes = []

    for nome_arquivo, status_filtro, legales_fixo in ARQUIVOS:
        caminho = os.path.join(PASTA_ELAW, nome_arquivo)
        df = carregar_parquet(caminho)
        if df is None:
            print(f"[SKIP] Arquivo não encontrado ou erro: {nome_arquivo}")
            continue

        # Filtro de STATUS
        status_serie = _col(df, "STATUS", "status")
        if status_serie is None:
            print(f"[SKIP] Coluna STATUS não encontrada em {nome_arquivo}")
            continue
        df = df[status_serie.astype(str).str.strip() == status_filtro].copy()

        if legales_fixo is not None:
            df["LEGALES_REITERATORIO"] = legales_fixo
        else:
            df["LEGALES_REITERATORIO"] = df.apply(legales_reiteratorio_ongoing, axis=1)

        partes.append(df)

    if not partes:
        return pd.DataFrame()

    union = pd.concat(partes, ignore_index=True)
    # UNION DISTINCT
    union = union.drop_duplicates()
    return union


def elaw_oficios(a: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica as mesmas transformações e filtros do CTE elaw_oficios do StepXX.
    Sem os JOINs comentados (DIM_10 e MaxConfirmacaoPorProcesso).
    """
    # Filtro: Requerimentos + Ofícios + data registrado > 2023-01-01
    area = _col(a, "AREA_DO_DIREITO", "area_do_direito")
    subarea = _col(a, "SUB_AREA_DO_DIREITO", "sub_area_do_direito")
    if area is None or subarea is None:
        return pd.DataFrame()
    a = a[(area.astype(str).str.strip() == "Requerimentos") & (subarea.astype(str).str.strip() == "Ofícios")].copy()

    # Data registrado > 2023-01-01
    data_reg = _col(a, "DATA_REGISTRADO", "data_registrado")
    if data_reg is None:
        return pd.DataFrame()
    datas_parseadas = data_reg.map(parse_date_br)
    a = a[datas_parseadas.notna() & (datas_parseadas >= DATA_MINIMA)].copy()

    if a.empty:
        return pd.DataFrame()

    # Reaplicar para as linhas que sobraram
    data_reg = _col(a, "DATA_REGISTRADO", "data_registrado")
    data_enc = _col(a, "DATA_DE_ENCERRAMENTO", "data_de_encerramento")

    def _s( nome, *aliases ):
        s = _col(a, nome, *aliases)
        return s if s is not None else pd.Series([None] * len(a))

    out = pd.DataFrame()
    out["processo_id"] = _s("PROCESSO_ID", "processo_id")
    out["STATUS"] = _s("STATUS", "status")
    out["AREA_DO_DIREITO"] = _s("AREA_DO_DIREITO", "area_do_direito")
    out["SUB_AREA_DO_DIREITO"] = _s("SUB_AREA_DO_DIREITO", "sub_area_do_direito")
    out["PAGE_REPORT_ESCRITORIORESPONSAVEL"] = _s("PAGE_REPORT_ESCRITORIORESPONSAVEL", "page_report_escritorioresponsavel")
    out["PROCESSO_ESTADO"] = _s("PROCESSO_ESTADO", "processo_estado")
    out["OBJETO"] = _s("OBJETO", "objeto")
    out["DATA_DE_CITACAO"] = _s("DATA_DE_CITACAO", "data_de_citacao").astype(str)
    out["DATA_REGISTRADO"] = _s("DATA_REGISTRADO", "data_registrado").astype(str)
    out["DATA_DE_ENCERRAMENTO"] = _s("DATA_DE_ENCERRAMENTO", "data_de_encerramento").astype(str)
    out["VALOR_DO_RISCO"] = _s("VALOR_DO_RISCO", "valor_do_risco")
    out["USUARIO"] = _s("USUARIO", "usuario")
    out["PROCESSO_MATERIA"] = _s("PROCESSO_MATERIA", "processo_materia")
    out["ESCRITORIO_EXTERNO"] = _s("ESCRITORIO_EXTERNO", "escritorio_externo")
    out["PROCESSO_PRAZO"] = _s("PROCESSO_PRAZO", "processo_prazo")
    out["PROVEDOR"] = "Finch"
    out["Pais"] = "Brasil"
    out["Tipo_Resposta"] = a.apply(tipo_resposta, axis=1)
    leg = _col(a, "LEGALES_REITERATORIO")
    out["LEGALES_REITERATORIO"] = (leg if leg is not None else pd.Series(["N"] * len(a))).astype(str)
    out["DATA_DE_REGISTRADO_TRATADA"] = data_reg.map(parse_date_br)
    out["DATA_DE_ENCERRAMENTO_TRATADA"] = data_enc.map(parse_date_br) if data_enc is not None else pd.Series([pd.NaT] * len(a))
    # Sem JOIN com DIM nem MaxConfirmacao (comentados no StepXX)
    out["DATA_DE_CONFIRMACAO_MAX_TAREFA"] = pd.NaT
    out["DATA_DE_REGISTRADO_MAX_TAREFA"] = pd.NaT

    return out.drop_duplicates()


def main():
    print("=" * 70)
    print("Embargos Brasil - Leitura a partir dos parquets eLAW")
    print("=" * 70)
    print(f"Pasta parquets: {PASTA_ELAW}\n")

    a = build_union_elaw()
    if a.empty:
        print("Nenhum dado carregado. Verifique os parquets em PASTA_ELAW.")
        return

    print(f"Union (Incoming+Ongoing+Outgoing) após filtros de STATUS: {len(a)} linhas.")

    result = elaw_oficios(a)
    print(f"Após filtro Requerimentos + Ofícios + DATA_REGISTRADO > 2023-01-01: {len(result)} linhas.\n")

    # Count distinct processo_id por ano-mês (DATA_DE_REGISTRADO_TRATADA)
    if not result.empty and "DATA_DE_REGISTRADO_TRATADA" in result.columns:
        df = result.dropna(subset=["DATA_DE_REGISTRADO_TRATADA", "processo_id"])
        df = df.copy()
        df["ano_mes"] = pd.to_datetime(df["DATA_DE_REGISTRADO_TRATADA"]).dt.to_period("M").astype(str)
        counts = df.groupby("ano_mes", sort=True)["processo_id"].nunique()
        print("Count distinct processo_id por ano-mês (DATA_DE_REGISTRADO_TRATADA):")
        print("-" * 40)
        for ano_mes, n in counts.items():
            print(f"  {ano_mes}: {n}")
        print(f"  TOTAL (distinct processo_id): {result['processo_id'].nunique()}\n")

    # Saída: DataFrame em memória; opcionalmente salvar parquet
    out_parquet = os.environ.get("OUT_EMBARGOS_BRASIL_PARQUET")
    if out_parquet:
        result.to_parquet(out_parquet, index=False)
        print(f"Resultado salvo em: {out_parquet}")
    else:
        print("Primeiras linhas do resultado (defina OUT_EMBARGOS_BRASIL_PARQUET para salvar parquet):")
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        print(result.head(10))

    print("\n" + "=" * 70)
    print("Fim.")
    print("=" * 70)


if __name__ == "__main__":
    main()
