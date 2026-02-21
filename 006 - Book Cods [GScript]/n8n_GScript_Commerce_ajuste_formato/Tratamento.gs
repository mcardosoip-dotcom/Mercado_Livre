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

function main(e) {
  formatarColunas();
}

function formatarColunas() {
  const spreadsheetId = '1BnKT25oRcYOg3UNechKi5v2WfciHzoJcDoGaGVZ5JnI';
  const ss = SpreadsheetApp.openById(spreadsheetId);
  const sheet = ss.getSheetByName('Database');

  if (!sheet) {
    Logger.log('Aba "Database" não encontrada!');
    return;
  }

  const lastRow = sheet.getLastRow();
  if (lastRow < 2) {
    Logger.log('Não há dados para formatar');
    return;
  }

  const dadosC = sheet.getRange(2, 3, lastRow - 1, 1).getValues();
  const dadosD = sheet.getRange(2, 4, lastRow - 1, 1).getValues();
  const dadosM = sheet.getRange(2, 13, lastRow - 1, 1).getValues();
  const dadosN = sheet.getRange(2, 14, lastRow - 1, 1).getValues();

  let contadorConversoes = 0;
  let contadorBrancos = 0;

  for (let i = 0; i < dadosC.length; i++) {
    const valorC = dadosC[i][0];

    if (valorC && typeof valorC === 'string' && valorC.indexOf('T') !== -1) {
      try {
        const dataHora = new Date(valorC);
        sheet.getRange(i + 2, 3).setValue(dataHora);

        if (dataHora.getHours() === 0 && dataHora.getMinutes() === 0) {
          sheet.getRange(i + 2, 4).clearContent();
          contadorBrancos++;
        } else {
          sheet.getRange(i + 2, 4).setValue(dataHora);
        }

        contadorConversoes++;
      } catch (e) {
        Logger.log('Erro ao converter linha ' + (i + 2) + ', coluna C: ' + e);
      }
    } else {
      const valorD = dadosD[i][0];
      if (valorD instanceof Date) {
        if (valorD.getHours() === 0 && valorD.getMinutes() === 0) {
          sheet.getRange(i + 2, 4).clearContent();
          contadorBrancos++;
        }
      }
    }
  }

  for (let i = 0; i < dadosM.length; i++) {
    const valorM = dadosM[i][0];

    if (valorM && typeof valorM === 'string' && valorM.indexOf('T') !== -1) {
      try {
        const dataHora = new Date(valorM);
        sheet.getRange(i + 2, 13).setValue(dataHora);

        if (dataHora.getHours() === 0 && dataHora.getMinutes() === 0) {
          sheet.getRange(i + 2, 14).clearContent();
          contadorBrancos++;
        } else {
          sheet.getRange(i + 2, 14).setValue(dataHora);
        }

        contadorConversoes++;
      } catch (e) {
        Logger.log('Erro ao converter linha ' + (i + 2) + ', coluna M: ' + e);
      }
    } else {
      const valorN = dadosN[i][0];
      if (valorN instanceof Date) {
        if (valorN.getHours() === 0 && valorN.getMinutes() === 0) {
          sheet.getRange(i + 2, 14).clearContent();
          contadorBrancos++;
        }
      }
    }
  }

  sheet.getRange(2, 3, lastRow - 1, 1).setNumberFormat('dd/MM/yyyy');
  sheet.getRange(2, 13, lastRow - 1, 1).setNumberFormat('dd/MM/yyyy');
  sheet.getRange(2, 4, lastRow - 1, 1).setNumberFormat('HH:mm');
  sheet.getRange(2, 14, lastRow - 1, 1).setNumberFormat('HH:mm');

  Logger.log('✓ Formatação concluída com sucesso!');
  Logger.log('Conversões ISO 8601 realizadas: ' + contadorConversoes);
  Logger.log('Campos de hora 00:00 deixados em branco: ' + contadorBrancos);
  Logger.log('Total de linhas processadas: ' + (lastRow - 1));
}
