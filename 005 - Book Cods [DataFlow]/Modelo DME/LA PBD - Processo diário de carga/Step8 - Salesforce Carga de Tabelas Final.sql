-- ============================
-- SALESFORCE_INCOMING_EMBARGOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_INCOMING_EMBARGOS` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(issue_tipo_de_registro AS STRING) AS issue_tipo_de_registro,
  CAST(legales_reiteratorio AS STRING) AS legales_reiteratorio,
  CAST(legales_fecha_de_recepcion AS STRING) AS legales_fecha_de_recepcion,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(issue_creado_por AS STRING) AS issue_creado_por,
  CAST(issue_id AS STRING) AS issue_id,
  CAST(pais AS STRING) AS pais,
  CAST(respuesta_negativa AS STRING) AS respuesta_negativa
FROM `<ENV>.STG.SALESFORCE_INCOMING_EMBARGOS`;


-- ============================
-- SALESFORCE_INCOMING_OFICIOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_INCOMING_OFICIOS` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(legales_reiteratorio AS STRING) AS legales_reiteratorio,
  CAST(issue_tipo_de_registro AS STRING) AS issue_tipo_de_registro,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(issue_creado_por AS STRING) AS issue_creado_por,
  CAST(pais AS STRING) AS pais,
  CAST(respuesta_negativa AS STRING) AS respuesta_negativa
FROM `<ENV>.STG.SALESFORCE_INCOMING_OFICIOS`;


-- ============================
-- SALESFORCE_OUTCOMING_OFICIOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_OUTCOMING_OFICIOS` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(issue_ultima_modificacion_por AS STRING) AS issue_ultima_modificacion_por,
  CAST(legales_fecha_aprobacion AS STRING) AS legales_fecha_aprobacion,
  CAST(pais AS STRING) AS pais,
  CAST(respuesta_negativa AS STRING) AS respuesta_negativa
FROM `<ENV>.STG.SALESFORCE_OUTCOMING_OFICIOS`;


-- ============================
-- SALESFORCE_OUTGOING_EMBARGOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_OUTGOING_EMBARGOS` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(issue_ultima_modificacion_por AS STRING) AS issue_ultima_modificacion_por,
  CAST(legales_fecha_aprobacion AS STRING) AS legales_fecha_aprobacion,
  CAST(pais AS STRING) AS pais,
  CAST(respuesta_negativa AS STRING) AS respuesta_negativa
FROM `<ENV>.STG.SALESFORCE_OUTGOING_EMBARGOS`;


-- ============================
-- SALESFORCE_PENDING_EMBARGOS_BCRA_E_NAO_BCRA
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_PENDING_EMBARGOS_BCRA_E_NAO_BCRA` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(pais AS STRING) AS pais,
  CAST(ncausa_expediente AS STRING) AS ncausa_expediente,
  CAST(legales_autoridad_interviniente AS STRING) AS legales_autoridad_interviniente,
  CAST(numero_de_oe AS STRING) AS numero_de_oe,
  CAST(legales_approval_status AS STRING) AS legales_approval_status,
  CAST(legales_otros_requerimientos AS STRING) AS legales_otros_requerimientos,
  CAST(legales_otros_requerimientos2 AS STRING) AS legales_otros_requerimientos2,
  CAST(legales_otros_requerimientos3 AS STRING) AS legales_otros_requerimientos3,
  CAST(representante_asignado AS STRING) AS representante_asignado,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(legales_fecha_de_recepcion AS STRING) AS legales_fecha_de_recepcion
FROM `<ENV>.STG.SALESFORCE_PENDING_EMBARGOS_BCRA_E_NAO_BCRA`;


-- ============================
-- SALESFORCE_PENDING_INFORMATIVOS
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_PENDING_INFORMATIVOS` AS
SELECT
  CAST(issue_number AS STRING) AS issue_number,
  CAST(pais AS STRING) AS pais,
  CAST(legales_approval_status AS STRING) AS legales_approval_status,
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(legales_fecha_de_recepcion AS STRING) AS legales_fecha_de_recepcion
FROM `<ENV>.STG.SALESFORCE_PENDING_INFORMATIVOS`;


-- ============================
-- SALESFORCE_BCRA_OE_ISSUE
-- ============================
CREATE OR REPLACE TABLE `<ENV>.STG.SALESFORCE_BCRA_OE_ISSUE` AS
SELECT
  CAST(issue_fecha_de_creacion AS STRING) AS issue_fecha_de_creacion,
  CAST(issue_number AS STRING) AS issue_number,
  CAST(numero_de_oe AS STRING) AS numero_de_oe
FROM `<ENV>.STG.SALESFORCE_BCRA_OE_ISSUE`;

