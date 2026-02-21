/**
 * ORQUESTRADOR GERAL
 * Função responsável por executar a rotina completa sequencialmente.
 * Deve ser agendada no Trigger (Relógio) para rodar toda manhã.
 */
function executarRotinaDiaria() {
  const inicio = new Date();
  Logger.log("🏁 [INÍCIO] Começando a rotina diária de validação: " + inicio);

  try {
    // --- PASSO 1: Atualizar Estrutura do Banco (Script 001) ---
    Logger.log("\n⏳ [PASSO 1/3] Criando/Atualizando Tabelas Externas e Views...");
    criarTodasAsTabelasExternas(); 
    Logger.log("✅ [PASSO 1] Concluído com sucesso.");

    // --- PASSO 2: Processar Cruzamentos e Preencher Planilha (Script 002) ---
    // Inclui uma pequena pausa de segurança para o BigQuery propagar as Views criadas acima
    Utilities.sleep(2000); 
    
    Logger.log("\n⏳ [PASSO 2/3] Executando Query no BigQuery e escrevendo na Planilha...");
    processarCrucesNoBigQuery();
    Logger.log("✅ [PASSO 2] Concluído com sucesso.");

    // --- PASSO 3: Gerar Relatório e Enviar E-mail (Script 003) ---
    // Só chega aqui se o passo 2 não der erro
    Logger.log("\n⏳ [PASSO 3/3] Gerando anexo e enviando e-mail...");
    exportarRelatoriosCrucePorEmail();
    Logger.log("✅ [PASSO 3] E-mail enviado.");

  } catch (erro) {
    // Se der erro em QUALQUER etapa acima, o script cai aqui e avisa no log
    Logger.log("❌ ERRO CRÍTICO NA ROTINA: " + erro.toString());
    
    // Opcional: Você pode configurar para enviar um email de alerta para você se falhar
    MailApp.sendEmail(
      "seu.email@mercadolivre.com", 
      "ALERTA: Falha na Rotina de Cruces", 
      "A rotina falhou com o seguinte erro:\n\n" + erro.toString()
    );
  }

  const fim = new Date();
  const tempoTotal = (fim - inicio) / 1000;
  Logger.log(`\n🏁 [FIM] Rotina finalizada em ${tempoTotal} segundos.`);
}