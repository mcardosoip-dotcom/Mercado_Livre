/**
 * Copia as linhas da aba 'EMBARGAR' com status "Enviado" (coluna Y)
 * para a aba 'E_mails_enviados', preservando o cabeçalho.
 * @description Versão standalone (sem vínculo direto à planilha)
 */
function copyAndClearEmbargarAndSetHeader() {
  // === CONFIGURAÇÕES ===
  const LINK_PLANILHA_PRINCIPAL = 'https://docs.google.com/spreadsheets/d/1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI/edit';
  const PLANILHA_ID = extrairIdDaUrl(LINK_PLANILHA_PRINCIPAL);
  const NOME_ABA_ORIGEM = 'EMBARGAR';
  const NOME_ABA_DESTINO = 'E_mails_enviados';
  const STATUS_COL_INDEX = 24; // Coluna Y (índice 0)

  const inicio = new Date();

  try {
    if (!PLANILHA_ID) throw new Error('Não foi possível extrair o ID da planilha. Verifique o link.');
    Logger.log('🔗 Acessando planilha principal...');
    const planilha = SpreadsheetApp.openById(PLANILHA_ID);

    const abaOrigem = planilha.getSheetByName(NOME_ABA_ORIGEM);
    const abaDestino = planilha.getSheetByName(NOME_ABA_DESTINO);

    if (!abaOrigem) throw new Error(`A aba '${NOME_ABA_ORIGEM}' não foi encontrada.`);
    if (!abaDestino) throw new Error(`A aba '${NOME_ABA_DESTINO}' não foi encontrada.`);

    Logger.log(`📄 Lendo dados da aba '${NOME_ABA_ORIGEM}'...`);
    const dados = abaOrigem.getDataRange().getValues();
    const rowsToCopy = [];

    if (dados.length === 0) {
      Browser.msgBox('Aviso', 'A aba "EMBARGAR" está vazia. Nenhuma linha foi copiada.', Browser.Buttons.OK);
      return;
    }

    // Adiciona o cabeçalho (linha 0)
    rowsToCopy.push(dados[0]);

    // Filtra linhas com status "enviado" (coluna Y)
    for (let i = 1; i < dados.length; i++) {
      const row = dados[i];
      const status = row[STATUS_COL_INDEX] ? row[STATUS_COL_INDEX].toString().trim().toLowerCase() : '';
      if (status === 'enviado') rowsToCopy.push(row);
    }

    // Se tiver pelo menos uma linha além do cabeçalho
    if (rowsToCopy.length > 1) {
      const lastRow = abaDestino.getLastRow();
      const targetRow = lastRow > 0 ? lastRow + 1 : 1;

      abaDestino
        .getRange(targetRow, 1, rowsToCopy.length, rowsToCopy[0].length)
        .setValues(rowsToCopy);

      const copiedCount = rowsToCopy.length - 1;
      const fim = new Date();
      const duracao = ((fim - inicio) / 1000).toFixed(2);

      const msg = `✅ ${copiedCount} linha(s) copiadas com sucesso para '${NOME_ABA_DESTINO}'.\nA aba '${NOME_ABA_ORIGEM}' foi mantida inalterada.\n\n⏱️ Tempo total: ${duracao}s`;
      Logger.log(msg);
     
    } else {
      Logger.log('ℹ️ Nenhuma linha com status "Enviado" encontrada.');
    }

  } catch (e) {
    const erroMsg = `❌ Erro: ${e.message}`;
    Logger.log(erroMsg);
    throw new Error(erroMsg);
  }
}

/**
 * Extrai o ID de uma URL de planilha Google Sheets.
 * @param {string} url - Link da planilha
 * @returns {string|null} - ID da planilha
 */
function extrairIdDaUrl(url) {
  const match = url.match(/\/spreadsheets\/d\/([a-zA-Z0-9_-]+)/);
  return match ? match[1] : null;
}
