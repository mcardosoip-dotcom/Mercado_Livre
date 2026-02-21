/************************************************************
 * CRIAÇÃO DE TABELA EXTERNA NO BIGQUERY (GOOGLE SHEETS)
 * SEM EXECUÇÃO DE JOB / SEM SQL
 ************************************************************/

function criarTabelaExterna() {

  const projectId = "ddme000426-gopr4nla6zo-furyid";
  const datasetId = "STG";

  const config = {
    tableName: "ext_base_integridade",
    spreadsheetId: "1hrKq2U9y7LuTZqiIpmizk4j72FTyweZcnZShawPDhgY",
    sheetName: "base de solicitações",
    headerRange: "A1:R1"
  };

  criarTabelaExternaFromSheet(
    projectId,
    datasetId,
    config.tableName,
    config.spreadsheetId,
    config.sheetName,
    config.headerRange
  );
}

/************************************************************
 * Cria tabela externa diretamente via BigQuery.Tables.insert
 ************************************************************/
function criarTabelaExternaFromSheet(
  projectId,
  datasetId,
  tableName,
  spreadsheetId,
  sheetName,
  headerRange
) {

  Logger.log(`Criando tabela externa ${tableName}`);

  const ss = SpreadsheetApp.openById(spreadsheetId);
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    throw new Error(`Aba "${sheetName}" não encontrada`);
  }

  const headerRow = sheet.getRange(headerRange).getValues()[0];
  const spreadsheetUrl = ss.getUrl();
  const sheetGid = sheet.getSheetId();

  const sanitizeColumnName = col => {
    if (!col) return "coluna_vazia";
    return col
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-zA-Z0-9_ ]/g, "")
      .replace(/[\s_]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .toLowerCase();
  };

  const schemaFields = headerRow.map(col => ({
    name: sanitizeColumnName(col),
    type: "STRING"
  }));

  const tableResource = {
    tableReference: {
      projectId: projectId,
      datasetId: datasetId,
      tableId: tableName
    },
    externalDataConfiguration: {
      sourceFormat: "GOOGLE_SHEETS",
      autodetect: false,
      schema: {
        fields: schemaFields
      },
      sourceUris: [
        `${spreadsheetUrl.split("/edit")[0]}/edit#gid=${sheetGid}`
      ],
      googleSheetsOptions: {
        skipLeadingRows: 1,
        range: `${sheetName}!A2`
      }
    }
  };

  BigQuery.Tables.insert(
    tableResource,
    projectId,
    datasetId
  );

  Logger.log("Tabela externa criada com sucesso");
}
