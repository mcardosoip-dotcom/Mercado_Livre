-- =============================================================================
-- STEP 3 - eLAW | Carga de tabelas STG - Legado
-- =============================================================================

-- =============================================================================
-- TEMA: TAREFAS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tarefas Agendadas (Subsídios Hispanos)
-- -----------------------------------------------------------------------------

-- Acompanhamento de Tarefas CORP CX
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_ACOMPANHAMENTO_DE_TAREFAS_CORP_CX_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Acompanhamento_de_tarefas_CORP_CX_legado.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos CAP
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP_legado.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos CAP CX
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_CAP_CX_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_CAP_CX_legado.parquet']
);

-- Tarefas Agendadas: Subsídios Hispanos DR
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_DR_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_DR_legado.parquet']
);

-- Tarefas Agendadas: OPS Enli
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_ENLI_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Enli_legado.parquet']
);

-- Tarefas Agendadas: OPS Inter
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_SUBSIDIOS_HISPANOS_OPS_INTER_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Subsidios_Hispanos_OPS_Inter_legado.parquet']
);

-- Tarefas Agendadas: Aguardando Informações
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDADAS_AGUARDANDO_INFORMACOES_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendadas_Aguardando_Informacoes_legado.parquet']
);

-- -----------------------------------------------------------------------------
-- Agendamentos Subsídios Clean
-- -----------------------------------------------------------------------------

-- Agendamentos Subsídios Clean: Confirmados
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_CONFIRMADOS_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Confirmados_legado.parquet']
);

-- Agendamentos Subsídios Clean: Pendentes
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_PENDENTES_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Pendentes_legado.parquet']
);

-- Agendamentos Subsídios Clean: Audiências
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_AUDIENCIAS_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Audiencias_legado.parquet']
);

-- Agendamentos Subsídios Clean: Garantias
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_TAREFAS_AGENDAMENTOS_SUBSIDIOS_CLEAN_GARANTIAS_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Tarefas_Agendamentos_Subsidios_Clean_Garantias_legado.parquet']
);

-- =============================================================================
-- TEMA: OUTROS
-- =============================================================================

-- Base Amélia (opcional: descomente quando Database_eLAW_Amelia_legado.parquet
-- for gerado e enviado ao bucket pela rotina legado / Carga em Bucket)
-- LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_AMELIA_legado
-- FROM FILES (
--   format = 'PARQUET',
--   uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Amelia_legado.parquet']
-- );

-- =============================================================================
-- TEMA: CONTENCIOSO - OUTGOING
-- =============================================================================

-- Outgoing Brasil
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_OUTGOING_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Contencioso_Brasil_Outgoing_legado.parquet']
);

-- Outgoing Hispanos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_OUTGOING_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Contencioso_Hispanos_Outgoing_legado.parquet']
);

-- =============================================================================
-- TEMA: CONTENCIOSO - INCOMING E MULTAS
-- =============================================================================

-- Incoming Brasil
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_BRASIL_INCOMING_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Contencioso_Brasil_Incoming_legado.parquet']
);

-- Incoming Hispanos
LOAD DATA OVERWRITE STG.STG_INPUT_DATABASE_ELAW_CONTENCIOSO_HISPANOS_INCOMING_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Contencioso_Hispanos_Incoming_legado.parquet']
);

-- Extração de Multas
LOAD DATA OVERWRITE STG.Database_eLAW_Extracao_multas_legado
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/eLAW_Databases_legado/Database_eLAW_Extracao_multas_legado.parquet']
);
