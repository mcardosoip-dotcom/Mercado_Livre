/**
 * GScript Legal Search - Consulta LK_PBD_LA_ENTRADAS_E_DESFECHOS
 * Planilha: lista de valores na coluna definida → Menu Processar → Diálogo (campo + colunas) → OK → Resultado em nova aba
 *
 * OBRIGATÓRIO: Ative o serviço BigQuery no projeto.
 * No editor do Apps Script: Extensões > Serviços do Apps Script > adicione "BigQuery API" e ative.
 */

const PROJECT_ID = 'pdme000426-c1s7scatwm0-furyid';
const DATASET_TABLE = 'STG.LK_PBD_LA_ENTRADAS_E_DESFECHOS';
const TABLE_FULL = '`' + PROJECT_ID + '.' + DATASET_TABLE + '`';

// Planilha: usar ID se script rodar fora da planilha; senão usa planilha ativa
const SPREADSHEET_ID = '1OgcNC-OKSRdvISJwpUYQlDhYCmCgAnyfny83jC95_dI';
const LIST_COLUMN = 1;   // A = 1
const LIST_START_ROW = 2;
const LIST_MAX_ROWS = 2000;
const RESULT_SHEET_NAME = 'Resultado';
const QUERY_LIMIT = 50000;

/**
 * Cria o menu ao abrir a planilha
 */
function onOpen() {
  try {
    SpreadsheetApp.getUi()
      .createMenu('Consulta BigQuery')
      .addItem('Processar', 'abrirDialogoProcessar')
      .addToUi();
  } catch (e) {
    Logger.log('onOpen: ' + e.message);
  }
}

/**
 * Função manual para criar o menu (útil para testes)
 */
function criarMenu() {
  onOpen();
}

/**
 * Para uso como Web App (código fora da planilha, acesso por URL).
 * Implantar como "Aplicativo da Web" e acessar a URL gerada.
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Legal Analytics - Search')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Retorna os nomes das colunas da tabela BigQuery (para combobox e checkboxes)
 */
function getColumnNames() {
  if (typeof BigQuery === 'undefined') {
    throw new Error(
      'Serviço BigQuery não ativo. No editor do script: Extensões > Serviços do Apps Script > adicione "BigQuery API" e ative.'
    );
  }
  const sql = `
    SELECT column_name
    FROM \`${PROJECT_ID}.STG.INFORMATION_SCHEMA.COLUMNS\`
    WHERE table_name = 'LK_PBD_LA_ENTRADAS_E_DESFECHOS'
    ORDER BY ordinal_position
  `;
  const request = { query: sql, useLegacySql: false };
  let queryResults = BigQuery.Jobs.query(request, PROJECT_ID);
  const jobId = queryResults.jobReference.jobId;
  const rows = [];
  let pageToken = null;
  do {
    if (pageToken) {
      queryResults = BigQuery.Jobs.getQueryResults(PROJECT_ID, jobId, { pageToken: pageToken });
    }
    if (queryResults.rows) {
      queryResults.rows.forEach(function (row) {
        rows.push(row.f[0].v);
      });
    }
    pageToken = queryResults.pageToken;
  } while (pageToken);
  return rows;
}

/**
 * Lê a lista de valores da planilha (coluna A a partir da linha definida)
 */
function getListFromSheet() {
  const ss = SPREADSHEET_ID
    ? SpreadsheetApp.openById(SPREADSHEET_ID)
    : SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  const range = sheet.getRange(LIST_START_ROW, LIST_COLUMN, LIST_START_ROW + LIST_MAX_ROWS - 1, LIST_COLUMN);
  const values = range.getValues();
  const list = [];
  for (let i = 0; i < values.length; i++) {
    const v = values[i][0];
    if (v !== null && v !== undefined && String(v).trim() !== '') {
      list.push(String(v).trim());
    }
  }
  return list;
}

/**
 * Valida se a lista da planilha não está vazia e abre o diálogo
 */
