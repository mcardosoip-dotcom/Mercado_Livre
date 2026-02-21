/**
 * Copia dados da aba "Demandas" da planilha de origem para "Database_Source_1" na planilha de destino.
 * Formata colunas F e G como data DD/MM/YYYY e adiciona coluna SLA (diferença em dias entre G e F).
 */

const SOURCE_SPREADSHEET_ID = '1Lp275wUQBmu6eAMRsFfk_2F-91S-EwZDHcDhEH2m7K0';
const DEST_SPREADSHEET_ID = '1mI37yyu7cXCok-oPgjTFF8CeSEWTfLNrpLTXEmH8ybo';
const SOURCE_SHEET_NAME = 'Demandas';
const DEST_SHEET_NAME = 'Database_Source_1';

function copiarDemandas() {
  const ssOrigem = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
  const ssDestino = SpreadsheetApp.openById(DEST_SPREADSHEET_ID);

  const abaOrigem = ssOrigem.getSheetByName(SOURCE_SHEET_NAME);
  if (!abaOrigem) {
    throw new Error('Aba "' + SOURCE_SHEET_NAME + '" não encontrada na planilha de origem.');
  }

  let abaDestino = ssDestino.getSheetByName(DEST_SHEET_NAME);
  if (!abaDestino) {
    abaDestino = ssDestino.insertSheet(DEST_SHEET_NAME);
  }

  // Limpar a base de destino antes de colar os novos dados
  abaDestino.clear();

  const dadosBrutos = abaOrigem.getDataRange().getValues();
  if (!dadosBrutos.length) {
    return;
  }

  // Desconsiderar a primeira linha em branco da origem
  const dados = dadosBrutos[0].every(function (c) { return c === '' || c === null; })
    ? dadosBrutos.slice(1)
    : dadosBrutos;

  const numRows = dados.length;

  // Garantir que há espaço para a coluna SLA (coluna H = índice 7)
  const colSLA = 7;
  let dadosParaColar = dados.map(function (row) {
    var newRow = row.slice();
    while (newRow.length <= colSLA) {
      newRow.push('');
    }
    return newRow;
  });

  // Cabeçalho da coluna SLA na primeira linha (linha 1 = cabeçalho no destino)
  if (dadosParaColar[0].length > colSLA) {
    dadosParaColar[0][colSLA] = 'SLA';
  }

  abaDestino.getRange(1, 1, dadosParaColar.length, dadosParaColar[0].length).setValues(dadosParaColar);

  // Formatar colunas F e G como DD/MM/YYYY
  abaDestino.getRange(1, 6, numRows, 6).setNumberFormat('dd/mm/yyyy'); // F
  abaDestino.getRange(1, 7, numRows, 7).setNumberFormat('dd/mm/yyyy'); // G

  // SLA: calcula diretamente no código para evitar erros de fórmula; valores negativos ficam como 0
  if (numRows > 1) {
    var valoresSLA = [];
    for (var r = 1; r < numRows; r++) {
      var rowData = dadosParaColar[r]; // dados da linha (índice 0 = cabeçalho, índice 1 = primeira linha de dados)
      var dataF = rowData[5]; // coluna F (índice 5)
      var dataG = rowData[6]; // coluna G (índice 6)
      
      try {
        // No Google Sheets, datas podem vir como Date ou como número serial
        var dateF = dataF instanceof Date ? dataF : (dataF ? new Date(dataF) : null);
        var dateG = dataG instanceof Date ? dataG : (dataG ? new Date(dataG) : null);
        
        if (dateF && dateG && !isNaN(dateF.getTime()) && !isNaN(dateG.getTime())) {
          var diferenca = Math.floor((dateG - dateF) / (1000 * 60 * 60 * 24)); // diferença em dias
          valoresSLA.push([Math.max(0, diferenca)]); // valores negativos viram 0
        } else {
          valoresSLA.push(['']);
        }
      } catch (e) {
        valoresSLA.push(['']);
      }
    }
    var numLinhasSLA = valoresSLA.length;
    if (numLinhasSLA > 0) {
      abaDestino.getRange(2, 8, numLinhasSLA, 1).setValues(valoresSLA);
      abaDestino.getRange(2, 8, numLinhasSLA, 1).setNumberFormat('0'); // inteiro (dias)
    }
  }

  Logger.log('Cópia concluída: ' + numRows + ' linhas para "' + DEST_SHEET_NAME + '".');
}
