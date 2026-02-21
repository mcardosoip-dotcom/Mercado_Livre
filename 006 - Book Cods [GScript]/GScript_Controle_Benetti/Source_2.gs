/**
 * Lê a aba "Controle" (source) da planilha de destino, extrai data, hora e participantes
 * de cada reunião (colunas Date e Resumo) e grava na aba "Database_Source_2" para análise
 * de carga de reuniões do time.
 * Usa DEST_SPREADSHEET_ID definido em Source_1.gs (mesmo projeto).
 */

const CONTROLE_SHEET_NAME = 'Controle';
const INPUT_CONTROLE_SHEET_NAME = 'Database_Source_2';
const TIME_SHIPPING_SHEET_NAME = 'TimeShipping';
const TZ = 'America/Sao_Paulo';
/** Formato padrão da data na aba Database_Source_2: DD/MM/YYYY */
const DATE_FORMAT = 'dd/MM/yyyy';

/**
 * Remove emojis/caracteres indesejados do texto (ex: 📝).
 * @param {string} s
 * @return {string}
 */
function cleanText(s) {
  if (s == null || s === undefined) return '';
  return String(s).replace(/\uD83D\uDCDD/g, '').trim(); // 📝
}

/**
 * Retorna o índice da coluna pelo nome do cabeçalho (case-insensitive, trim).
 * @param {Array.<string>} headers - Primeira linha da planilha
 * @param {string} name - Nome da coluna (ex: 'Date', 'Resumo')
 * @return {number} Índice 0-based ou -1 se não encontrado
 */
function getColumnIndex(headers, name) {
  if (!headers || !headers.length) {
    return -1;
  }
  var n = (name || '').toString().trim().toLowerCase();
  for (var i = 0; i < headers.length; i++) {
    if (String(headers[i] || '').trim().toLowerCase() === n) {
      return i;
    }
  }
  return -1;
}

/**
 * Extrai data e hora de um valor Date (ISO ou objeto Date).
 * @param {*} cellValue - Valor da célula (string ISO ou Date)
 * @return {{data: string, hora: string}}
 */
function parseDateCell(cellValue) {
  var data = '';
  var hora = '';
  if (cellValue === null || cellValue === undefined || cellValue === '') {
    return { data: data, hora: hora };
  }
  try {
    var d = cellValue instanceof Date ? cellValue : new Date(cellValue);
    if (isNaN(d.getTime())) {
      return { data: data, hora: hora };
    }
    data = Utilities.formatDate(d, TZ, DATE_FORMAT);
    hora = Utilities.formatDate(d, TZ, 'HH:mm');
  } catch (e) {
    // mantém vazio
  }
  return { data: data, hora: hora };
}

/**
 * Extrai a lista de participantes do texto do Resumo (bloco PARTICIPANTES: até próximo bloco ou fim).
 * Nomes separados por vírgula; retorna array de nomes (um por linha na saída).
 * @param {string} resumo - Texto da coluna Resumo
 * @return {Array.<string>} Lista de nomes de participantes
 */
function extractParticipantesList(resumo) {
  if (!resumo || typeof resumo !== 'string') {
    return [];
  }
  var idx = resumo.indexOf('PARTICIPANTES:');
  if (idx === -1) {
    idx = resumo.indexOf('PARTICIPANTES :');
  }
  if (idx === -1) {
    return [];
  }
  var start = idx + 'PARTICIPANTES:'.length;
  var rest = resumo.substring(start);
  var nextLabels = ['SÍNTESE:', 'DECISÕES:', 'AÇÕES:'];
  var segmentEnd = rest.length;
  for (var i = 0; i < nextLabels.length; i++) {
    var pos = rest.indexOf(nextLabels[i]);
    if (pos !== -1 && pos < segmentEnd) {
      segmentEnd = pos;
    }
  }
  var segment = rest.substring(0, segmentEnd).trim();
  if (!segment) {
    return [];
  }
  return segment.split(',').map(function (s) {
    return cleanText(s);
  }).filter(function (s) {
    return s.length > 0;
  });
}

/**
 * Carrega o conjunto de nomes da aba TimeShipping.
 * Usa a primeira coluna (A); ignora a primeira linha (cabeçalho). Match case-insensitive + trim.
 * @param {Spreadsheet} ss - Planilha
 * @return {Object} Objeto com chaves normalizadas (trim + lowercase) para lookup rápido
 */
function loadTimeShippingNames(ss) {
  var set = {};
  var aba = ss.getSheetByName(TIME_SHIPPING_SHEET_NAME);
  if (!aba) {
    Logger.log('Aba "' + TIME_SHIPPING_SHEET_NAME + '" não encontrada; coluna TimeShipping ficará vazia.');
    return set;
  }
  var range = aba.getDataRange();
  if (!range) return set;
  var values = range.getValues();
  // Coluna A (índice 0); se houver mais de uma linha, considera linha 0 como cabeçalho
  var startRow = values.length > 1 ? 1 : 0;
  for (var i = startRow; i < values.length; i++) {
    var name = String((values[i][0] !== undefined && values[i][0] !== null) ? values[i][0] : '').trim();
    if (name.length > 0) set[name.toLowerCase()] = true;
  }
  Logger.log('TimeShipping: ' + Object.keys(set).length + ' nomes carregados da coluna A.');
  return set;
}

