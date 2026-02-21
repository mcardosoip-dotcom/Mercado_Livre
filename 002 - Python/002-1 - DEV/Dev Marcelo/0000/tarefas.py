"""
Lista de tarefas (queries + tabelas BQ) - Mesa de entrada MySQL para BigQuery.
Usado no workflow n8n como referência e pelo Code node (Python).
"""

TAREFAS = [
    {
        "query": "SELECT *, DAYOFWEEK(fecha) AS dia_semana FROM vista_entradas",
        "tableName": "vista_entradas",
    },
    {"query": "SELECT * FROM dw_hist_casos_x_estado", "tableName": "dw_hist_casos_x_estado"},
    {"query": "SELECT * FROM entradas", "tableName": "tab_entradas"},
    {
        "query": "SELECT * FROM vista_cantidad_casos_usuarios",
        "tableName": "vista_cantidad_casos_usuarios",
    },
    {"query": "SELECT * FROM vista_usuarios", "tableName": "vista_usuarios"},
    {"query": "SELECT * FROM mesa_entrada.v_metricas_qa", "tableName": "v_metricas_qa"},
    {"query": "SELECT * FROM mesa_entrada.estados", "tableName": "estados"},
    {"query": "SELECT * FROM mesa_entrada.tipo_documentos", "tableName": "tipo_documentos"},
    {
        "query": "SELECT * FROM mesa_entrada.metricas_big_query",
        "tableName": "metricas_big_query",
    },
    {"query": "SELECT * FROM mesa_entrada.origenes", "tableName": "origenes"},
    {"query": "SELECT * FROM mesa_entrada.entradas_estados", "tableName": "entradas_estados"},
]


def get_tarefas_n8n():
    """Retorna lista no formato esperado pelo n8n (Code node Python)."""
    return [{"json": t} for t in TAREFAS]


if __name__ == "__main__":
    import json
    print(json.dumps(get_tarefas_n8n(), indent=2))
