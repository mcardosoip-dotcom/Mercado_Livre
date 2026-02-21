# ==============================================================================
# PROCESSO DE CORTE TEMPORAL eLAW
# Objetivo: Unificar bases "Legado" e "Nova" aplicando regra de corte por data.
# Saída: Arquivos consolidados no diretório "Combinado".
# ==============================================================================

import os
import pandas as pd
from datetime import datetime

# --- Parâmetros de Configuração ---


# Estrutura de Diretórios (relativos ao script).
PASTA_LEGADO = "Legado"
PASTA_NOVA = "Nova"
PASTA_COMBINADO = "Combinado"


# Configuração de rastreabilidade (flag para identificar origem do registro).
ADICIONAR_COLUNA_ORIGEM = False
NOME_COLUNA_ORIGEM = "versao_fonte"


# Definição das datas de corte (thresholds).
# Lógica: Registros <= Data (mantém Legado) | Registros > Data (mantém Nova).
DATAS_CORTE = {
    "padrao": datetime(2026, 1, 1),      
    "2025": datetime(2025, 1, 1), 
    # "outra": datetime(2025, 1, 1),
}


# Chave de corte padrão para arquivos não listados explicitamente nos grupos.
DATA_CORTE_PADRAO = "padrao"
# Coluna de data para fallback (arquivos presentes nos diretórios mas sem grupo definido).
COLUNA_DATA_PADRAO = "data_registrado"


# Definição dos grupos de processamento (referencial: parquets_elaw_nomes_temporario.csv).
# Estrutura: Coluna alvo para filtro, chave da data de corte e lista de arquivos.
GRUPOS = [
    {
        "coluna_data": "data_da_tarefa",
        "data_corte": "padrao",
        "arquivos": [
            "Database_eLAW_Acompanhamento_de_tarefas_CORP_CX.parquet",
            "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP.parquet",
            "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP_CX.parquet",
            "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR.parquet",
            "Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS.parquet",
        ],
    },
    {
        "coluna_data": "data_registrado",
        "data_corte": "padrao",
        "arquivos": [
            "Database_eLAW_Amelia.parquet",
            "Database_eLAW_Contencioso_Brasil_Incoming.parquet",
            "Database_eLAW_Contencioso_Hispanos_Incoming.parquet",
            "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados.parquet",
            "Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes.parquet",
        ],
    },
    {
        "coluna_data": "data_de_encerramento",
        "data_corte": "padrao",
        "arquivos": [
            "Database_eLAW_Contencioso_Brasil_Outgoing.parquet",
            "Database_eLAW_Contencioso_Hispanos_Outgoing.parquet",
        ],
    },
    {
        "coluna_data": "data",
        "data_corte": "padrao",
        "arquivos": [
            "Database_eLAW_Extracao_multas.parquet",
            "Database_eLAW_Tarefas_Agendadas_Aguardando_Informações.parquet",
        ],
    },
]



def _dir_base():
    """Retorna o diretório raiz absoluto onde o script está localizado."""
    return os.path.dirname(os.path.abspath(__file__))


def _listar_arquivos_legado_e_nova(base_dir):
    """
    Identifica a interseção de arquivos presentes simultaneamente nas pastas Legado e Nova.
    Retorna lista ordenada.
    """
    dir_legado = os.path.join(base_dir, PASTA_LEGADO)
    dir_nova = os.path.join(base_dir, PASTA_NOVA)
    if not os.path.isdir(dir_legado) or not os.path.isdir(dir_nova):
        return []
    legado = set(f for f in os.listdir(dir_legado) if os.path.isfile(os.path.join(dir_legado, f)))
    nova = set(f for f in os.listdir(dir_nova) if os.path.isfile(os.path.join(dir_nova, f)))
    return sorted(legado & nova)


def _arquivos_em_grupos():
    """Retorna conjunto único de arquivos já mapeados na variável GRUPOS."""
    return {nome for grupo in GRUPOS for nome in grupo.get("arquivos", [])}


def _data_corte_do_grupo(grupo):
    """Obtém o objeto datetime configurado para o grupo; aplica fallback se necessário."""
    chave = grupo.get("data_corte", DATA_CORTE_PADRAO)
    if chave not in DATAS_CORTE:
        raise ValueError(f"Chave '{chave}' não definida em DATAS_CORTE. Disponíveis: {list(DATAS_CORTE)}")
    return DATAS_CORTE[chave]


def _parse_data(serie, coluna):
    """Converte série para datetime. Suporta formatos DD/MM/AAAA e ISO."""
    s = pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")
    if s.isna().all():
        s = pd.to_datetime(serie, errors="coerce")
    return s


def _ler_arquivo(path):
    """IO de leitura: Suporta Parquet (pyarrow) e CSV/TXT (utf-8)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        return pd.read_parquet(path, engine="pyarrow")
    if ext in (".csv", ".txt"):
        return pd.read_csv(path, sep=";", encoding="utf-8", on_bad_lines="skip", low_memory=False)
    raise ValueError(f"Formato não suportado: {ext}")


def _salvar_arquivo(df, path):
    """IO de escrita: Mantém extensão original (Parquet ou CSV)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        df.to_parquet(path, index=False, engine="pyarrow")
    elif ext in (".csv", ".txt"):
        df.to_csv(path, index=False, sep=";", encoding="utf-8-sig")
    else:
        df.to_parquet(path.replace(ext, ".parquet"), index=False, engine="pyarrow")