function abrirDialogoProcessar() {
  const list = getListFromSheet();
  if (!list || list.length === 0) {
    SpreadsheetApp.getUi().alert('Lista vazia', 'Coloque os valores na coluna A (a partir da linha ' + LIST_START_ROW + ') e tente novamente.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  const html = HtmlService.createHtmlOutputFromFile('Index')
    .setWidth(500)
    .setHeight(600)
    .setTitle('Legal Analytics - Search');
  // Título que aparece na barra da janela (troque aqui se ainda vir "Processar consulta")
  SpreadsheetApp.getUi().showModalDialog(html, 'Legal Analytics - Search');
}

/**
 * Executa a consulta: lê lista, monta SQL, executa BigQuery, escreve em Resultado.
 * Chamado pelo diálogo ao clicar OK.
 * @param {string} fieldName - Nome da coluna para filtrar (WHERE campo IN (...))
 * @param {string[]} selectedColumns - Nomes das colunas para retornar (SELECT)
 * @returns {{ success: boolean, message: string, rowCount?: number }}
 */
function executarConsulta(fieldName, selectedColumns) {
  try {
    if (!fieldName || !selectedColumns || selectedColumns.length === 0) {
      return { success: false, message: 'Selecione o campo da consulta e pelo menos uma coluna para retornar.' };
    }

    const validColumns = getColumnNames();
    if (validColumns.indexOf(fieldName) === -1) {
      return { success: false, message: 'Campo de filtro inválido: ' + fieldName };
    }
    for (let i = 0; i < selectedColumns.length; i++) {
      if (validColumns.indexOf(selectedColumns[i]) === -1) {
        return { success: false, message: 'Coluna inválida: ' + selectedColumns[i] };
      }
    }

    const list = getListFromSheet();
    if (!list || list.length === 0) {
      return { success: false, message: 'A lista da planilha está vazia. Preencha a coluna A e tente novamente.' };
    }

    // Campo de pesquisa sempre vem no resultado; evita duplicata na lista de colunas
    const colsParaSelect = selectedColumns.slice();
    if (colsParaSelect.indexOf(fieldName) === -1) {
      colsParaSelect.unshift(fieldName);
    }

    const sql = buildSql(fieldName, colsParaSelect, list);
    const queryResult = runQuery(sql);
    const headers = queryResult.headers;
    const rows = queryResult.rows;
    const previewRows = rows.slice(0, 10);
    const csvContent = buildCsvContent(headers, rows);

    return {
      success: true,
      message: 'Consulta concluída. ' + rows.length + ' linha(s). Visualize o preview e baixe o CSV.',
      rowCount: rows.length,
      headers: headers,
      previewRows: previewRows,
      csvContent: csvContent
    };
  } catch (e) {
    Logger.log('executarConsulta: ' + e.message);
    return { success: false, message: 'Erro: ' + e.message };
  }
}

/**
 * Monta o SQL: SELECT colunas FROM tabela WHERE campo IN (valores) LIMIT
 */
function buildSql(fieldName, selectedColumns, listValues) {
  const selectList = selectedColumns.map(function (col) {
    return '`' + col + '`';
  }).join(', ');
  const escaped = listValues.map(function (v) {
    return "'" + String(v).replace(/\\/g, '\\\\').replace(/'/g, "''") + "'";
  });
  const inList = escaped.join(', ');
  return [
    'SELECT ' + selectList,
    'FROM ' + TABLE_FULL,
    'WHERE CAST(`' + fieldName + '` AS STRING) IN (' + inList + ')',
    'LIMIT ' + QUERY_LIMIT
  ].join('\n');
}

/**
 * Executa a query no BigQuery e retorna { headers, rows }
 */
function runQuery(sql) {
  const request = { query: sql, useLegacySql: false };
  let queryResults = BigQuery.Jobs.query(request, PROJECT_ID);
  const jobId = queryResults.jobReference.jobId;
  let rows = [];
  let pageToken = null;

  do {
    if (pageToken) {
      queryResults = BigQuery.Jobs.getQueryResults(PROJECT_ID, jobId, { pageToken: pageToken });
    }
    if (queryResults.rows) {
      const currentRows = queryResults.rows.map(function (row) {
        return row.f.map(function (cell) {
          return cell.v !== null && cell.v !== undefined ? cell.v : '';
        });
      });
      rows = rows.concat(currentRows);
    }
    pageToken = queryResults.pageToken;
  } while (pageToken);

  const headers = queryResults.schema && queryResults.schema.fields
    ? queryResults.schema.fields.map(function (f) { return f.name; })
    : [];
  return { headers: headers, rows: rows };
}

/**
 * Gera o conteúdo CSV (UTF-8 com BOM para Excel reconhecer acentos).
 * Escapa aspas e quebras de linha nos valores.
 */
function buildCsvContent(headers, rows) {
  function escapeCsvCell(val) {
    const s = String(val === null || val === undefined ? '' : val);
    if (s.indexOf('"') !== -1 || s.indexOf('\n') !== -1 || s.indexOf('\r') !== -1 || s.indexOf(',') !== -1) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  }
  const lines = [];
  lines.push(headers.map(escapeCsvCell).join(','));
  rows.forEach(function (row) {
    lines.push(row.map(escapeCsvCell).join(','));
  });
  const BOM = '\uFEFF';
  return BOM + lines.join('\r\n');
}
