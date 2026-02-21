// URL da planilha - usando ID direto
const SPREADSHEET_ID = '1vmynDnT4DfzuSGxxjbL8zdBMsqla7PT9MPahhR102UI';
const SHEET_NAME = 'Database';

/**
 * Abre a página web
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Marketplace RPA - Processos')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Função de teste - execute esta função manualmente para testar a conexão
 */
function testConnection() {
  try {
    Logger.log("=== TESTE DE CONEXÃO ===");
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    Logger.log("✓ Planilha aberta com sucesso");
    Logger.log("Nome da planilha: " + ss.getName());
    
    const sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      Logger.log("✗ Aba 'Database' não encontrada!");
      Logger.log("Abas disponíveis: " + ss.getSheets().map(s => s.getName()).join(", "));
      return;
    }
    Logger.log("✓ Aba 'Database' encontrada");
    
    const data = sheet.getDataRange().getValues();
    Logger.log("✓ Dados obtidos: " + data.length + " linhas");
    Logger.log("Cabeçalhos: " + data[0].join(" | "));
    Logger.log("Primeira linha de dados: " + data[1].join(" | "));
    Logger.log("=== TESTE CONCLUÍDO COM SUCESSO ===");
  } catch (error) {
    Logger.log("✗ ERRO: " + error.toString());
    Logger.log("Stack: " + error.stack);
  }
}

/**
 * Busca todos os dados da planilha
 */
function getData() {
  try {
    Logger.log("Iniciando busca de dados...");
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error('Aba "Database" não encontrada. Abas disponíveis: ' + 
        ss.getSheets().map(s => s.getName()).join(", "));
    }
    
    const data = sheet.getDataRange().getValues();
    Logger.log("Dados brutos obtidos: " + data.length + " linhas");
    
    if (data.length === 0) {
      return [];
    }
    
    const headers = data[0];
    Logger.log("Cabeçalhos: " + headers.join(" | "));
    
    const rows = data.slice(1);
    
    // Colunas: A=RPA, B=Data Início, C=TT Recebido, D=TT processado, E=Lista_Email, F=Solicitante, G=Status, H=Data Fim
    const processes = rows.map((row, index) => {
      // Pula linhas completamente vazias
      if (!row[0] || row[0].toString().trim() === '') {
        return null;
      }
      
      const recebido = Number(row[2]) || 0;
      const processado = Number(row[3]) || 0;
      const progress = recebido > 0 ? Math.round((processado / recebido) * 100) : 0;
      
      return {
        RPA: row[0] ? row[0].toString() : '',
        'Data Início': row[1] ? formatDateValue(row[1]) : '',
        'TT Recebido': recebido,
        'TT processado': processado,
        Lista_Email: row[4] ? row[4].toString() : '',
        Solicitante: row[5] ? row[5].toString() : '',
        Status: row[6] ? row[6].toString() : '',
        'Data Fim': row[7] ? formatDateValue(row[7]) : '',
        progress: progress
      };
    }).filter(item => item !== null); // Remove linhas nulas
    
    Logger.log("Processos processados: " + processes.length);
    return processes;
  } catch (error) {
    Logger.log("Erro ao buscar dados: " + error.toString());
    Logger.log("Stack: " + error.stack);
    throw new Error('Erro ao buscar dados: ' + error.toString());
  }
}

/**
 * Formata valor de data
 */
function formatDateValue(value) {
  if (!value) return '';
  
  // Se já é uma string, retorna
  if (typeof value === 'string') {
    return value;
  }
  
  // Se é um objeto Date
  if (value instanceof Date) {
    return Utilities.formatDate(value, Session.getScriptTimeZone(), 'dd/MM/yyyy');
  }
  
  return value.toString();
}

/**
 * Busca processos com filtros
 */
function searchProcesses(searchTerm, statusFilter) {
  try {
    Logger.log("Buscando com filtros - Termo: " + searchTerm + ", Status: " + statusFilter);
    let processes = getData();
    
    // Filtro por termo de busca
    if (searchTerm && searchTerm.trim() !== '') {
      const term = searchTerm.toLowerCase();
      processes = processes.filter(p => {
        return (p.RPA && p.RPA.toLowerCase().includes(term)) ||
               (p.Solicitante && p.Solicitante.toLowerCase().includes(term)) ||
               (p.Lista_Email && p.Lista_Email.toLowerCase().includes(term));
      });
    }
    
    // Filtro por status
    if (statusFilter && statusFilter !== 'all') {
      processes = processes.filter(p => p.Status === statusFilter);
    }
    
    Logger.log("Processos filtrados: " + processes.length);
    return processes;
  } catch (error) {
    Logger.log("Erro ao buscar processos: " + error.toString());
    throw new Error('Erro ao buscar processos: ' + error.toString());
  }
}

/**
 * Retorna lista única de status
 */
function getUniqueStatuses() {
  try {
    const processes = getData();
    const statuses = [...new Set(processes.map(p => p.Status).filter(s => s && s.trim() !== ''))];
    return statuses.sort();
  } catch (error) {
    Logger.log("Erro ao buscar status: " + error.toString());
    return [];
  }
}
