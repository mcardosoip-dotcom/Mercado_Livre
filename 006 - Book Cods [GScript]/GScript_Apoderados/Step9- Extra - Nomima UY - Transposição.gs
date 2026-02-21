/**
 * FASE 2: Transfere o intervalo A2:C<fim> da aba 'Resultado' (do arquivo atual)
 * para a célula C6 da aba 'URU - Todas las soc.' (no arquivo de origem).
 * O objetivo é colar os valores do PROCV concluído de volta no arquivo de origem.
 */
function transferirResultadoParaOrigem() {
  // --- CONFIGURAÇÕES DE TRANSFERÊNCIA ---
  
  // ARQUIVO DE ORIGEM (Onde os dados serão COLADOS)
  const ID_DESTINO_PASTE = "1T6cBl4TRzHy2ZDFxvuaKhOnMIwtW6x17LYoBGHccojE";
  const NOME_ABA_DESTINO_PASTE = "URU - Todas las soc.";
  const CELULA_INICIO_DESTINO = "C6"; // Célula de início da colagem
  
  // ARQUIVO DE ORIGEM DOS DADOS (Onde os dados serão COPIADOS - Arquivo atual)
  const ID_ORIGEM_COPIA = "15xxGjUdYiEIYf07a1o3mT120tg0vc_cud0jeKH0xMJk";
  const NOME_ABA_ORIGEM_COPIA = "Resultado";
  const COLUNA_INICIO_COPIA = 1; // Coluna A
  const COLUNA_FIM_COPIA = 3; // Coluna C
  const LINHA_INICIO_COPIA = 2; // Linha 2
  // ------------------------------------

  let ui = null;
  try {
    ui = SpreadsheetApp.getUi();
  } catch (e) {
    Logger.log("Aviso: Não foi possível obter a interface do usuário.");
  }

  try {
    // --- PASSO 1: COPIAR DADOS DO ARQUIVO DE TRABALHO (Resultado!A2:C<fim>) ---
    
    const ssOrigemCopia = SpreadsheetApp.openById(ID_ORIGEM_COPIA);
    const sheetOrigemCopia = ssOrigemCopia.getSheetByName(NOME_ABA_ORIGEM_COPIA);
    if (!sheetOrigemCopia) {
      throw new Error(`[ERRO COPIA] Aba de origem "${NOME_ABA_ORIGEM_COPIA}" não encontrada no arquivo atual.`);
    }

    const ultimaLinha = sheetOrigemCopia.getLastRow();
    
    if (ultimaLinha < LINHA_INICIO_COPIA) {
        if (ui) ui.alert("Atenção", "A aba Resultado não tem dados para copiar (além do cabeçalho).", ui.ButtonSet.OK);
        return;
    }
    
    const numLinhas = ultimaLinha - LINHA_INICIO_COPIA + 1;
    const numColunas = COLUNA_FIM_COPIA - COLUNA_INICIO_COPIA + 1;

    // Obtém os valores do intervalo A2:C<ultima linha>
    const dadosACopiar = sheetOrigemCopia.getRange(LINHA_INICIO_COPIA, COLUNA_INICIO_COPIA, numLinhas, numColunas).getValues();
    Logger.log(`Copiados ${dadosACopiar.length} linhas de dados do intervalo ${NOME_ABA_ORIGEM_COPIA}!A2:C.`);

    // --- PASSO 2: COLAR DADOS NO ARQUIVO DE DESTINO (URU - Todas las soc.!C6) ---

    // Abre o arquivo de destino (Arquivo Original)
    const ssDestinoPaste = SpreadsheetApp.openById(ID_DESTINO_PASTE);
    if (!ssDestinoPaste) {
        throw new Error(`[ERRO PASTE] Não foi possível abrir o arquivo de destino (ID: ${ID_DESTINO_PASTE}). Verifique as permissões.`);
    }

    const sheetDestinoPaste = ssDestinoPaste.getSheetByName(NOME_ABA_DESTINO_PASTE);
    if (!sheetDestinoPaste) {
      throw new Error(`[ERRO PASTE] Aba de destino "${NOME_ABA_DESTINO_PASTE}" não encontrada no arquivo de destino.`);
    }

    // Calcula o intervalo de colagem
    const celulaDestino = sheetDestinoPaste.getRange(CELULA_INICIO_DESTINO);
    const linhaDestino = celulaDestino.getRow(); // 6
    const colunaDestino = celulaDestino.getColumn(); // 3 (C)

    // Cola os valores na planilha de destino, começando em C6
    sheetDestinoPaste.getRange(linhaDestino, colunaDestino, dadosACopiar.length, dadosACopiar[0].length).setValues(dadosACopiar);
    
    Logger.log(`Colados ${dadosACopiar.length} linhas de dados como valores em ${NOME_ABA_DESTINO_PASTE}!C6.`);
    
    if (ui) ui.alert("Sucesso!", "A transferência dos dados (A:C) da aba Resultado para a aba 'URU - Todas las soc.' (C6) foi concluída.", ui.ButtonSet.OK);

  } catch (e) {
    Logger.log("ERRO FATAL NA TRANSFERÊNCIA: " + e.toString());
    if (ui) {
        ui.alert("Ocorreu um erro durante a transferência de dados. Verifique o log e as permissões de acesso ao arquivo de destino.", e.message, ui.ButtonSet.OK);
    }
  }
}