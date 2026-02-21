/**
 * =============================================================================
 * SCRIPT UNIFICADO - ROTINA DE CRUCES DE VALIDAÇÃO DE RETENÇÕES
 * =============================================================================
 * Planilha: https://docs.google.com/spreadsheets/d/1THO6WBD5lTCyBtgrJBVacsOdX7cB5ecgwzAwy1sUUq8/
 * Aba fonte: "base de solicitações"
 * Aba controle (email): "Controle" (A5 = Sim/Não, A8+ = lista de emails)
 * Resultados escritos nesta mesma planilha (CRUCE_*, RESUMO) - não altera a base.
 *
 * ACIONADOR MANUAL: Editor do Apps Script → selecione a função "executarRotinaDiaria"
 * no dropdown, depois clique em "Executar" (ícone de play). Ou use o Trigger (Relógio)
 * para agendar (ex.: toda manhã).
 * =============================================================================
 */

const SPREADSHEET_ID = "1THO6WBD5lTCyBtgrJBVacsOdX7cB5ecgwzAwy1sUUq8";
const PROJECT_ID_BQ = "ddme000426-gopr4nla6zo-furyid";
const DATASET_ID = "STG";
const PROJECT_ID_QUERY = "meli-bi-data";

/** Array global para acumular linhas do log e gravar na aba Controle (C2 em diante). */
var LOG_LINHAS = [];

/**
 * Registra mensagem no Logger e na lista para gravar na planilha (aba Controle, coluna C).
 * Mensagens com \n são quebradas em uma linha por vez.
 */
function logMsg(msg) {
  var texto = (msg === undefined || msg === null) ? "" : String(msg);
  Logger.log(texto);
  var linhas = texto.split("\n");
  for (var i = 0; i < linhas.length; i++) {
    LOG_LINHAS.push(linhas[i]);
  }
}

/**
 * Zera o log na aba Controle (C2 em diante) e grava as linhas acumuladas em LOG_LINHAS.
 * Chamado no início da rotina (zerar) e no fim (gravar).
 */
function salvarLogNaPlanilha(zerarApenas) {
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var aba = ss.getSheetByName("Controle");
    if (!aba) return;
    var maxLinhas = 999;
    var rangeLog = aba.getRange(2, 3, maxLinhas, 1);
    if (zerarApenas) {
      rangeLog.clearContent();
      return;
    }
    if (LOG_LINHAS.length === 0) return;
    var dados = LOG_LINHAS.map(function(linha) { return [linha]; });
    rangeLog.clearContent();
    aba.getRange(2, 3, dados.length, 1).setValues(dados);
  } catch (e) {
    Logger.log("Erro ao salvar log na planilha: " + e.toString());
  }
}

// -----------------------------------------------------------------------------
// ORQUESTRADOR GERAL (agendar no Trigger ou rodar manualmente)
// -----------------------------------------------------------------------------

/**
 * Executa a rotina completa: tabelas externas → query → resultados na planilha → email (se A5 = Sim).
 * Para acionador manual: no editor do Apps Script, selecione esta função e clique em "Executar".
 */
function executarRotinaDiaria() {
  LOG_LINHAS = [];
  salvarLogNaPlanilha(true);

  const inicio = new Date();
  logMsg("🏁 [INÍCIO] Rotina diária de validação: " + inicio);

  try {
    logMsg("");
    logMsg("⏳ [PASSO 1/3] Criando/Atualizando Tabelas Externas e Views...");
    criarTodasAsTabelasExternas();
    logMsg("✅ [PASSO 1] Concluído.");

    Utilities.sleep(2000);

    logMsg("");
    logMsg("⏳ [PASSO 2/3] Executando Query no BigQuery e escrevendo na Planilha...");
    processarCrucesNoBigQuery();
    logMsg("✅ [PASSO 2] Concluído.");

    logMsg("");
    logMsg("⏳ [PASSO 3/3] Relatório e e-mail (conforme Controle)...");
    exportarRelatoriosCrucePorEmail();
    logMsg("✅ [PASSO 3] Concluído.");

  } catch (erro) {
    logMsg("❌ ERRO CRÍTICO: " + erro.toString());
    try {
      MailApp.sendEmail(
        "seu.email@mercadolivre.com",
        "ALERTA: Falha na Rotina de Cruces",
        "Erro:\n\n" + erro.toString()
      );
    } catch (e) {
      logMsg("Falha ao enviar email de alerta: " + e.toString());
    }
  }

  const fim = new Date();
  logMsg("");
  logMsg("🏁 [FIM] Rotina finalizada em " + ((fim - inicio) / 1000) + " segundos.");
  salvarLogNaPlanilha(false);
}

