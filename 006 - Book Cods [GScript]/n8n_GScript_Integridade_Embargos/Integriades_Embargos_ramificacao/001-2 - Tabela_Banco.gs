/************************************************************
 * CRIAÇÃO DE TABELAS EXTERNAS + VIEW DE TRATAMENTO
 * SCRIPT COMPLETO E CORRIGIDO (Correção de Reserved Keywords)
 ************************************************************/

/**
 * Função principal – cria tabelas externas (STG) e Views de tratamento.
 */
function criarTodasAsTabelasExternas() {
  Logger.log("==== INICIANDO CRIAÇÃO DE TABELAS E VIEWS ====");

  // 1. CONFIGURAÇÃO GERAL
  const projectId = "ddme000426-gopr4nla6zo-furyid"; // Seu Project ID
  const datasetId = "STG";                            // Seu Dataset

  // 2. CONFIGURAÇÃO DAS TABELAS
  const tabelas = [
    {
      nome: "base_integridade",
      id: "1hrKq2U9y7LuTZqiIpmizk4j72FTyweZcnZShawPDhgY", // ID da Planilha
      aba: "base de solicitações",                        // Nome da Aba
      cabecalho: "A1:R1",                                 // Onde estão os títulos (R1 para pegar até coluna R)
      // Colunas que devem virar FLOAT (número decimal) na View final
      colunasFloat: ["monto_total", "valor_liquido", "outra_coluna_valor"] 
    }
  ];

  const tabelasCriadas = [];

  tabelas.forEach(t => {
    try {
      Logger.log(`➡️ Processando: ${t.nome} ...`);

      // Define nomes: Tabela Externa (ext_) e View Final (nome limpo)
      const nomeTabelaExterna = `ext_${t.nome}`;
      const nomeViewFinal = t.nome;

      // PASSO A: Cria a Tabela Externa (Raw Data - Tudo String)
      // Retorna o array de colunas limpas
      const schema = createExternalTableFromSheet(
        projectId,
        datasetId,
        nomeTabelaExterna,
        t.id,
        t.aba,
        t.cabecalho
      );

      // PASSO B: Cria a View de Tratamento (Limpeza de vírgulas e tipagem)
      if (schema && schema.length > 0) {
        createCorrectedView(
          projectId, 
          datasetId, 
          nomeViewFinal, 
          nomeTabelaExterna, 
          schema, 
          t.colunasFloat || []
        );
      }

      tabelasCriadas.push(nomeViewFinal);
      Utilities.sleep(1000); // Pausa para evitar rate limit

    } catch (e) {
      Logger.log(`❌ Falha ao processar ${t.nome}: ${e.message}`);
    }
  });

  if (tabelasCriadas.length > 0) {
    Logger.log("✅ Finalizado. Views criadas e prontas para uso:");
    tabelasCriadas.forEach(n => Logger.log(" • " + n));
  } else {
    Logger.log("⚠️ Nenhuma tabela foi criada.");
  }

  Logger.log("==== FIM DO PROCESSO ====");
}

/************************************************************
 * Cria tabela externa no BigQuery a partir de uma planilha
 * RETORNA: Lista com os nomes das colunas sanitizadas
 ************************************************************/
