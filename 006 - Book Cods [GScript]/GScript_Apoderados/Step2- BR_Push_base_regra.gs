function copiarRegrasSemTranspor() {
  // =============================================================
  // === CONFIGURAÇÕES ===========================================
  // =============================================================
  const ID_ORIGEM = '1L1wFbtA3MKvV4FrnGXTSDH3RhMYm3y4yYB2d-sLrzD4';
  const ID_DESTINO = '1EohsmWblwSVujLowqe1025y4Y3T6sgvs-V6NtPIuRIU';
  const NOME_ABA = 'Regras';

  // =============================================================
  // === ACESSA PLANILHAS ========================================
  // =============================================================
  const planilhaOrigem = SpreadsheetApp.openById(ID_ORIGEM);
  const abaOrigem = planilhaOrigem.getSheetByName(NOME_ABA);
  const planilhaDestino = SpreadsheetApp.openById(ID_DESTINO);
  const abaDestino = planilhaDestino.getSheetByName(NOME_ABA);

  // =============================================================
  // === COLETA DADOS DE A:E (SEM O CABEÇALHO) ==================
  // =============================================================
  const ultimaLinha = abaOrigem.getLastRow();
  if (ultimaLinha < 2) {
    Logger.log("⚠️ Nenhum dado encontrado na planilha de origem.");
    return;
  }

  const dados = abaOrigem.getRange(2, 1, ultimaLinha - 1, 5).getValues(); // Linhas 2→fim, colunas A:E

  // =============================================================
  // === LIMPA ABA DE DESTINO A PARTIR DA LINHA 2 ================
  // =============================================================
  const ultimaLinhaDestino = abaDestino.getLastRow();
  if (ultimaLinhaDestino > 1) {
    abaDestino.getRange(2, 1, ultimaLinhaDestino - 1, abaDestino.getLastColumn()).clearContent();
  }

  // =============================================================
  // === COLA OS DADOS COPIADOS ==================================
  // =============================================================
  abaDestino.getRange(2, 1, dados.length, dados[0].length).setValues(dados);

  Logger.log(`✅ ${dados.length} linhas copiadas da planilha de origem para a de destino.`);
}
