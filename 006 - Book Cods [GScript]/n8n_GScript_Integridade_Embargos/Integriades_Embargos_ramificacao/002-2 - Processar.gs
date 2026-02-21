/************************************************************
 * CONFIGURAÇÕES GERAIS
 * RAMIFICAÇÃO: para IDs CRUCE_2, cruza com BT_MP_TRANSFER_ADMIN e escreve abas _2
 ************************************************************/
const PROJECT_ID = "meli-bi-data";
const PLANILHA_ID = "1hrKq2U9y7LuTZqiIpmizk4j72FTyweZcnZShawPDhgY";

function processarCrucesNoBigQuery() {
  const ss = SpreadsheetApp.openById(PLANILHA_ID);
  
  console.log(">> Executando Cruzamentos SQL...");
  const resultados = executarQueryDeCruzamento();

  // Coletar IDs que são CRUCE_2 para ramificação (Transfer Admin)
  const idsCruce2 = [];
  if (resultados && resultados.length > 0) {
    resultados.forEach(r => {
      const tipo = r.f[2] ? r.f[2].v : null;
      if (tipo === 'CRUCE_2') {
        const id = r.f[0].v;
        if (id != null && id !== '') idsCruce2.push(String(id));
      }
    });
  }

  console.log(">> Escrevendo resultados na planilha...");
  distribuirResultadosNaPlanilha(ss, resultados);

  // Ramificação: segunda query só para IDs CRUCE_2
  if (idsCruce2.length > 0) {
    console.log(`>> Ramificação: ${idsCruce2.length} IDs CRUCE_2. Cruzando com BT_MP_TRANSFER_ADMIN...`);
    const resultados2 = executarQueryDeCruzamentoTransferAdmin(idsCruce2);
    distribuirResultadosNaPlanilha_2(ss, resultados2);
  }

  console.log(">> Processo Finalizado.");
}

/************************************************************
 * PASSO 2: QUERY (DISB_DEBT)
 ************************************************************/