// =============================================================================
// PASSO 1: TABELAS EXTERNAS E VIEWS (lê da aba "base de solicitações")
// =============================================================================

function criarTodasAsTabelasExternas() {
  logMsg("==== CRIAÇÃO DE TABELAS E VIEWS ====");

  const tabelas = [
    {
      nome: "base_integridade",
      id: SPREADSHEET_ID,
      aba: "base de solicitações",
      cabecalho: "A1:R1",
      colunasFloat: ["monto_total", "valor_liquido", "outra_coluna_valor"]
    }
  ];

  const tabelasCriadas = [];

  tabelas.forEach(t => {
    try {
      logMsg("➡️ Processando: " + t.nome + " ...");
      const nomeTabelaExterna = "ext_" + t.nome;
      const nomeViewFinal = t.nome;

      const schema = createExternalTableFromSheet(
        PROJECT_ID_BQ,
        DATASET_ID,
        nomeTabelaExterna,
        t.id,
        t.aba,
        t.cabecalho
      );

      if (schema && schema.length > 0) {
        createCorrectedView(
          PROJECT_ID_BQ,
          DATASET_ID,
          nomeViewFinal,
          nomeTabelaExterna,
          schema,
          t.colunasFloat || []
        );
      }
      tabelasCriadas.push(nomeViewFinal);
      Utilities.sleep(1000);
    } catch (e) {
      logMsg("❌ Falha " + t.nome + ": " + e.message);
    }
  });

  if (tabelasCriadas.length > 0) {
    logMsg("✅ Views criadas: " + tabelasCriadas.join(", "));
  } else {
    logMsg("⚠️ Nenhuma tabela criada.");
  }
  logMsg("==== FIM ====");
}

function createExternalTableFromSheet(projectId, datasetId, baseTableName, spreadsheetId, sheetName, headerRange) {
  const externalTableName = projectId + "." + datasetId + "." + baseTableName;
  logMsg("   [ETAPA 1] Tabela Externa: " + baseTableName);

  const ss = SpreadsheetApp.openById(spreadsheetId);
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) throw new Error('Aba "' + sheetName + '" não encontrada.');

  const headerRow = sheet.getRange(headerRange).getValues()[0];
  const spreadsheetUrl = ss.getUrl();
  const sheetGid = sheet.getSheetId();

  const sanitizeColumnName = function(colName) {
    if (!colName) return "coluna_vazia";
    let clean = colName.toString().replace(/[^a-zA-Z0-9\s_]/g, "");
    clean = clean.replace(/[\s_]+/g, "_").replace(/^_+|_+$/g, "");
    return clean.toLowerCase();
  };

  const cleanedHeader = headerRow.map(sanitizeColumnName);

  const numToColLetter = function(num) {
    var temp, letter = "";
    while (num > 0) {
      temp = (num - 1) % 26;
      letter = String.fromCharCode(temp + 65) + letter;
      num = (num - temp - 1) / 26;
    }
    return letter;
  };

  const lastColumnLetter = numToColLetter(cleanedHeader.length);
  const schemaDefinition = cleanedHeader.map(function(c) { return "`" + c + "` STRING"; }).join(",\n   ");
  const finalUri = spreadsheetUrl.split("/edit")[0] + "/edit#gid=" + sheetGid;

  const sqlCreateExternal =
    "CREATE OR REPLACE EXTERNAL TABLE `" + externalTableName + "` (\n   " + schemaDefinition + "\n)\n" +
    "OPTIONS (\n  format = 'GOOGLE_SHEETS',\n  skip_leading_rows = 1,\n  sheet_range = '" + sheetName + "!A2:" + lastColumnLetter + "',\n  uris = ['" + finalUri + "']\n);";

  runBigQueryJob(sqlCreateExternal, projectId);
  logMsg("   --> Tabela externa criada.");
  return cleanedHeader;
}

