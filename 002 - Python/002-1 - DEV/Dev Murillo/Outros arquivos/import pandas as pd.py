# import os
# from pathlib import Path
# import pandas as pd

# # ============================================================
# # CONFIGURAÇÕES
# # ============================================================

# STAGE_DIR = Path(r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE")
# LEGADO_DIR = STAGE_DIR / "Legado_eLAW"
# ADHOC_DIR = STAGE_DIR / "ADHOC - Data de corte"
# MERGE_DIR = ADHOC_DIR / "Merge_Legado_pre2025"

# CUTOFF_DATE = pd.Timestamp("2025-01-01")
# VALID_EXTENSIONS = {".xlsx", ".xls"}


# # ============================================================
# # AUXILIARES
# # ============================================================

# def encontrar_linha_header(df_raw):
#     """Detecta a linha onde de fato começa o cabeçalho."""
#     for idx, row in df_raw.iterrows():
#         row_str = row.astype(str).str.lower()
#         if row.notna().sum() >= 3 and row_str.str.contains("data").any():
#             return idx
#     return 0


# def carregar_planilha(path: Path) -> pd.DataFrame:
#     df_raw = pd.read_excel(path, header=None)

#     header_idx = encontrar_linha_header(df_raw)
#     header_row = df_raw.iloc[header_idx]

#     df = df_raw.iloc[header_idx + 1:].copy()
#     df.columns = header_row

#     df = df.loc[:, ~df.columns.isna()]
#     df = df.dropna(how="all")
#     return df


# def encontrar_coluna_data(df, tipo):
#     """Seleciona automaticamente a coluna de data correta."""
#     cols = [c for c in df.columns if isinstance(c, str)]

#     if tipo == "incoming":
#         prioridades = ["data registrado"]
#         for col in cols:
#             if col.strip().lower() in prioridades:
#                 return col
#         for col in cols:
#             nome = col.lower()
#             if "data" in nome and "registr" in nome:
#                 return col

#     if tipo == "outgoing":
#         prioridades = [
#             "data de encerramento",
#             "data encerramento",
#             "encerramento",
#         ]
#         for col in cols:
#             if col.strip().lower() in prioridades:
#                 return col
#         for col in cols:
#             nome = col.lower()
#             if "data" in nome and "encer" in nome:
#                 return col

#     raise ValueError(f"Não achei coluna de data para {tipo}. Colunas: {cols}")


# def parsear_coluna_data(serie):
#     if pd.api.types.is_numeric_dtype(serie):
#         return pd.to_datetime(serie, origin="1899-12-30", unit="D", errors="coerce")
#     return pd.to_datetime(serie, dayfirst=True, errors="coerce")


# def salvar_planilha(df, path):
#     path.parent.mkdir(parents=True, exist_ok=True)
#     df.to_excel(path, index=False)


# # ============================================================
# # PROCESSO 1 — SPLIT (AGORA COM CHECAGEM)
# # ============================================================

# def split_arquivos_stage_por_data():

#     ADHOC_DIR.mkdir(parents=True, exist_ok=True)
#     pre2025_map = {}

#     for item in STAGE_DIR.iterdir():

#         if item.name.startswith("~$"):
#             continue

#         if item.is_dir():
#             if item.name.lower() in {LEGADO_DIR.name.lower(), ADHOC_DIR.name.lower()}:
#                 continue
#             continue

#         if item.suffix.lower() not in VALID_EXTENSIONS:
#             continue

#         nome_lower = item.name.lower()

#         if "incoming" in nome_lower:
#             tipo = "incoming"
#         elif "outgoing" in nome_lower:
#             tipo = "outgoing"
#         else:
#             continue

#         base = item.stem

#         pre_path = ADHOC_DIR / f"{base}_pre2025.xlsx"
#         post_path = ADHOC_DIR / f"{base}_from2025.xlsx"

#         # ⚡ CHECAGEM DE EXISTÊNCIA DO SPLIT
#         if pre_path.exists() and post_path.exists():
#             print(f"Split já existe, pulando: {item.name}")
#             pre2025_map[base] = pre_path
#             continue

#         print(f"Processando arquivo STAGE: {item.name}")

#         df = carregar_planilha(item)
#         col_data = encontrar_coluna_data(df, tipo)
#         df[col_data] = parsear_coluna_data(df[col_data])
#         df = df.dropna(subset=[col_data])

#         df_pre = df[df[col_data] < CUTOFF_DATE]
#         df_post = df[df[col_data] >= CUTOFF_DATE]

#         if not df_pre.empty:
#             salvar_planilha(df_pre, pre_path)
#             pre2025_map[base] = pre_path
#             print(f"  → Gerado pré-2025: {pre_path.name} ({len(df_pre)} linhas)")

#         if not df_post.empty:
#             salvar_planilha(df_post, post_path)
#             print(f"  → Gerado from-2025: {post_path.name} ({len(df_post)} linhas)")

#     return pre2025_map


# # ============================================================
# # PROCESSO 2 — MERGE (EMPILHAMENTO)
# # ============================================================

# def merge_legado_com_pre2025(pre2025_map):
#     MERGE_DIR.mkdir(parents=True, exist_ok=True)

#     for legacy_file in LEGADO_DIR.iterdir():

#         if legacy_file.name.startswith("~$"):
#             continue

#         if not legacy_file.is_file() or legacy_file.suffix.lower() not in VALID_EXTENSIONS:
#             continue