function createExternalTableFromSheet(projectId, datasetId, baseTableName, spreadsheetId, sheetName, headerRange) {

  const externalTableName = `${projectId}.${datasetId}.${baseTableName}`;
  Logger.log(`   [ETAPA 1] Criando Tabela Externa: ${baseTableName}`);

  try {
    const ss = SpreadsheetApp.openById(spreadsheetId);
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) throw new Error(`Aba "${sheetName}" não encontrada.`);

    const headerRow = sheet.getRange(headerRange).getValues()[0];
    const spreadsheetUrl = ss.getUrl();
    const sheetGid = sheet.getSheetId();

    // Sanitização dos nomes das colunas
    const sanitizeColumnName = colName => {
      if (!colName) return 'coluna_vazia';
      let clean = colName.toString().replace(/[^a-zA-Z0-9\s_]/g, ''); // Remove chars especiais
      clean = clean.replace(/[\s_]+/g, '_'); // Espaço vira _
      clean = clean.replace(/^_+|_+$/g, ''); // Remove _ das pontas
      return clean.toLowerCase();
    };

    const cleanedHeader = headerRow.map(sanitizeColumnName);
    
    // Lógica para converter número da coluna em letra (ex: 1->A, 27->AA)
    const numToColLetter = num => {
      let temp, letter = '';
      while (num > 0) {
        temp = (num - 1) % 26;
        letter = String.fromCharCode(temp + 65) + letter;
        num = (num - temp - 1) / 26;
      }
      return letter;
    };

    const lastColumnLetter = numToColLetter(cleanedHeader.length);

    // CORREÇÃO: Adicionamos crases (`...`) ao redor do nome da coluna
    // Isso evita erro se a coluna se chamar "true", "order", "group", etc.
    const schemaDefinition = cleanedHeader
      .map(c => `\`${c}\` STRING`) 
      .join(',\n   ');

    const finalUri = `${spreadsheetUrl.split('/edit')[0]}/edit#gid=${sheetGid}`;

    const sqlCreateExternal = `
      CREATE OR REPLACE EXTERNAL TABLE \`${externalTableName}\` (
        ${schemaDefinition}
      )
      OPTIONS (
        format = 'GOOGLE_SHEETS',
        skip_leading_rows = 1,
        sheet_range = '${sheetName}!A2:${lastColumnLetter}',
        uris = ['${finalUri}']
      );
    `;

    runBigQueryJob(sqlCreateExternal, projectId);
    Logger.log(`   --> Tabela externa criada com sucesso.`);
    
    return cleanedHeader; // Retorna o schema para ser usado na View

  } catch (e) {
    throw new Error(e.message);
  }
}

/************************************************************
 * Cria uma VIEW que corrige vírgulas e tipos de dados
 ************************************************************/
function createCorrectedView(projectId, datasetId, viewName, sourceTableName, columns, floatColumns) {
  
  const fullViewName = `${projectId}.${datasetId}.${viewName}`;
  const fullSourceTable = `${projectId}.${datasetId}.${sourceTableName}`;
  
  Logger.log(`   [ETAPA 2] Criando View Tratada: ${viewName}`);

  // Tenta remover tabela existente (caso nome colida)
  try {
    const sqlDrop = `DROP TABLE IF EXISTS \`${fullViewName}\``;
    runBigQueryJob(sqlDrop, projectId);
  } catch (e) {
    // Ignora erro de drop se não existir
  }

  // Monta o SQL da View
  // CORREÇÃO: Adicionamos crases aqui também (`${col}`)
  const selectClause = columns.map(col => {
    // Se a coluna estiver na lista de floats, aplica o tratamento
    if (floatColumns.includes(col)) {
      // REPLACE de vírgula por ponto e SAFE_CAST
      return `SAFE_CAST(REPLACE(\`${col}\`, ',', '.') AS FLOAT64) AS \`${col}\``;
    } else {
      // Mantém string, mas com crases
      return `\`${col}\``;
    }
  }).join(',\n     ');

  const sqlCreateView = `
    CREATE OR REPLACE VIEW \`${fullViewName}\` AS
    SELECT
      ${selectClause}
    FROM \`${fullSourceTable}\`
  `;

  runBigQueryJob(sqlCreateView, projectId);
  Logger.log(`   --> View criada! Use: SELECT * FROM ${datasetId}.${viewName}`);
}

/************************************************************
 * Executa SQL no BigQuery
 ************************************************************/
function runBigQueryJob(sql, projectId) {
  const queryConfigObject = { query: sql, useLegacySql: false };
  let job = BigQuery.newJob();
  job.setConfiguration({ query: queryConfigObject });
  
  // Insere o Job
  let queryJob = BigQuery.Jobs.insert(job, projectId);
  const jobId = queryJob.getJobReference().getJobId();

  // Espera completar
  while (!queryJob.getStatus().getState().match(/DONE/)) {
    Utilities.sleep(1000);
    queryJob = BigQuery.Jobs.get(projectId, jobId);
  }

  // Verifica Erros
  if (queryJob.getStatus().getErrorResult()) {
    const err = queryJob.getStatus().getErrorResult();
    // Exibe a mensagem completa do erro para facilitar debug
    throw new Error(`BigQuery Erro: ${err.getMessage()}`);
  }
}