function createCorrectedView(projectId, datasetId, viewName, sourceTableName, columns, floatColumns) {
  const fullViewName = projectId + "." + datasetId + "." + viewName;
  const fullSourceTable = projectId + "." + datasetId + "." + sourceTableName;
  logMsg("   [ETAPA 2] View: " + viewName);

  try {
    runBigQueryJob("DROP TABLE IF EXISTS `" + fullViewName + "`", projectId);
  } catch (e) {}

  const selectClause = columns.map(function(col) {
    if (floatColumns.indexOf(col) !== -1) {
      return "SAFE_CAST(REPLACE(`" + col + "`, ',', '.') AS FLOAT64) AS `" + col + "`";
    }
    return "`" + col + "`";
  }).join(",\n     ");

  const sqlCreateView =
    "CREATE OR REPLACE VIEW `" + fullViewName + "` AS\nSELECT\n     " + selectClause + "\nFROM `" + fullSourceTable + "`";
  runBigQueryJob(sqlCreateView, projectId);
  logMsg("   --> View criada.");
}

function runBigQueryJob(sql, projectId) {
  var job = BigQuery.newJob();
  job.setConfiguration({ query: { query: sql, useLegacySql: false } });
  var queryJob = BigQuery.Jobs.insert(job, projectId);
  var jobId = queryJob.getJobReference().getJobId();
  while (!queryJob.getStatus().getState().match(/DONE/)) {
    Utilities.sleep(1000);
    queryJob = BigQuery.Jobs.get(projectId, jobId);
  }
  if (queryJob.getStatus().getErrorResult()) {
    throw new Error("BigQuery: " + queryJob.getStatus().getErrorResult().getMessage());
  }
}

// =============================================================================
// PASSO 2: QUERY E ESCRITA NA PLANILHA (mesma planilha, abas CRUCE_* e RESUMO)
// =============================================================================

function processarCrucesNoBigQuery() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  logMsg(">> Executando Cruzamentos SQL...");
  const resultados = executarQueryDeCruzamento();
  logMsg(">> Escrevendo resultados na planilha...");
  distribuirResultadosNaPlanilha(ss, resultados);
}