function executarQueryDeCruzamento() {
  const sql = `
    WITH base_sheet AS (
      SELECT
        id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia AS id_deuda,
        CAST(REPLACE(CAST(monto_total AS STRING), ',', '.') AS FLOAT64) AS monto_transferido,
        LOWER(cul_es_el_tipo_de_cuenta) AS tipo_conta, 
        TRIM(CAST(cbu_22_dgitos AS STRING)) AS cbu_informado,
        CAST(issue_en_salesforce AS STRING) as issue_salesforce,
        
        COUNT(*) OVER (
          PARTITION BY 
            id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia, 
            SAFE_CAST(REPLACE(CAST(monto_total AS STRING), ',', '.') AS NUMERIC)
        ) as qtd_ocorrencias
      FROM
        \`ddme000426-gopr4nla6zo-furyid.STG.base_integridade\`
    ),

    base_bq AS (
      SELECT
        CAST(DEBT_ID AS INT64) AS DEBT_ID,
        DEBT_PAID_AMOUNT,
        DEBT_STATUS_DETAIL,
        DEBT_DEBT_TYPE_ID 
      FROM \`meli-bi-data.WHOWNER.BT_MP_DISB_DEBT\`
      WHERE DEBT_DEBT_TYPE_ID IN (442, 77, 459, 437) 
    ),
    FINAL as (
    SELECT 
      sheet.id_deuda,
      CURRENT_TIMESTAMP() as data_execucao,
      CASE
        WHEN bq.DEBT_ID IS NULL THEN 'CRUCE_2'
        WHEN sheet.monto_transferido IS NULL THEN 'ERROR_DATA_SUJA' 
        
        -- CRUCE 6: Duplicidade
        WHEN sheet.qtd_ocorrencias > 1 THEN 'CRUCE_6_DUPLICADOS'

        -- CRUCE 5: Validação CBU
        WHEN sheet.cbu_informado IS NOT NULL 
             AND NOT REGEXP_CONTAINS(sheet.cbu_informado, r'^[0-9]{22}$') THEN 'CRUCE_5_TESTE_CBU'

        -- CRUCE 7: DEBT TYPE INCORRETO
        WHEN bq.DEBT_ID IS NOT NULL AND (
            (sheet.tipo_conta LIKE '%no remun%' AND bq.DEBT_DEBT_TYPE_ID NOT IN (77, 437, 459))
            OR
            (sheet.tipo_conta NOT LIKE '%no remun%' AND sheet.tipo_conta LIKE '%remun%' AND bq.DEBT_DEBT_TYPE_ID != 442)
        ) THEN 'CRUCE_7_DEBT_TYPE_INCORRETO'
             
        WHEN TRUNC(sheet.monto_transferido) > TRUNC(bq.DEBT_PAID_AMOUNT) THEN 'CRUCE_1'
        WHEN TRUNC(sheet.monto_transferido) < TRUNC(bq.DEBT_PAID_AMOUNT) THEN 'CRUCE_4'
        WHEN (sheet.tipo_conta LIKE '%remun%') 
             AND (bq.DEBT_STATUS_DETAIL NOT IN ('executed', 'partially_executed','awaiting_confirmation')) 
             AND (bq.DEBT_ID IS NOT NULL)
             AND (bq.DEBT_DEBT_TYPE_ID = 442) THEN 'CRUCE_3'
        ELSE 'OK'
      END as status_cruce,
      sheet.monto_transferido,
      bq.DEBT_PAID_AMOUNT,
      (IFNULL(sheet.monto_transferido, 0) - IFNULL(bq.DEBT_PAID_AMOUNT, 0)) as diferenca,
      sheet.cbu_informado,
      sheet.issue_salesforce,
      sheet.tipo_conta,         
      bq.DEBT_DEBT_TYPE_ID      
    FROM base_sheet sheet
    LEFT JOIN base_bq bq ON CAST(sheet.id_deuda as STRING) = CAST(bq.DEBT_ID AS STRING)
    WHERE 
      bq.DEBT_ID IS NULL 
      OR sheet.monto_transferido IS NULL 
      OR sheet.qtd_ocorrencias > 1
      OR (sheet.cbu_informado IS NOT NULL AND NOT REGEXP_CONTAINS(sheet.cbu_informado, r'^[0-9]{22}$'))
      OR (
          bq.DEBT_ID IS NOT NULL AND (
            (sheet.tipo_conta LIKE '%no remun%' AND bq.DEBT_DEBT_TYPE_ID NOT IN (77, 437, 459))
            OR
            (sheet.tipo_conta NOT LIKE '%no remun%' AND sheet.tipo_conta LIKE '%remun%' AND bq.DEBT_DEBT_TYPE_ID != 442)
          )
      )
      OR TRUNC(sheet.monto_transferido) != TRUNC(bq.DEBT_PAID_AMOUNT) 
      OR (
          (sheet.tipo_conta LIKE '%remun%') 
          AND (bq.DEBT_STATUS_DETAIL NOT IN ('executed', 'partially_executed','awaiting_confirmation'))
          AND (bq.DEBT_DEBT_TYPE_ID = 442) 
      ) 
    )
    SELECT * FROM final
  `;
  
  const jobConfig = {
    configuration: { query: { query: sql, useLegacySql: false } }
  };

  console.log(">> Enviando Job para o BigQuery...");
  let job = BigQuery.Jobs.insert(jobConfig, PROJECT_ID);
  const jobId = job.jobReference.jobId;

  let jobStatus = BigQuery.Jobs.get(PROJECT_ID, jobId);
  while (jobStatus.status.state !== 'DONE') {
    Utilities.sleep(3000);
    jobStatus = BigQuery.Jobs.get(PROJECT_ID, jobId);
  }

  if (jobStatus.status.errorResult) {
    throw new Error(`Erro no BigQuery: ${jobStatus.status.errorResult.message}`);
  }

  const stats = jobStatus.statistics.query;
  const gbProcessed = (stats.totalBytesProcessed / (1024 * 1024 * 1024)).toFixed(2);
  console.log(`✅ Job Concluído. Dados lidos: ${gbProcessed} GB`);

  console.log(">> Baixando resultados...");
  let rows = [];
  let pageToken = null;
  do {
    const results = BigQuery.Jobs.getQueryResults(PROJECT_ID, jobId, { pageToken: pageToken });
    if (results.rows) rows = rows.concat(results.rows);
    pageToken = results.pageToken;
  } while (pageToken);
  
  console.log(`>> Total de divergências encontradas: ${rows.length}`);
  return rows;
}

