function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Painel de Processos - Embargos');
}

/**
 * Executa a função correspondente à etapa selecionada no menu.
 */
function executarProcesso(etapa) {
  try {
    switch (etapa) {
      case '001':
         // PASSO 2: Executa a query logo em seguida
        executarQueryPOC();
        
        // PASSO 1: Executa a cópia da planilha
        copiarDadosDaPlanilhaExterna();
       
        
        return "✅ Processo 001 - Cópia de dados e Query POC executados com sucesso!";

      case '002':
        runPdfGenerator();
        return "✅ Processo 002 - Exportação para Excel concluída!";

      case '003':
        listarPdfsDeMultiplasPastasNaPlanilhaExterna();
        return "✅ Processo 003 - Listagem de PDFs concluída!";

      case '004':
        enviarPdfsPorIssueEMail_notif_Externo();
        return "✅ Processo 004 - Envio de e-mails concluído!";

      case '005':
        copyAndClearEmbargarAndSetHeader();
        return "✅ Processo 005 - Limpeza e Definição de Header concluída!";

      default:
        return "❌ Etapa não reconhecida.";
    }
  } catch (e) {
    // Captura erros em qualquer uma das etapas
    return `❌ Erro ao executar o processo ${etapa}: ${e.message}`;
  }
}