function executarQueryDeCruzamento() {
  const sql = [
    "WITH base_sheet AS (",
    "  SELECT",
    "    id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia AS id_deuda,",
    "    CAST(REPLACE(CAST(monto_total AS STRING), ',', '.') AS FLOAT64) AS monto_transferido,",
    "    LOWER(cul_es_el_tipo_de_cuenta) AS tipo_conta,",
    "    TRIM(CAST(cbu_22_dgitos AS STRING)) AS cbu_informado,",
    "    CAST(issue_en_salesforce AS STRING) as issue_salesforce,",
    "    COUNT(*) OVER (",
    "      PARTITION BY id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia,",
    "                   SAFE_CAST(REPLACE(CAST(monto_total AS STRING), ',', '.') AS NUMERIC)",
    "    ) as qtd_ocorrencias",
    "  FROM `" + PROJECT_ID_BQ + "." + DATASET_ID + ".base_integridade`",
    "),",
    "base_bq AS (",
    "  SELECT CAST(DEBT_ID AS INT64) AS DEBT_ID, DEBT_PAID_AMOUNT, DEBT_STATUS_DETAIL, DEBT_DEBT_TYPE_ID",
    "  FROM `meli-bi-data.WHOWNER.BT_MP_DISB_DEBT`",
    "  WHERE DEBT_DEBT_TYPE_ID IN (442, 77, 459, 437)",
    "),",
    "FINAL AS (",
    "  SELECT",
    "    sheet.id_deuda,",
    "    CURRENT_TIMESTAMP() as data_execucao,",
    "    CASE",
    "      WHEN bq.DEBT_ID IS NULL THEN 'CRUCE_2'",
    "      WHEN sheet.monto_transferido IS NULL THEN 'ERROR_DATA_SUJA'",
    "      WHEN sheet.qtd_ocorrencias > 1 THEN 'CRUCE_6_DUPLICADOS'",
    "      WHEN sheet.cbu_informado IS NOT NULL AND NOT REGEXP_CONTAINS(sheet.cbu_informado, r'^[0-9]{22}$') THEN 'CRUCE_5_TESTE_CBU'",
    "      WHEN bq.DEBT_ID IS NOT NULL AND (",
    "        (sheet.tipo_conta LIKE '%no remun%' AND bq.DEBT_DEBT_TYPE_ID NOT IN (77, 437, 459))",
    "        OR (sheet.tipo_conta NOT LIKE '%no remun%' AND sheet.tipo_conta LIKE '%remun%' AND bq.DEBT_DEBT_TYPE_ID != 442)",
    "      ) THEN 'CRUCE_7_DEBT_TYPE_INCORRETO'",
    "      WHEN TRUNC(sheet.monto_transferido) > TRUNC(bq.DEBT_PAID_AMOUNT) THEN 'CRUCE_1'",
    "      WHEN TRUNC(sheet.monto_transferido) < TRUNC(bq.DEBT_PAID_AMOUNT) THEN 'CRUCE_4'",
    "      WHEN (sheet.tipo_conta LIKE '%remun%') AND (bq.DEBT_STATUS_DETAIL NOT IN ('executed','partially_executed','awaiting_confirmation')) AND (bq.DEBT_ID IS NOT NULL) AND (bq.DEBT_DEBT_TYPE_ID = 442) THEN 'CRUCE_3'",
    "      ELSE 'OK'",
    "    END as status_cruce,",
    "    sheet.monto_transferido,",
    "    bq.DEBT_PAID_AMOUNT,",
    "    (IFNULL(sheet.monto_transferido,0) - IFNULL(bq.DEBT_PAID_AMOUNT,0)) as diferenca,",
    "    sheet.cbu_informado,",
    "    sheet.issue_salesforce,",
    "    sheet.tipo_conta,",
    "    bq.DEBT_DEBT_TYPE_ID",
    "  FROM base_sheet sheet",
    "  LEFT JOIN base_bq bq ON CAST(sheet.id_deuda AS STRING) = CAST(bq.DEBT_ID AS STRING)",
    "  WHERE bq.DEBT_ID IS NULL OR sheet.monto_transferido IS NULL OR sheet.qtd_ocorrencias > 1",
    "    OR (sheet.cbu_informado IS NOT NULL AND NOT REGEXP_CONTAINS(sheet.cbu_informado, r'^[0-9]{22}$'))",
    "    OR (bq.DEBT_ID IS NOT NULL AND (",
    "      (sheet.tipo_conta LIKE '%no remun%' AND bq.DEBT_DEBT_TYPE_ID NOT IN (77, 437, 459))",
    "      OR (sheet.tipo_conta NOT LIKE '%no remun%' AND sheet.tipo_conta LIKE '%remun%' AND bq.DEBT_DEBT_TYPE_ID != 442)",
    "    ))",
    "    OR TRUNC(sheet.monto_transferido) != TRUNC(bq.DEBT_PAID_AMOUNT)",
    "    OR ((sheet.tipo_conta LIKE '%remun%') AND (bq.DEBT_STATUS_DETAIL NOT IN ('executed','partially_executed','awaiting_confirmation')) AND (bq.DEBT_DEBT_TYPE_ID = 442))",
    "  )",
    "SELECT * FROM FINAL"
  ].join("\n");

  const jobConfig = {
    configuration: {
      query: {
        query: sql,
        useLegacySql: false
      }
    }
  };
  logMsg(">> Enviando Job BigQuery...");
  var job = BigQuery.Jobs.insert(jobConfig, PROJECT_ID_QUERY);
  var jobId = job.jobReference.jobId;
  var jobStatus = BigQuery.Jobs.get(PROJECT_ID_QUERY, jobId);
  while (jobStatus.status.state !== "DONE") {
    Utilities.sleep(3000);
    jobStatus = BigQuery.Jobs.get(PROJECT_ID_QUERY, jobId);
  }
  if (jobStatus.status.errorResult) {
    throw new Error("BigQuery: " + jobStatus.status.errorResult.message);
  }
  var gb = (jobStatus.statistics.query.totalBytesProcessed / (1024 * 1024 * 1024)).toFixed(2);
  logMsg("✅ Job concluído. Dados: " + gb + " GB");

  var rows = [];
  var pageToken = null;
  do {
    var results = BigQuery.Jobs.getQueryResults(PROJECT_ID_QUERY, jobId, { pageToken: pageToken });
    if (results.rows) rows = rows.concat(results.rows);
    pageToken = results.pageToken;
  } while (pageToken);
  logMsg(">> Divergências: " + rows.length);
  return rows;
}