def processar_arquivo(nome_arquivo, base_dir, data_corte, coluna_data, adicionar_origem, nome_col_origem):
    """
    Executa o pipeline de fusão para um arquivo específico:
    1. Carregamento; 2. Validação; 3. Normalização; 4. Filtro Temporal; 5. Exportação.
    Retorna: (bool sucesso, str mensagem).
    """
    path_legado = os.path.join(base_dir, PASTA_LEGADO, nome_arquivo)
    path_nova = os.path.join(base_dir, PASTA_NOVA, nome_arquivo)
    path_combinado = os.path.join(base_dir, PASTA_COMBINADO, nome_arquivo)

    if not os.path.isfile(path_legado):
        return False, f"Arquivo ausente em Legado: {path_legado}"
    if not os.path.isfile(path_nova):
        return False, f"Arquivo ausente em Nova: {path_nova}"

    try:
        df_legado = _ler_arquivo(path_legado)
        df_nova = _ler_arquivo(path_nova)
    except Exception as e:
        return False, f"Erro de I/O na leitura: {e}"

    if coluna_data not in df_legado.columns:
        return False, f"Coluna '{coluna_data}' inexistente no Legado."
    if coluna_data not in df_nova.columns:
        return False, f"Coluna '{coluna_data}' inexistente na Nova."

    # Normalização de datas (sem alterar conjunto de colunas)
    df_legado = df_legado.copy()
    df_nova = df_nova.copy()
    df_legado["_dt_corte"] = _parse_data(df_legado[coluna_data], coluna_data)
    df_nova["_dt_corte"] = _parse_data(df_nova[coluna_data], coluna_data)

    # Aplicação do filtro temporal
    legado_filtrado = df_legado[df_legado["_dt_corte"] <= data_corte].copy()
    nova_filtrada = df_nova[df_nova["_dt_corte"] > data_corte].copy()
    legado_filtrado.drop(columns=["_dt_corte"], inplace=True)
    nova_filtrada.drop(columns=["_dt_corte"], inplace=True)

    # Alinhar Legado ao esquema da Nova: mesma ordem de colunas e mesmas colunas;
    # colunas que existem só na Nova ficam vazias (NaN) no Legado, sem alterar posição das colunas da Nova
    legado_alinhado = legado_filtrado.reindex(columns=nova_filtrada.columns)

    if adicionar_origem:
        legado_alinhado[nome_col_origem] = "Legado"
        nova_filtrada[nome_col_origem] = "Nova"

    combinado = pd.concat([legado_alinhado, nova_filtrada], ignore_index=True)

    try:
        _salvar_arquivo(combinado, path_combinado)
    except Exception as e:
        return False, f"Erro de I/O na escrita: {e}"

    return True, f"Legado: {len(legado_filtrado):,} | Nova: {len(nova_filtrada):,} | Combinado: {len(combinado):,} -> {path_combinado}"


def main():
    base_dir = _dir_base()
    lista_referencia = _listar_arquivos_legado_e_nova(base_dir)
    arquivos_com_coluna_definida = _arquivos_em_grupos()
    arquivos_fallback = [f for f in lista_referencia if f not in arquivos_com_coluna_definida]

    data_corte_fallback = DATAS_CORTE.get(DATA_CORTE_PADRAO)
    if data_corte_fallback is None:
        raise ValueError(f"DATA_CORTE_PADRAO '{DATA_CORTE_PADRAO}' inválida.")

    print("=" * 70)
    print("PROCESSAMENTO DE CORTE TEMPORAL eLAW")
    print("=" * 70)
    print(f"Diretório Base: {base_dir}")
    datas_str = ", ".join(f"{k}={v.strftime('%d/%m/%Y')}" for k, v in DATAS_CORTE.items())
    print(f"Thresholds (Corte): {datas_str}")
    print(f"Arquivos Elegíveis (Interseção L&N): {len(lista_referencia)}")
    if arquivos_fallback:
        print(f"Arquivos em Fallback: {len(arquivos_fallback)} (Regra: '{COLUNA_DATA_PADRAO}' @ {data_corte_fallback.strftime('%d/%m/%Y')})")
    print("=" * 70)

    # Processamento dos Grupos Mapeados
    for i, grupo in enumerate(GRUPOS):
        coluna_data = grupo["coluna_data"]
        data_corte = _data_corte_do_grupo(grupo)
        chave_data = grupo.get("data_corte", DATA_CORTE_PADRAO)
        arquivos = grupo["arquivos"]
        if not arquivos:
            continue
        print(f"\n--- Grupo {i + 1}: Coluna '{coluna_data}' | Corte '{chave_data}' ({data_corte.strftime('%d/%m/%Y')}) | Qtd: {len(arquivos)} ---")
        for nome in arquivos:
            ok, msg = processar_arquivo(
                nome, base_dir, data_corte, coluna_data,
                ADICIONAR_COLUNA_ORIGEM, NOME_COLUNA_ORIGEM
            )
            if ok:
                print(f"  [OK] {nome}\n       {msg}")
            else:
                print(f"  [ERRO] {nome}\n         {msg}")

    # Processamento de Fallback (Arquivos sem grupo definido)
    if arquivos_fallback:
        print(f"\n--- Processamento Fallback: Coluna '{COLUNA_DATA_PADRAO}' | Corte {data_corte_fallback.strftime('%d/%m/%Y')} ---")
        for nome in arquivos_fallback:
            ok, msg = processar_arquivo(
                nome, base_dir, data_corte_fallback, COLUNA_DATA_PADRAO,
                ADICIONAR_COLUNA_ORIGEM, NOME_COLUNA_ORIGEM
            )
            if ok:
                print(f"  [OK] {nome}\n       {msg}")
            else:
                print(f"  [ERRO] {nome}\n         {msg}")

    print("\n" + "=" * 70)
    print("Processamento Concluído.")
    print("=" * 70)


if __name__ == "__main__":
    main()