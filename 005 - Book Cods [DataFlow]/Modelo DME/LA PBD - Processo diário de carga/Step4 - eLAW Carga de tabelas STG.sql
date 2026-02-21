--------------------------------------------------------------------------------
-- TEMA: TAREFAS
--------------------------------------------------------------------------------

-- Acompanhamento de Tarefas CORP CX
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_ACOMPANHAMENTO_DE_TAREFAS_CORP_CX
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Acompanhamento_de_tarefas_CORP_CX.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos CAP
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos CAP CX
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP_CX.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos DR
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_DR
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos OPS Enli
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Enli.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos OPS Inter
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Inter.parquet']
);

-- Tarefas Agendadas: Aguardando Informações
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendadas_Aguardando_Informacoes.parquet']
);

-- Agendamentos Subsídios Clean: Confirmados
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_CONFIRMADOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados.parquet']
);

-- Agendamentos Subsídios Clean: Pendentes
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_PENDENTES
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes.parquet']
);

-- Agendamentos Subsídios Clean: Audiências
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_AUDIENCIAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias.parquet']
);

-- Agendamentos Subsídios Clean: Garantias
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_GARANTIAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias.parquet']
);





--------------------------------------------------------------------------------
-- TEMA: OUTROS
--------------------------------------------------------------------------------

-- Base Amélia
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_AMELIA
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Amelia.parquet']
);

-- Extração de Multas
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_EXTRACAO_MULTAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Extracao_multas.parquet']
);

-- Obrigações de Fazer
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_OBRIGACOES_DE_FAZER
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Obrigacoes_de_Fazer.parquet']
);

-- Obrigações de Fazer com Multas
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_OBRIGACOES_DE_FAZER_COM_MULTAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Obrigacoes_de_Fazer_Com_Multas.parquet']
);

-- Relatório de Garantia Veículos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_VEICULOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Relatorio_de_Garantia_Veiculo.parquet']
);





--------------------------------------------------------------------------------
-- TEMA: CONTENCIOSO - ONGOING
--------------------------------------------------------------------------------

-- Ongoing Brasil
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_ONGOING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Brasil_Ongoing.parquet']
);

-- Ongoing Hispanos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_ONGOING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Hispanos_Ongoing.parquet']
);





--------------------------------------------------------------------------------
-- TEMA: CONTENCIOSO - OUTGOING
--------------------------------------------------------------------------------

-- Outgoing Brasil
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Brasil_Outgoing.parquet']
);

-- Outgoing Hispanos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Hispanos_Outgoing.parquet']
);





--------------------------------------------------------------------------------
-- TEMA: CONTENCIOSO - BASE DE ENCERRADOS (Histórico)
--------------------------------------------------------------------------------
-- Carga desativada: tabela não é referenciada em nenhum step downstream (Step5, Step6, Step11).
-- Encerrados entram via Outgoing (WHERE STATUS = 'Encerrado'). Para reativar, descomentar o bloco abaixo.
--
-- DEPENDÊNCIA: O arquivo deve existir em GCS antes desta etapa.
-- Path esperado: gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Base_de_encerrados/
-- Nome: Base_Consolidada_Encerrados_eLAW.parquet (ou Base_Consolidada_Encerrados_eLAW*.parquet)
--
-- Base consolidada encerrados eLAW (Encerrados + Entradas, sem duplicidade ID, sem Status Ativo)
-- LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_BASE_ENCERRADOS
-- FROM FILES (
--   format = 'PARQUET',
--   uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Base_de_encerrados/Base_Consolidada_Encerrados_eLAW*.parquet']
-- );





--------------------------------------------------------------------------------
-- TEMA: CONTENCIOSO - INCOMING
--------------------------------------------------------------------------------

-- Incoming Brasil
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Brasil_Incoming.parquet']
);

-- Incoming Hispanos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Contencioso_Hispanos_Incoming.parquet']
);





--------------------------------------------------------------------------------
-- TEMA: AMÉLIA PARA PAULA (RPA)
--------------------------------------------------------------------------------

-- Seguimiento RPA Tarefas
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_SEGUIMIENTO_RPA_TAREFAS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Seguimiento_RPA_Tarefas.parquet']
);

-- Seguimiento RPA Pagos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_SEGUIMIENTO_RPA_PAGOS
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases/Database_eLAW_Seguimiento_RPA_Pagos.parquet']
);