function distribuirResultadosNaPlanilha(ss, rows) {
  var c1 = [], c2 = [], c3 = [], c4 = [], c5 = [], c6 = [], c7 = [];
  const dataFormatada = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");

  if (rows && rows.length > 0) {
    rows.forEach(function(r) {
      var id = r.f[0].v;
      if (id === null || id === "" || id === undefined) return;
      var tipo = r.f[2].v;
      var valSheet = r.f[3].v ? Number(r.f[3].v) : 0;
      var valBQ = r.f[4].v ? Number(r.f[4].v) : 0;
      var diff = r.f[5].v ? Number(r.f[5].v) : 0;
      var cbuInvalido = r.f[6] ? r.f[6].v : "N/A";
      var issueSf = r.f[7] ? r.f[7].v : "N/A";
      var tipoContaSheet = r.f[8] ? r.f[8].v : "";
      var tipoContaBQ = r.f[9] ? r.f[9].v : "";
      var linhaPadrao = [id, dataFormatada];

      if (tipo === "CRUCE_1") c1.push([id, dataFormatada, valSheet, valBQ, diff]);
      else if (tipo === "CRUCE_2") c2.push(linhaPadrao);
      else if (tipo === "CRUCE_3") c3.push(linhaPadrao);
      else if (tipo === "CRUCE_4") c4.push(linhaPadrao);
      else if (tipo === "CRUCE_5_TESTE_CBU") c5.push([id, dataFormatada, cbuInvalido]);
      else if (tipo === "CRUCE_6_DUPLICADOS") c6.push([id, dataFormatada, issueSf, valSheet]);
      else if (tipo === "CRUCE_7_DEBT_TYPE_INCORRETO") c7.push([id, dataFormatada, tipoContaSheet, tipoContaBQ]);
    });
  }

  var nomes = [
    "CRUCE_1_VALOR_MAIOR_QUE_RETIDO",
    "CRUCE_2_ERRO_ID_DEUDA",
    "CRUCE_3_ENLIGHTEN_NAO_EXECUTOU",
    "CRUCE_4_VALOR_MENOR_QUE_RETIDO",
    "CRUCE_5_TESTE_CBU",
    "CRUCE_6_DUPLICADOS",
    "CRUCE_7_DEBT_TYPE_INCORRETO"
  ];
  escreverAba(ss, nomes[0], c1, ["DEBT_ID", "Data Execução", "Vl. Planilha", "Vl. BigQuery", "Diferença"]);
  var headerPadrao = ["DEBT_ID", "Data Execução"];
  escreverAba(ss, nomes[1], c2, headerPadrao);
  escreverAba(ss, nomes[2], c3, headerPadrao);
  escreverAba(ss, nomes[3], c4, headerPadrao);
  escreverAba(ss, nomes[4], c5, ["DEBT_ID", "Data Execução", "CBU Inválido"]);
  escreverAba(ss, nomes[5], c6, ["DEBT_ID", "Data Execução", "Issue Salesforce", "Valor Duplicado"]);
  escreverAba(ss, nomes[6], c7, ["DEBT_ID", "Data Execução", "Tipo na Planilha", "Tipo no Banco (ID)"]);
  atualizarResumo(ss, c1.length, c2.length, c3.length, c4.length, c5.length, c6.length, c7.length, nomes);
  logMsg(">> Processo finalizado.");
}