/**
 * Popula a aba "Database_Source_2" a partir da aba "Controle" (source).
 * Colunas de saída: Data da reunião, Hora da reunião, Participantes, TimeShipping, Subject, fileId.
 */
function popularInputControle() {
  var ss = SpreadsheetApp.openById(DEST_SPREADSHEET_ID);

  var abaControle = ss.getSheetByName(CONTROLE_SHEET_NAME) || ss.getSheetByName('Controle (source)');
  if (!abaControle) {
    throw new Error('Aba "' + CONTROLE_SHEET_NAME + '" (ou "Controle (source)") não encontrada.');
  }

  var abaInput = ss.getSheetByName(INPUT_CONTROLE_SHEET_NAME);
  if (!abaInput) {
    abaInput = ss.insertSheet(INPUT_CONTROLE_SHEET_NAME);
  } else {
    // Limpa completamente a aba antes de inserir novos dados
    // Primeiro limpa o conteúdo e formatação de todo o range de dados existente
    var existingRange = abaInput.getDataRange();
    if (existingRange && existingRange.getNumRows() > 0) {
      existingRange.clearContent();
      existingRange.clearFormat();
    }
    // Garante que toda a aba esteja limpa (incluindo células fora do range de dados)
    abaInput.clear();
    Logger.log('Aba "' + INPUT_CONTROLE_SHEET_NAME + '" limpa antes de inserir novos dados.');
  }

  var timeShippingSet = loadTimeShippingNames(ss);

  var range = abaControle.getDataRange();
  var dados = range ? range.getValues() : [];
  if (!dados.length || !dados[0]) {
    Logger.log('Aba Controle sem dados ou sem cabeçalho.');
    return;
  }

  var headers = dados[0].map(function (c) {
    return String(c || '');
  });
  var idxFileId = getColumnIndex(headers, 'fileId');
  var idxSubject = getColumnIndex(headers, 'Subject');
  var idxDate = getColumnIndex(headers, 'Date');
  var idxResumo = getColumnIndex(headers, 'Resumo');

  if (idxDate === -1 || idxResumo === -1) {
    throw new Error('Colunas "Date" e "Resumo" são obrigatórias na aba Controle. Cabeçalhos encontrados: ' + headers.join(', '));
  }

  var outHeaders = ['Data da reunião', 'Hora da reunião', 'Participantes', 'TimeShipping', 'Subject', 'fileId'];
  var outRows = [outHeaders];
  // Set para rastrear combinações únicas e evitar duplicatas
  var uniqueKeys = {};

  for (var r = 1; r < dados.length; r++) {
    var row = dados[r];
    var dateVal = row[idxDate];
    var resumoVal = row[idxResumo];
    var parsed = parseDateCell(dateVal);
    var participantesList = extractParticipantesList(resumoVal);
    var subject = cleanText(idxSubject >= 0 ? row[idxSubject] : '');
    var fileId = idxFileId >= 0 ? (row[idxFileId] || '') : '';
    if (participantesList.length === 0) {
      // Cria chave única: Data + Hora + Participante (vazio) + Subject + fileId
      var keyEmpty = [parsed.data, parsed.hora, '', subject, fileId].join('|').toLowerCase();
      if (!uniqueKeys[keyEmpty]) {
        uniqueKeys[keyEmpty] = true;
        outRows.push([parsed.data, parsed.hora, '', 'NÃO', subject, fileId]);
      }
    } else {
      for (var p = 0; p < participantesList.length; p++) {
        var participante = participantesList[p];
        // Cria chave única: Data + Hora + Participante + Subject + fileId
        var key = [parsed.data, parsed.hora, participante.trim().toLowerCase(), subject, fileId].join('|').toLowerCase();
        if (!uniqueKeys[key]) {
          uniqueKeys[key] = true;
          var isTimeShipping = timeShippingSet[participante.trim().toLowerCase()] ? 'SIM' : 'NÃO';
          outRows.push([
            parsed.data,
            parsed.hora,
            participante,
            isTimeShipping,
            subject,
            fileId
          ]);
        }
      }
    }
  }

  var numRows = outRows.length;
  var numCols = outHeaders.length;
  if (numRows > 1) {
    abaInput.getRange(1, 1, numRows, numCols).setValues(outRows);
    abaInput.getRange(1, 1, 1, numCols).setFontWeight('bold');
    // Padronizar coluna Data da reunião (A) como DD/MM/YYYY
    abaInput.getRange(2, 1, numRows, 1).setNumberFormat('dd/mm/yyyy');
  }

  var totalUnique = Object.keys(uniqueKeys).length;
  Logger.log('Database_Source_2 atualizado: ' + (numRows - 1) + ' linhas únicas (duplicatas removidas).');
}
