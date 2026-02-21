function executarQueryPOC() {
  // =================================================================
  // CONFIGURAÇÃO JÁ PREENCHIDA COM SEU PROJETO
  // =================================================================
  const projectId = 'meli-bi-data'; 
  
  const spreadsheetUrl = 'https://docs.google.com/spreadsheets/d/1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI/edit';
  const sheetName = 'Query_Suporte_Resultado';

  // --- QUERY ---
  const sql = `
    SELECT
      d.DEBT_ID                AS DEB_DEBT_ID,
      d.DEBT_USER_ID           AS DEB_DEBT_USER_ID,
      d.DEBT_TOTAL_AMOUNT      AS DEB_DEBT_TOTAL_AMOUNT,
      d.DEBT_PAID_AMOUNT       AS DEB_DEBT_PAID_AMOUNT,
      d.DEBT_STATUS            AS DEB_DEBT_STATUS,
      d.DEBT_CURRENCY_ID       AS DEB_DEBT_CURRENCY_ID,
      d.DEBT_SITE_ID           AS DEB_DEBT_SITE_ID,
      d.DEBT_CREATED_AT        AS DEB_DEBT_CREATED_AT,
      COUNT(d.DEBT_USER_ID) OVER (
          PARTITION BY d.DEBT_USER_ID
      ) AS qtd_embargos_usuario
    FROM
      \`meli-bi-data.WHOWNER.BT_MP_DISB_DEBT\` d
    WHERE
      d.DEBT_DEBT_TYPE_ID IN (77, 437, 442, 459)
      AND DATE(d.DEBT_CREATED_AT) >= DATE_SUB(CURRENT_DATE(), INTERVAL 20 DAY)
    ORDER BY
      DEB_DEBT_CREATED_AT DESC
  `;

  try {
    Logger.log('Iniciando conexão com BigQuery via projeto: ' + projectId);

    const request = {
      query: sql,
      useLegacySql: false
    };

    // Executa a query
    let queryResults = BigQuery.Jobs.query(request, projectId);
    const jobId = queryResults.jobReference.jobId;

    // Paginação (garante que traga todos os dados)
    let rows = [];
    let pageToken = null;

    do {
      if (pageToken) {
        queryResults = BigQuery.Jobs.getQueryResults(projectId, jobId, {
          pageToken: pageToken
        });
      }

      if (queryResults.rows) {
        const currentRows = queryResults.rows.map(row => {
          return row.f.map(cell => cell.v);
        });
        rows = rows.concat(currentRows);
      }
      pageToken = queryResults.pageToken;
    } while (pageToken);

    if (rows.length === 0) {
      Logger.log('A query rodou com sucesso, mas o resultado veio vazio.');
      return;
    }

    // Escreve na Planilha
    const headers = queryResults.schema.fields.map(field => field.name);
    const ss = SpreadsheetApp.openByUrl(spreadsheetUrl);
    const sheet = ss.getSheetByName(sheetName);

    if (!sheet) {
      throw new Error(`A aba "${sheetName}" não foi encontrada na planilha.`);
    }

    sheet.clear();
    const finalData = [headers, ...rows];
    sheet.getRange(1, 1, finalData.length, finalData[0].length).setValues(finalData);

    Logger.log(`✅ SUCESSO! ${rows.length} linhas importadas na aba '${sheetName}'.`);

  } catch (e) {
    Logger.log('❌ ERRO: ' + e.message);
    
    // Dica caso dê erro de permissão no meli-bi-data
    if (e.message.includes("Access Denied")) {
      Logger.log("DICA: Parece que você não tem permissão para RODAR queries usando o projeto 'meli-bi-data' como pagador.");
      Logger.log("Tente descobrir se sua equipe tem um projeto próprio (ex: legal-analytics) e troque na linha 5.");
    }
  }
}