function escreverAba(ss, nomeAba, dados, cabecalho) {
  var aba = ss.getSheetByName(nomeAba);
  if (!aba) aba = ss.insertSheet(nomeAba);
  aba.clear();
  aba.appendRow(cabecalho);
  if (dados.length > 0) {
    // getRange(row, col, numRows, numCols): 3º parâmetro = quantidade de linhas, não linha final
    var numRows = dados.length;
    var numCols = dados[0].length;
    aba.getRange(2, 1, numRows, numCols).setValues(dados);
  } else {
    aba.appendRow(["Nenhum caso encontrado", ""]);
  }
}

function atualizarResumo(ss, q1, q2, q3, q4, q5, q6, q7, nomes) {
  var aba = ss.getSheetByName("RESUMO");
  if (!aba) aba = ss.insertSheet("RESUMO");
  aba.clear();
  var hoje = new Date();
  aba.appendRow(["CRUCE", "Quantidade", "Data Execução"]);
  aba.appendRow([nomes[0], q1, hoje]);
  aba.appendRow([nomes[1], q2, hoje]);
  aba.appendRow([nomes[2], q3, hoje]);
  aba.appendRow([nomes[3], q4, hoje]);
  aba.appendRow([nomes[4], q5, hoje]);
  aba.appendRow([nomes[5], q6, hoje]);
  aba.appendRow([nomes[6], q7, hoje]);
}

// =============================================================================
// PASSO 3: RELATÓRIO E E-MAIL (Controle: A5 = Sim/Não, A8+ = lista de emails)
// =============================================================================

