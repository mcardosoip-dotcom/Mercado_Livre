

// // Permite ser acionado via Webhook (pelo N8N)
// function doGet(e) {
//   try {
//     Logger.log("🌐 [WEBHOOK] Acionamento recebido via HTTP/N8N.");
//     executarRotinaOrquestrada();
//     return ContentService.createTextOutput("Sucesso: Rotina executada completa.");
//   } catch (error) {
//     return ContentService.createTextOutput("Erro: " + error.message);
//   }
// }

// // Função principal (pode ser agendada no Relógio/Trigger se não usar N8N)
// function executarRotinaOrquestrada() {
//   const inicio = new Date();
//   console.log("🏁 [ORQUESTRADOR] Iniciando rotina: " + inicio);

//   try {
//     // --- PASSO 1: Sincronização de Dados (Antigo script 002) ---
//     // O script 001 original foi removido pois o N8N já preparou a tabela.
//     console.log("👉 [1/2] Iniciando Processamento de Dados (BQ -> Sheets)...");
    
//     // Chama a função principal do arquivo 001_Processamento.gs
//     processarCrucesNoBigQuery(); 
    
//     console.log("✅ [1/2] Dados atualizados na planilha com sucesso.");

//     // --- PASSO 2: Notificação (Antigo script 003) ---
//     console.log("👉 [2/2] Gerando Relatório e Enviando E-mail...");
    
//     // Chama a função principal do arquivo 002_Notificacao.gs
//     exportarRelatoriosCrucePorEmail();
    
//     console.log("✅ [2/2] E-mail disparado.");

//   } catch (erro) {
//     console.error("❌ ERRO FATAL NO ORQUESTRADOR: " + erro.toString());
    
//     // Envia alerta de falha técnica para o admin (opcional)
//     MailApp.sendEmail(
//       "murillo.franca@mercadolivre.com", // Coloque seu email aqui
//       "🚨 FALHA: Rotina de Cruces", 
//       "O orquestrador parou devido ao erro:\n\n" + erro.toString()
//     );
//     throw erro; // Relança o erro para o N8N saber que falhou
//   }

//   const fim = new Date();
//   const tempoTotal = ((fim - inicio) / 1000).toFixed(2);
//   console.log(`🏁 [FIM] Rotina finalizada em ${tempoTotal} segundos.`);
// }