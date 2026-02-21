Corte temporal eLAW — Legado + Nova -> Combinado
================================================

Estrutura:
  Corte_temporal_eLAW/
    Legado/     <- versões legado dos arquivos (até a data de corte)
    Nova/       <- versões novas dos arquivos (após a data de corte)
    Combinado/  <- saída: um arquivo por item da lista, com corte aplicado
    corte_temporal_combinar.py

Uso:
  1. Defina DATA_CORTE e GRUPOS no início de corte_temporal_combinar.py.
  2. Em GRUPOS, cada grupo tem "coluna_data" (nome da coluna de data) e "arquivos" (lista de nomes).
     Arquivos com estruturas diferentes podem usar colunas de corte diferentes (cada grupo sua coluna).
  3. Coloque em Legado/ e Nova/ os arquivos com os mesmos nomes indicados nos grupos.
  4. Execute: python corte_temporal_combinar.py

Regra:
  - Registros com data <= DATA_CORTE são tomados do arquivo em Legado.
  - Registros com data > DATA_CORTE são tomados do arquivo em Nova.
  - O resultado é salvo em Combinado/ com o mesmo nome do arquivo.
