/**
 * ORQUESTRADOR GERAL
 * Função responsável por executar a rotina completa sequencialmente.
 * Deve ser agendada no Trigger (Relógio) para rodar toda manhã.
 * RAMIFICAÇÃO: usa 001/002/003 desta pasta (com cruces _2 via Transfer Admin).
 */
function executarRotinaDiaria() {
  const inicio = new Date();
  Logger.log("[INÍCIO] Começando a rotina diária de validação: " + inicio);

  try {
    Logger.log("\n[PASSO 1/3] Criando/Atualizando Tabelas Externas e Views...");
    criarTodasAsTabelasExternas(); 
    Logger.log("[PASSO 1] Concluído com sucesso.");

    Utilities.sleep(2000); 
    
    Logger.log("\n[PASSO 2/3] Executando Query no BigQuery e escrevendo na Planilha...");
    processarCrucesNoBigQuery();
    Logger.log("[PASSO 2] Concluído com sucesso.");

    Logger.log("\n[PASSO 3/3] Gerando anexo e enviando e-mail...");
    exportarRelatoriosCrucePorEmail();
    Logger.log("[PASSO 3] E-mail enviado.");

  } catch (erro) {
    Logger.log("ERRO CRÍTICO NA ROTINA: " + erro.toString());
    
    MailApp.sendEmail(
      "seu.email@mercadolivre.com", 
      "ALERTA: Falha na Rotina de Cruces", 
      "A rotina falhou com o seguinte erro:\n\n" + erro.toString()
    );
  }

  const fim = new Date();
  const tempoTotal = (fim - inicio) / 1000;
  Logger.log("\n[FIM] Rotina finalizada em " + tempoTotal + " segundos.");
}