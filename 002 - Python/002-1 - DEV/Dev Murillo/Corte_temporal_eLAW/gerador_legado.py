# ==============================================================================
# GERADOR DE LEGADO - Corte temporal eLAW
# Pega os últimos parquets gerados no processo (001 - Carga de bases em stage
# + conversão eLAW), antes de carregar no banco, e salva na pasta Legado.
# Gera arquivo de validação do legado com intervalos de datas e lista de colunas.
# ==============================================================================

import os
import shutil
import pandas as pd
from datetime import datetime
from dateutil import parser

# --- Caminhos ---
# Origem: pasta onde a conversão em massa eLAW grava os parquets (saída do processo)
PASTA_ORIGEM_PARQUETS = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW"
# Destino: pasta Legado do projeto Corte_temporal_eLAW
DIR_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_LEGADO = os.path.join(DIR_BASE, "Legado")
# Arquivo de validação na pasta do projeto (não dentro de Legado)
ARQUIVO_VALIDACAO = os.path.join(DIR_BASE, "validacao_legado.xlsx")


def _eh_data(val):
    """Tenta interpretar valor como data; retorna datetime ou None."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    if isinstance(val, datetime):
        return val
    if hasattr(val, "to_pydatetime"):
        return val.to_pydatetime()
    s = str(val).strip()
    if not s or s.lower() in ("nan", "nat", "--", "00/00/0000"):
        return None
    try:
        return parser.parse(s, dayfirst=True)
    except Exception:
        return None


def _detectar_colunas_data(df):
    """Retorna lista de nomes de colunas que parecem conter datas."""
    candidatas = []
    for col in df.columns:
        s = df[col].dropna()
        if s.empty:
            continue
        # Amostra para decidir
        sample = s.head(100)
        try:
            parsed = sample.apply(_eh_data)
            if parsed.notna().sum() >= max(1, len(sample) * 0.3):
                candidatas.append(col)
        except Exception:
            pass
    return candidatas


def _intervalo_datas_serie(serie):
    """Retorna (min, max) em formato string para uma coluna de datas."""
    vals = serie.apply(_eh_data)
    vals = vals.dropna()
    if vals.empty:
        return None, None
    dmin, dmax = vals.min(), vals.max()
    if hasattr(dmin, "strftime"):
        return dmin.strftime("%Y-%m-%d"), dmax.strftime("%Y-%m-%d")
    return str(dmin), str(dmax)


def copiar_parquets_para_legado():
    """
    Copia todos os .parquet da pasta de origem para a pasta Legado.
    Se a pasta de origem não existir, retorna lista dos parquets já presentes em Legado.
    """
    os.makedirs(PASTA_LEGADO, exist_ok=True)
    if not os.path.isdir(PASTA_ORIGEM_PARQUETS):
        print(f"  Aviso: Pasta de origem não encontrada: {PASTA_ORIGEM_PARQUETS}")
        print("  Usando parquets já existentes na pasta Legado para validação.")
        return [
            f for f in os.listdir(PASTA_LEGADO)
            if f.lower().endswith(".parquet") and os.path.isfile(os.path.join(PASTA_LEGADO, f))
        ]

    copiados = []
    for nome in os.listdir(PASTA_ORIGEM_PARQUETS):
        if not nome.lower().endswith(".parquet"):
            continue
        src = os.path.join(PASTA_ORIGEM_PARQUETS, nome)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(PASTA_LEGADO, nome)
        shutil.copy2(src, dst)
        copiados.append(nome)
    return copiados


def gerar_validacao_legado(arquivos_parquet):
    """
    Gera validacao_legado.xlsx com:
    - Aba 1: arquivos capturados e intervalo de datas de todos os campos de data.
    - Aba 2: lista de todas as colunas dos arquivos.
    """
    pasta = PASTA_LEGADO
    linhas_aba_arquivos = []
    linhas_aba_colunas = []

    for nome_arquivo in sorted(arquivos_parquet):
        path = os.path.join(pasta, nome_arquivo)
        if not os.path.isfile(path):
            continue
        try:
            df = pd.read_parquet(path)
        except Exception as e:
            linhas_aba_arquivos.append({
                "arquivo": nome_arquivo,
                "coluna_data": "(erro leitura)",
                "data_min": "",
                "data_max": str(e),
            })
            continue

        colunas_data = _detectar_colunas_data(df)
        if colunas_data:
            for col in colunas_data:
                dmin, dmax = _intervalo_datas_serie(df[col])
                linhas_aba_arquivos.append({
                    "arquivo": nome_arquivo,
                    "coluna_data": col,
                    "data_min": dmin or "",
                    "data_max": dmax or "",
                })
        else:
            linhas_aba_arquivos.append({
                "arquivo": nome_arquivo,
                "coluna_data": "(nenhuma coluna de data detectada)",
                "data_min": "",
                "data_max": "",
            })

        for col in df.columns:
            linhas_aba_colunas.append({
                "arquivo": nome_arquivo,
                "coluna": col,
            })

    df_arquivos = pd.DataFrame(linhas_aba_arquivos)
    df_colunas = pd.DataFrame(linhas_aba_colunas)

    with pd.ExcelWriter(ARQUIVO_VALIDACAO, engine="openpyxl") as writer:
        df_arquivos.to_excel(writer, sheet_name="Arquivos e intervalos de data", index=False)
        df_colunas.to_excel(writer, sheet_name="Colunas por arquivo", index=False)

    return ARQUIVO_VALIDACAO


def main():
    print("Gerador de legado - Corte temporal eLAW")
    print("=" * 50)
    print(f"Origem parquets: {PASTA_ORIGEM_PARQUETS}")
    print(f"Destino Legado:  {PASTA_LEGADO}")
    print()

    print("Copiando parquets para Legado...")
    copiados = copiar_parquets_para_legado()
    if not copiados:
        print("Nenhum arquivo .parquet na origem nem na pasta Legado. Nada a fazer.")
        return
    print(f"Arquivos considerados para validação: {len(copiados)}.")

    print("Gerando arquivo de validação...")
    path_validacao = gerar_validacao_legado(copiados)
    print(f"Validação salva: {path_validacao}")
    print("Concluído.")


if __name__ == "__main__":
    main()
