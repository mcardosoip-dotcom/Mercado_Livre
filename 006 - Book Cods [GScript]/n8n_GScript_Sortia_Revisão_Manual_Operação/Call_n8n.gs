// --- ESTRUTURA PARA WEB APP ---
function doPost(e) {
  return handleRequest(e);
}

function doGet(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  try {
    main(e);
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "ok",
        message: "Processo executado com sucesso"
      }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "error",
        message: err.message
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// --- FUNÇÃO PRINCIPAL (RODE ESTA) ---
function main(e) {
  const ss = SpreadsheetApp.openById('16ty2m0fFDI20aSw4H0N3dkxKay2rX7_ew9L-RZvwFrM');
  
  // 1. Faz o cruzamento e escreve os dados
  cruzarDados(ss);
  
  // 2. IMPORTANTE: Força o Google a salvar os dados escritos antes de tentar formatar
  SpreadsheetApp.flush();
  
  // 3. Formata a coluna O em negrito
  formatarColunaO(ss);
  
  // 4. Configura a coluna P na aba Cruzamento
  configurarColunaStatus(ss);
}

// --- PARTE 1: CRUZAMENTO ---
function cruzarDados(ss) {
  if (!ss) ss = SpreadsheetApp.openById('16ty2m0fFDI20aSw4H0N3dkxKay2rX7_ew9L-RZvwFrM');

  const sheetManual = ss.getSheetByName('DataBase_Rev_Manual');
  const sheetMachine = ss.getSheetByName('DataBase_Machine');
  let sheetCruzamento = ss.getSheetByName('Cruzamento');

  if (!sheetManual || !sheetMachine) throw new Error('Abas de origem não encontradas.');
  if (!sheetCruzamento) sheetCruzamento = ss.insertSheet('Cruzamento');

  const dadosManual = sheetManual.getDataRange().getValues();
  const dadosMachine = sheetMachine.getDataRange().getValues();

  // Cabeçalho da Machine (Coluna I)
  const cabecalhoColunaI = (dadosMachine.length > 0 && dadosMachine[0].length > 8) ? dadosMachine[0][8] : "Info_Machine";

  // Mapeamento
  let mapaMachine = {};
  for (let i = 1; i < dadosMachine.length; i++) {
    let linha = dadosMachine[i];
    if (linha.length < 9) continue;
    let chave = linha[7]; 
    let valor = linha[8]; 
    let chaveTratada = (chave === null || chave === undefined) ? "" : String(chave).trim().toUpperCase();
    if (chaveTratada !== "") mapaMachine[chaveTratada] = valor;
  }

  // Cruzamento
  let resultadoFinal = [];
  for (let i = 0; i < dadosManual.length; i++) {
    let linhaManual = dadosManual[i];
    if (i === 0) {
      resultadoFinal.push([...linhaManual, cabecalhoColunaI]);
      continue;
    }
    let chaveManual = linhaManual[2];
    let chaveTratada = (chaveManual === null || chaveManual === undefined) ? "" : String(chaveManual).trim().toUpperCase();
    let valorEncontrado = mapaMachine.hasOwnProperty(chaveTratada) ? mapaMachine[chaveTratada] : "";
    resultadoFinal.push([...linhaManual, valorEncontrado]);
  }

  // Conjunto de Issues já concluídos (coluna C da aba DataBase_Concluídos)
  let concluidosSet = {};
  const sheetConcluidos = ss.getSheetByName('DataBase_Concluídos');
  if (sheetConcluidos && sheetConcluidos.getLastRow() >= 2) {
    const colCConcluidos = sheetConcluidos.getRange(2, 3, sheetConcluidos.getLastRow(), 3).getValues();
    for (let r = 0; r < colCConcluidos.length; r++) {
      let val = colCConcluidos[r][0];
      let valTratado = (val === null || val === undefined) ? "" : String(val).trim().toUpperCase();
      if (valTratado !== "") concluidosSet[valTratado] = true;
    }
  }

  // Filtrar apenas casos com "REVISION_MANUAL" na coluna O (índice 14)
  // e que NÃO estejam na DataBase_Concluídos (coluna C)
  let resultadoFiltrado = [];
  for (let i = 0; i < resultadoFinal.length; i++) {
    let linha = resultadoFinal[i];
    // Mantém o cabeçalho (linha 0)
    if (i === 0) {
      resultadoFiltrado.push([...linha, ""]);
      continue;
    }
    // Só inclui se coluna O = "REVISION_MANUAL"
    if (linha.length <= 14 || String(linha[14]).trim().toUpperCase() !== "REVISION_MANUAL") continue;
    // Exclui se o Issue (coluna C) já estiver em DataBase_Concluídos
    let issueC = (linha[2] === null || linha[2] === undefined) ? "" : String(linha[2]).trim().toUpperCase();
    if (concluidosSet[issueC]) continue;
    // Adiciona coluna P vazia (será preenchida pela função configurarColunaStatus)
    resultadoFiltrado.push([...linha, ""]);
  }

  // Escrita
  sheetCruzamento.clear();
  if (resultadoFiltrado.length > 0) {
    sheetCruzamento.getRange(1, 1, resultadoFiltrado.length, resultadoFiltrado[0].length).setValues(resultadoFiltrado);
  }
}

// --- PARTE 2: FORMATAÇÃO DA COLUNA O EM NEGRITO ---
function formatarColunaO(ss) {
  if (!ss) ss = SpreadsheetApp.openById('16ty2m0fFDI20aSw4H0N3dkxKay2rX7_ew9L-RZvwFrM');

  const sheetName = 'Cruzamento';
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) return;

  // DEFINIÇÃO DA COLUNA O
  const colunaO = 15; // A=1 ... O=15
  
  // Pega a última linha com dados REAIS
  const ultimaLinha = sheet.getLastRow();

  // Aplica negrito em toda a coluna O (incluindo cabeçalho)
  if (ultimaLinha > 0) {
    const rangeColunaO = sheet.getRange(1, colunaO, ultimaLinha);
    rangeColunaO.setFontWeight('bold');
  }
}

// --- PARTE 3: STATUS NA COLUNA P DA ABA CRUZAMENTO ---
function configurarColunaStatus(ss) {
  if (!ss) ss = SpreadsheetApp.openById('16ty2m0fFDI20aSw4H0N3dkxKay2rX7_ew9L-RZvwFrM');

  const sheetName = 'Cruzamento';
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) return;

  // DEFINIÇÃO DA COLUNA P
  const colunaStatus = 16; // A=1 ... P=16
  
  // Pega a última linha com dados REAIS
  const ultimaLinha = sheet.getLastRow();

  // 1. Define o Cabeçalho na linha 1
  sheet.getRange(1, colunaStatus).setValue('Status').setFontWeight('bold');

  // 2. Aplica Validação e Cor (da linha 2 até a última)
  if (ultimaLinha > 1) {
    const rangeDados = sheet.getRange(2, colunaStatus, ultimaLinha - 1);
    
    // Define valor padrão "Não concluído"
    rangeDados.setValue('Não concluído');
    
    // Cria o Dropdown
    const regraValidacao = SpreadsheetApp.newDataValidation()
      .requireValueInList(['Não concluído', 'Concluído'], true)
      .setAllowInvalid(false)
      .build();

    rangeDados.setDataValidation(regraValidacao);
    rangeDados.setBackground('#FFF2CC'); // Fundo Amarelo Claro
  }
  
  // Ajusta a largura para caber o texto
  sheet.autoResizeColumn(colunaStatus);
}