function exportarRelatoriosCrucePorEmail() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var abaControle = ss.getSheetByName("Controle");
  if (!abaControle) {
    logMsg("Aba 'Controle' não encontrada. E-mail não enviado.");
    return;
  }

  var enviarEmail = (abaControle.getRange("A5").getValue() || "").toString().trim().toLowerCase();
  if (enviarEmail !== "sim") {
    logMsg("Enviar email? = '" + enviarEmail + "'. E-mail não enviado (use 'Sim' na célula A5 da aba Controle).");
    return;
  }

  var listaEmails = [];
  var ultimaLinha = Math.max(abaControle.getLastRow(), 100);
  var colA = abaControle.getRange(8, 1, ultimaLinha, 1).getValues();
  for (var i = 0; i < colA.length; i++) {
    var cel = (colA[i][0] || "").toString().trim();
    if (cel.indexOf("@") !== -1) listaEmails.push(cel);
  }
  if (listaEmails.length === 0) {
    Logger.log("Nenhum e-mail na coluna A a partir da linha 8 (aba Controle). E-mail não enviado.");
    return;
  }

  var RECEPTOR_EMAIL = listaEmails.join(",");
  var SHEET_NAMES_TO_EXPORT = [
    "RESUMO",
    "CRUCE_1_VALOR_MAIOR_QUE_RETIDO",
    "CRUCE_2_ERRO_ID_DEUDA",
    "CRUCE_3_ENLIGHTEN_NAO_EXECUTOU",
    "CRUCE_5_TESTE_CBU",
    "CRUCE_6_DUPLICADOS",
    "CRUCE_7_DEBT_TYPE_INCORRETO"
  ];
  var LABEL_MAP = {
    "CRUCE_1_VALOR_MAIOR_QUE_RETIDO": "1. Valor transferido > Retido",
    "CRUCE_2_ERRO_ID_DEUDA": "2. Erro no ID da Deuda",
    "CRUCE_3_ENLIGHTEN_NAO_EXECUTOU": "3. Enlighten não executou",
    "CRUCE_5_TESTE_CBU": "5. CBU Inválido (Regra 22 digitos)",
    "CRUCE_6_DUPLICADOS": "6. Casos Duplicados (debt ID + Valor)",
    "CRUCE_7_DEBT_TYPE_INCORRETO": "7. Debt Type Incorreto (Planilha vs BQ)"
  };
  var ASSUNTO_EMAIL = "Reporte Diário: Cruces de Validação de Retenções";
  var NOME_ARQUIVO_ANEXO = "Relatorio_Cruces_Validacao.xlsx";

  var fileBlob;
  var tempSpreadsheetId = null;
  var summaryCounts = {};

  try {
    var spreadsheetOrigem = SpreadsheetApp.openById(SPREADSHEET_ID);
    var tempSheetName = "Relatorio Cruces TEMP " + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm");
    var tempSpreadsheet = SpreadsheetApp.create(tempSheetName);
    tempSpreadsheetId = tempSpreadsheet.getId();
    var defaultSheet = tempSpreadsheet.getSheets()[0];
    var sheetsCopied = 0;

    SHEET_NAMES_TO_EXPORT.forEach(function(nomeHoja) {
      var hojaOrigem = spreadsheetOrigem.getSheetByName(nomeHoja);
      if (!hojaOrigem) return;
      var rangoDatos = hojaOrigem.getDataRange();
      var datos = rangoDatos.getValues();

      if (nomeHoja !== "RESUMO") {
        var qtd = 0;
        if (datos.length > 1) {
          var primeiraCelulaDados = String(datos[1][0]).trim();
          qtd = primeiraCelulaDados === "Nenhum caso encontrado" ? 0 : datos.length - 1;
        }
        summaryCounts[nomeHoja] = qtd;
      }

      var hojaDestino = tempSpreadsheet.insertSheet(nomeHoja);
      sheetsCopied++;
      if (datos.length > 0) {
        hojaDestino.getRange(1, 1, datos.length, datos[0].length).setValues(datos);
      }
    });

    if (sheetsCopied > 0) {
      if (tempSpreadsheet.getSheets().length > 1) tempSpreadsheet.deleteSheet(defaultSheet);

      var abaResumoTemp = tempSpreadsheet.getSheetByName("RESUMO");
      if (abaResumoTemp) {
        var dadosResumo = abaResumoTemp.getDataRange().getValues();
        for (var i = dadosResumo.length - 1; i >= 0; i--) {
          if (String(dadosResumo[i][0]).indexOf("CRUCE_4_VALOR_MENOR_QUE_RETIDO") !== -1) {
            abaResumoTemp.deleteRow(i + 1);
          }
        }
      }

      SpreadsheetApp.flush();

      var ordemExibicao = [
        "CRUCE_1_VALOR_MAIOR_QUE_RETIDO",
        "CRUCE_2_ERRO_ID_DEUDA",
        "CRUCE_3_ENLIGHTEN_NAO_EXECUTOU",
        "CRUCE_5_TESTE_CBU",
        "CRUCE_6_DUPLICADOS",
        "CRUCE_7_DEBT_TYPE_INCORRETO"
      ];
      var linhasTabelaHtml = "";
      ordemExibicao.forEach(function(key) {
        var label = LABEL_MAP[key];
        var qtd = summaryCounts[key] || 0;
        var estiloQtd = qtd > 0 ? "color: #D32F2F;" : "color: #333;";
        linhasTabelaHtml += "<tr><td style=\"padding: 12px; border-bottom: 1px solid #eee; color: #333;\">" + label + "</td><td style=\"padding: 12px; border-bottom: 1px solid #eee; text-align: right; font-weight: bold; " + estiloQtd + "\">" + qtd + "</td></tr>";
      });

      var TEXTO_EMAIL_HTML = [
        "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body style=\"margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;\">",
        "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"background-color: #f5f5f5; padding: 20px 0;\"><tr><td align=\"center\">",
        "<table width=\"600\" cellpadding=\"0\" cellspacing=\"0\" style=\"background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);\">",
        "<tr><td style=\"background: linear-gradient(135deg, #FFE600 0%, #FFF159 100%); padding: 30px 40px; text-align: center;\">",
        "<h1 style=\"margin: 0; color: #333333; font-size: 24px; font-weight: 600;\">📊 RELATÓRIO DIÁRIO</h1>",
        "<p style=\"margin: 8px 0 0 0; color: #666666; font-size: 14px;\">Cruces de Validação de Retenções</p></td></tr>",
        "<tr><td style=\"padding: 40px 40px 30px 40px;\">",
        "<p style=\"margin: 0 0 20px 0; color: #333333; font-size: 16px;\"><strong>Olá!</strong></p>",
        "<p style=\"margin: 0 0 20px 0; color: #333333; font-size: 15px; line-height: 1.6;\">Segue abaixo o resumo. O detalhe está no anexo.</p>",
        "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"margin: 20px 0; border: 1px solid #eee; border-radius: 6px;\">",
        "<thead><tr style=\"background-color: #f9f9f9;\"><th style=\"padding: 12px; text-align: left; color: #666;\">Cruce</th><th style=\"padding: 12px; text-align: right; color: #666;\">Quantidade</th></tr></thead><tbody>",
        linhasTabelaHtml,
        "</tbody></table>",
        "<p style=\"margin: 20px 0 10px 0; color: #333333; font-size: 16px; font-weight: 600;\">Obrigado!</p>",
        "<p style=\"margin: 0; color: #3483FA; font-size: 15px;\">Legal Ops Automation</p></td></tr>",
        "<tr><td style=\"background-color: #2D3277; padding: 15px; text-align: center;\"><p style=\"margin: 0; color: #ffffff; font-size: 12px;\">📎 Anexo: Relatório consolidado (.xlsx)</p></td></tr>",
        "</table></td></tr></table></body></html>"
      ].join("");

      var url = tempSpreadsheet.getUrl();
      var exportUrl = url.replace("/edit", "/export") + "?exportFormat=xlsx";
      var params = { method: "get", headers: { "Authorization": "Bearer " + ScriptApp.getOAuthToken() }, muteHttpExceptions: true };
      fileBlob = UrlFetchApp.fetch(exportUrl, params).getBlob();
      fileBlob.setName(NOME_ARQUIVO_ANEXO);

      MailApp.sendEmail({
        to: RECEPTOR_EMAIL,
        subject: ASSUNTO_EMAIL,
        htmlBody: TEXTO_EMAIL_HTML,
        attachments: [fileBlob]
      });
      Logger.log("SUCESSO: E-mail enviado para " + listaEmails.length + " destinatário(s).");
    } else {
      logMsg("ERRO: Nenhuma aba encontrada.");
    }
  } catch (e) {
    Logger.log("ERRO exportar/enviar: " + e.toString());
  } finally {
    if (tempSpreadsheetId) {
      try { DriveApp.getFileById(tempSpreadsheetId).setTrashed(true); } catch (err) {}
    }
  }
}