/************************************************************
 * RAMIFICAÇÃO: Query com BT_MP_TRANSFER_ADMIN (só para IDs CRUCE_2)
 ************************************************************/
function executarQueryDeCruzamentoTransferAdmin(idsCruce2) {
  if (!idsCruce2 || idsCruce2.length === 0) return [];
  const inList = idsCruce2.map(id => "'" + String(id).replace(/'/g, "\\'") + "'").join(',');
  
  const sql = `
    WITH base_sheet AS (
      SELECT
        id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia AS id_deuda,
        CAST(REPLACE(CAST(monto_total AS STRING), ',', '.') AS FLOAT64) AS monto_transferido,
        LOWER(cul_es_el_tipo_de_cuenta) AS tipo_conta,
        TRIM(CAST(cbu_22_dgitos AS STRING)) AS cbu_informado,
        CAST(issue_en_salesforce AS STRING) AS issue_salesforce
      FROM \`ddme000426-gopr4nla6zo-furyid.STG.base_integridade\`
      WHERE CAST(id_de_deuda_indique_a_qu_id_de_deuda_corresponde_esta_transferencia AS STRING) IN (${inList})
    ),
    base_ta AS (
      SELECT
        CAST(CREATED_PAYMENT_ID AS STRING) AS CREATED_PAYMENT_ID,
        AMOUNT,
        STATUS_DETAIL
      FROM \`meli-bi-data.WHOWNER.BT_MP_TRANSFER_ADMIN\`
      WHERE CAST(CREATED_PAYMENT_ID AS STRING) IN (${inList})
    ),
    FINAL AS (
      SELECT
        sheet.id_deuda,
        CURRENT_TIMESTAMP() AS data_execucao,
        CASE
          WHEN ta.CREATED_PAYMENT_ID IS NULL THEN 'CRUCE_2_2'
          WHEN sheet.monto_transferido IS NULL THEN 'ERROR_DATA_SUJA'
          WHEN TRUNC(sheet.monto_transferido) > TRUNC(ta.AMOUNT) THEN 'CRUCE_1_2'
          WHEN TRUNC(sheet.monto_transferido) < TRUNC(ta.AMOUNT) THEN 'CRUCE_4_2'
          WHEN (sheet.tipo_conta LIKE '%remun%')
               AND (ta.STATUS_DETAIL IS NULL OR LOWER(TRIM(ta.STATUS_DETAIL)) NOT IN ('executed', 'partially_executed', 'awaiting_confirmation'))
               THEN 'CRUCE_3_2'
          ELSE 'OK'
        END AS status_cruce,
        sheet.monto_transferido,
        ta.AMOUNT AS valor_ta,
        (IFNULL(sheet.monto_transferido, 0) - IFNULL(ta.AMOUNT, 0)) AS diferenca,
        sheet.cbu_informado,
        sheet.issue_salesforce,
        sheet.tipo_conta
      FROM base_sheet sheet
      LEFT JOIN base_ta ta ON CAST(sheet.id_deuda AS STRING) = ta.CREATED_PAYMENT_ID
    )
    SELECT * FROM FINAL
  `;

  const jobConfig = {
    configuration: { query: { query: sql, useLegacySql: false } }
  };

  console.log(">> Enviando Job Transfer Admin...");
  let job = BigQuery.Jobs.insert(jobConfig, PROJECT_ID);
  const jobId = job.jobReference.jobId;

  let jobStatus = BigQuery.Jobs.get(PROJECT_ID, jobId);
  while (jobStatus.status.state !== 'DONE') {
    Utilities.sleep(3000);
    jobStatus = BigQuery.Jobs.get(PROJECT_ID, jobId);
  }

  if (jobStatus.status.errorResult) {
    throw new Error(`Erro BigQuery Transfer Admin: ${jobStatus.status.errorResult.message}`);
  }

  let rows = [];
  let pageToken = null;
  do {
    const results = BigQuery.Jobs.getQueryResults(PROJECT_ID, jobId, { pageToken: pageToken });
    if (results.rows) rows = rows.concat(results.rows);
    pageToken = results.pageToken;
  } while (pageToken);

  console.log(`>> Ramificação: ${rows.length} linhas retornadas.`);
  return rows;
}

/************************************************************
 * PASSO 3: DISTRIBUIÇÃO E RESULTADOS (CRUCE 1..7)
 ************************************************************/
function distribuirResultadosNaPlanilha(ss, rows) {
  let c1 = [], c2 = [], c3 = [], c4 = [], c5 = [], c6 = [], c7 = [];
  
  const dataFormatada = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");

  if (rows && rows.length > 0) {
    rows.forEach(r => {
      const id = r.f[0].v;
      if (id === null || id === "" || id === undefined) return; 

      const tipo = r.f[2].v;
      const valSheet = r.f[3].v ? Number(r.f[3].v) : 0; 
      const valBQ = r.f[4].v ? Number(r.f[4].v) : 0;     
      const diff = r.f[5].v ? Number(r.f[5].v) : 0;
      const cbuInvalido = r.f[6] ? r.f[6].v : "N/A";
      const issueSf = r.f[7] ? r.f[7].v : "N/A"; 
      const tipoContaSheet = r.f[8] ? r.f[8].v : "";
      const tipoContaBQ = r.f[9] ? r.f[9].v : "";

      const linhaPadrao = [id, dataFormatada];

      if (tipo === 'CRUCE_1') c1.push([id, dataFormatada, valSheet, valBQ, diff]);
      else if (tipo === 'CRUCE_2') c2.push(linhaPadrao);
      else if (tipo === 'CRUCE_3') c3.push(linhaPadrao);
      else if (tipo === 'CRUCE_4') c4.push(linhaPadrao);
      else if (tipo === 'CRUCE_5_TESTE_CBU') c5.push([id, dataFormatada, cbuInvalido]);
      else if (tipo === 'CRUCE_6_DUPLICADOS') c6.push([id, dataFormatada, issueSf, valSheet]);
      else if (tipo === 'CRUCE_7_DEBT_TYPE_INCORRETO') c7.push([id, dataFormatada, tipoContaSheet, tipoContaBQ]);
    });
  }

  const nomes = [
    "CRUCE_1_VALOR_MAIOR_QUE_RETIDO",
    "CRUCE_2_ERRO_ID_DEUDA",
    "CRUCE_3_ENLIGHTEN_NAO_EXECUTOU",
    "CRUCE_4_VALOR_MENOR_QUE_RETIDO",
    "CRUCE_5_TESTE_CBU",
    "CRUCE_6_DUPLICADOS",
    "CRUCE_7_DEBT_TYPE_INCORRETO"
  ];
  
  escreverAba(ss, nomes[0], c1, ["DEBT_ID", "Data Execução", "Vl. Planilha", "Vl. BigQuery", "Diferença"]);
  const headerPadrao = ["DEBT_ID", "Data Execução"];
  escreverAba(ss, nomes[1], c2, headerPadrao);
  escreverAba(ss, nomes[2], c3, headerPadrao);
  escreverAba(ss, nomes[3], c4, headerPadrao);
  escreverAba(ss, nomes[4], c5, ["DEBT_ID", "Data Execução", "CBU Inválido"]);
  escreverAba(ss, nomes[5], c6, ["DEBT_ID", "Data Execução", "Issue Salesforce", "Valor Duplicado"]);
  escreverAba(ss, nomes[6], c7, ["DEBT_ID", "Data Execução", "Tipo na Planilha", "Tipo no Banco (ID)"]);
  
  atualizarResumo(ss, c1.length, c2.length, c3.length, c4.length, c5.length, c6.length, c7.length, nomes);
}

/************************************************************
 * RAMIFICAÇÃO: Distribuição resultados _2 (Transfer Admin)
 ************************************************************/
function distribuirResultadosNaPlanilha_2(ss, rows) {
  let c1_2 = [], c2_2 = [], c3_2 = [], c4_2 = [];
  const dataFormatada = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy HH:mm:ss");

  if (rows && rows.length > 0) {
    rows.forEach(r => {
      const id = r.f[0].v;
      if (id === null || id === "" || id === undefined) return;
      const tipo = r.f[2].v;
      const valSheet = r.f[3].v ? Number(r.f[3].v) : 0;
      const valTA = r.f[4].v ? Number(r.f[4].v) : 0;
      const diff = r.f[5].v ? Number(r.f[5].v) : 0;
      const issueSf = r.f[7] ? r.f[7].v : "N/A";
      const tipoConta = r.f[8] ? r.f[8].v : "";
      const linhaPadrao = [id, dataFormatada];

      if (tipo === 'CRUCE_1_2') c1_2.push([id, dataFormatada, valSheet, valTA, diff]);
      else if (tipo === 'CRUCE_2_2') c2_2.push(linhaPadrao);
      else if (tipo === 'CRUCE_3_2') c3_2.push(linhaPadrao);
      else if (tipo === 'CRUCE_4_2') c4_2.push([id, dataFormatada, valSheet, valTA, diff]);
    });
  }

  const nomes_2 = [
    "CRUCE_1_2_VALOR_MAIOR_QUE_RETIDO",
    "CRUCE_2_2_ERRO_ID_DEUDA",
    "CRUCE_3_2_ENLIGHTEN_NAO_EXECUTOU",
    "CRUCE_4_2_VALOR_MENOR_QUE_RETIDO"
  ];
  escreverAba(ss, nomes_2[0], c1_2, ["DEBT_ID", "Data Execução", "Vl. Planilha", "Vl. Transfer Admin", "Diferença"]);
  escreverAba(ss, nomes_2[1], c2_2, ["DEBT_ID", "Data Execução"]);
  escreverAba(ss, nomes_2[2], c3_2, ["DEBT_ID", "Data Execução"]);
  escreverAba(ss, nomes_2[3], c4_2, ["DEBT_ID", "Data Execução", "Vl. Planilha", "Vl. Transfer Admin", "Diferença"]);
  atualizarResumo_2(ss, c1_2.length, c2_2.length, c3_2.length, c4_2.length, nomes_2);
}

function escreverAba(ss, nomeAba, dados, cabecalho) {
  let aba = ss.getSheetByName(nomeAba);
  if (!aba) aba = ss.insertSheet(nomeAba);
  aba.clear();
  aba.appendRow(cabecalho);
  if (dados.length > 0) {
    const numLinhas = dados.length;
    const numColunas = dados[0].length;
    aba.getRange(2, 1, numLinhas, numColunas).setValues(dados);
  } else {
    aba.appendRow(["Nenhum caso encontrado", ""]);
  }
}

function atualizarResumo(ss, q1, q2, q3, q4, q5, q6, q7, nomes) {
  let aba = ss.getSheetByName("RESUMO");
  if (!aba) aba = ss.insertSheet("RESUMO");
  aba.clear();
  const hoje = new Date();
  
  aba.appendRow(["CRUCE", "Quantidade", "Data Execução"]);
  aba.appendRow([nomes[0], q1, hoje]);
  aba.appendRow([nomes[1], q2, hoje]);
  aba.appendRow([nomes[2], q3, hoje]);
  aba.appendRow([nomes[3], q4, hoje]);
  aba.appendRow([nomes[4], q5, hoje]);
  aba.appendRow([nomes[5], q6, hoje]);
  aba.appendRow([nomes[6], q7, hoje]);
}

function atualizarResumo_2(ss, q1, q2, q3, q4, nomes) {
  let aba = ss.getSheetByName("RESUMO_2");
  if (!aba) aba = ss.insertSheet("RESUMO_2");
  aba.clear();
  const hoje = new Date();
  aba.appendRow(["CRUCE", "Quantidade", "Data Execução"]);
  aba.appendRow([nomes[0], q1, hoje]);
  aba.appendRow([nomes[1], q2, hoje]);
  aba.appendRow([nomes[2], q3, hoje]);
  aba.appendRow([nomes[3], q4, hoje]);
}