#         nome_lower = legacy_file.name.lower()
#         if "incoming" not in nome_lower and "outgoing" not in nome_lower:
#             continue

#         base = legacy_file.stem

#         pre_path = None
#         for k, v in pre2025_map.items():
#             if k == base or base.startswith(k) or k.startswith(base):
#                 pre_path = v
#                 break

#         if not pre_path or not pre_path.exists():
#             print(f"[MERGE] Sem pré-2025 para {legacy_file.name}")
#             continue

#         print(f"[MERGE] Empilhando {legacy_file.name} + {pre_path.name}")

#         df_leg = carregar_planilha(legacy_file)
#         df_pre = carregar_planilha(pre_path)

#         df_merged = pd.concat([df_leg, df_pre], ignore_index=True, sort=False).drop_duplicates()

#         out = MERGE_DIR / f"{base}_merged.xlsx"
#         salvar_planilha(df_merged, out)

#         print(f"  → Merge salvo: {out.name} ({len(df_merged)} linhas)")


# # ============================================================
# # EXECUÇÃO
# # ============================================================

# if __name__ == "__main__":
#     print("=== Etapa 1: Split por data (com checagem) ===")
#     pre2025_map = split_arquivos_stage_por_data()

#     print("\n=== Etapa 2: Merge Legado + Pré-2025 ===")
#     merge_legado_com_pre2025(pre2025_map)

#     print("\nProcesso concluído.")


import os
from pathlib import Path
import pandas as pd

# ============================================================
# CONFIGURAÇÕES
# ============================================================

STAGE_DIR = Path(r"G:\Drives compartilhados\Legales_Analytics\001 - Base\STAGE")
LEGADO_DIR = STAGE_DIR / "Legado_eLAW"
MERGE_DIR = STAGE_DIR / "ADHOC - Data de corte" / "Merge_Legado_pre2025"
FINAL_DIR = STAGE_DIR / "ADHOC - Data de corte" / "Final_Sem_Merged"
REPORT_PATH = STAGE_DIR / "ADHOC - Data de corte" / "Relatorio_Diferencas.xlsx"

VALID_EXTENSIONS = {".xlsx", ".xls"}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def carregar_planilha(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, dtype=str)
    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.isna()]
    return df


def salvar_planilha(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False)


# ============================================================
# ETAPA 1 — REMOVER DUPLICATAS E GERAR VERSÃO FINAL
# ============================================================

def remover_duplicatas_e_salvar():

    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    print("\n=== Removendo duplicatas dos arquivos merged ===\n")

    final_files = []  # manteremos lista para usar na etapa de comparação

    for file in MERGE_DIR.iterdir():

        if file.name.startswith("~$"):
            continue

        if not file.is_file() or file.suffix.lower() not in VALID_EXTENSIONS:
            continue

        if not file.name.lower().endswith("_merged.xlsx"):
            continue

        print(f"Processando (dedupe): {file.name}")

        df = carregar_planilha(file)
        before = len(df)
        df_clean = df.drop_duplicates()
        after = len(df_clean)

        print(f" → Linhas antes: {before}")
        print(f" → Linhas depois: {after}")
        print(f" → Removidas: {before - after}")

        new_name = file.name.replace("_merged", "")
        new_path = FINAL_DIR / new_name

        salvar_planilha(df_clean, new_path)
        final_files.append(new_path)

        print(f" → Salvo: {new_name}\n")

    return final_files


# ============================================================
# ETAPA 2 — COMPARAR FINAL VS LEGADO E GERAR ABA DE DIFERENÇAS
# ============================================================

def comparar_com_legado(arquivos_finais):

    print("\n=== Comparando arquivos finais com os arquivos do LEGAdo_eLAW ===\n")

    # Abrir writer de relatório consolidado
    with pd.ExcelWriter(REPORT_PATH, engine='openpyxl') as writer:

        for final_file in arquivos_finais:

            base_name = final_file.name  # sem _merged
            legacy_file = LEGADO_DIR / base_name

            print(f"Comparando: {base_name}")

            if not legacy_file.exists():
                print(f" ⚠️ Legado não encontrado: {legacy_file.name}, ignorando.\n")
                continue

            df_final = carregar_planilha(final_file)
            df_legacy = carregar_planilha(legacy_file)

            # Reset de index para permitir merge confiável
            df_final = df_final.fillna("")
            df_legacy = df_legacy.fillna("")

            # Diferenças = linhas que mudaram, foram adicionadas ou removidas
            concat = pd.concat([df_final.assign(origem="FINAL"),
                                df_legacy.assign(origem="LEGADO")],
                               ignore_index=True)

            duplicates_removed = concat.drop_duplicates(keep=False)

            print(f" → Diferenças encontradas: {len(duplicates_removed)}")

            # Nome da aba sem caracteres problemáticos
            sheet_name = base_name.replace(".xlsx", "")[:31]

            duplicates_removed.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f" → Aba criada: {sheet_name}\n")

    print(f"\n=== Relatório consolidado salvo em ===\n{REPORT_PATH}\n")


# ============================================================
# EXECUÇÃO COMPLETA DO PIPELINE
# ============================================================

if __name__ == "__main__":

    # ETAPA 1: limpar duplicatas
    arquivos_finais = remover_duplicatas_e_salvar()

    # ETAPA 2: comparar final vs legado e gerar relatório em abas
    comparar_com_legado(arquivos_finais)

    print("\nProcesso concluído com sucesso!\n")

