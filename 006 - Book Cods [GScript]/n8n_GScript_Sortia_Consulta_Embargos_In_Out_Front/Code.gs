// Configurações do BigQuery
const PROJECT_ID = 'ddme000426-gopr4nla6zo-furyid';
const DATASET_ID = 'STG';
const TABLE_ID = 'Sortia_Embargos_InOut_FE';

// Campos disponíveis para busca (apenas DEBT_USER_ID visível; descomente os demais se necessário)
const SEARCH_FIELDS = [
  // 'amount',
  // 'case_file',
  // 'court',
  // 'cover_sheet',
  // 'debt_id',
  // 'Expediente',
  // 'Juzgado',
  // 'Caratula',
  // 'debt_id_disp',
  'DEBT_USER_ID',
  // 'DEBT_SITE_ID',
  // 'DEBT_CURRENCY_ID',
  // 'DEBT_DEBT_TYPE_ID',
  // 'DEBT_CREATED_AT',
  // 'DEBT_TOTAL_AMOUNT',
  // 'DEBT_PAID_AMOUNT',
  // 'DEBT_STATUS',
  // 'DEBT_DESCRIPTION'
];

/**
 * Cria o menu customizado ao abrir a planilha
 * Nota: Esta função só pode ser executada quando a planilha é aberta, não durante testes manuais
 */
function onOpen() {
  try {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('BigQuery')
      .addItem('Buscar Dados', 'showSearchDialog')
      .addItem('Limpar Resultados', 'clearResults')
      .addToUi();
  } catch (error) {
    console.log('onOpen será executado automaticamente ao abrir a planilha');
  }
}

/**
 * Função manual para criar o menu (útil para testes)
 */
function criarMenu() {
  onOpen();
}

/**
 * Exibe o diálogo de busca
 */
function showSearchDialog() {
  const html = HtmlService.createHtmlOutputFromFile('Interface')
    .setWidth(400)
    .setHeight(250)
    .setTitle('Buscar no BigQuery');
  SpreadsheetApp.getUi().showModalDialog(html, 'Buscar Dados');
}

/**
 * Serve a página web quando acessada via URL
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Busca BigQuery - Sortia Embargos')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Retorna os campos disponíveis para busca
 */
function getSearchFields() {
  return SEARCH_FIELDS;
}

/**
 * Executa a busca no BigQuery e retorna os resultados
 */
function searchBigQuery(field, value) {
  try {
    // Validação do campo
    if (!SEARCH_FIELDS.includes(field)) {
      throw new Error('Campo inválido selecionado');
    }
    
    // Construir a query SQL com CAST para STRING
    const query = `
      SELECT *
      FROM \`${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`
      WHERE CAST(${field} AS STRING) LIKE '%${value}%'
      LIMIT 1000
    `;
    
    // Executar a query
    const request = {
      query: query,
      useLegacySql: false
    };
    
    const queryResults = BigQuery.Jobs.query(request, PROJECT_ID);
    
    // Verificar se há resultados
    if (!queryResults.rows || queryResults.rows.length === 0) {
      return {
        success: true,
        count: 0,
        message: 'Nenhum resultado encontrado',
        headers: [],
        rows: []
      };
    }
    
    // Processar resultados
    const headers = queryResults.schema.fields.map(field => field.name);
    const rows = queryResults.rows.map(row => {
      return row.f.map(cell => cell.v || '');
    });
    
    return {
      success: true,
      count: rows.length,
      message: `${rows.length} resultados encontrados`,
      headers: headers,
      rows: rows
    };
    
  } catch (error) {
    console.error('Erro na busca:', error);
    return {
      success: false,
      message: `Erro ao buscar dados: ${error.message}`,
      headers: [],
      rows: []
    };
  }
}

/**
 * Limpa os resultados da planilha
 */
function clearResults() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();
  SpreadsheetApp.getUi().alert('Resultados limpos com sucesso!');
}
