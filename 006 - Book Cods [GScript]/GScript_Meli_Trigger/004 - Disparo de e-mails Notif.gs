/**
 * Função para buscar arquivos PDF com base no número da Issue em pastas do Drive 
 * e enviar por e-mail para o destinatário associado na planilha externa.
 * * ✅ Ajustes incluídos:
 * 1. Alias de envio (from: ALIAS_EMAIL_SAIDA) reativado.
 * 2. Todas as chamadas Browser.msgBox() substituídas por Logger.log() para execução via Trigger.
 */
function enviarPdfsPorIssueEMail_notif_Externo() {
  // === CONFIGURAÇÕES PRINCIPAIS ===
  // Planilha de origem (IDs de Planilhas e pastas são sensíveis a maiúsculas/minúsculas)
  const ID_PLANILHA_ORIGEM = "1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI"; // <-- Planilha externa
  const NOME_ABA_EMBARGOS = "EMBARGAR";
  
  // Índices das colunas (base 0)
  const COLUNA_ISSUE_INDEX = 16;  // Coluna Q (Issue)
  const COLUNA_EMAIL_INDEX = 10;  // Coluna K (E-mail)
  const COLUNA_STATUS_INDEX = 24; // Coluna Y (Status)
  
  const NOME_CABECALHO_STATUS = "Status_Email";
  const COLUNA_STATUS_NUMERO = COLUNA_STATUS_INDEX + 1; // Índice base 1 (para métodos de Range)

  // IDs das pastas do Drive onde os PDFs serão buscados
const PASTAS_DE_BUSCA_IDS = [
  "1oJzt3p1xczU_6TCgf_Ss6zSD_9DIFwo9", // SEM_SALDO
  "1pkdoMkXljhS0yEEi-CV8t4Ct_HJdnn_p", // COM_SALDO
  "1KO8G-sk5SFWPrdtbvyM5PeKem_up9IMh"  // NOVOS_GERADOS (nova pasta)
];

  // Configurações de E-mail
  const ASSUNTO_EMAIL_PADRAO = "Documento referente al proceso ";
  const CORPO_EMAIL_PADRAO = 
    `Estimados,
    
Tengo el agrado de dirigirme a Ustedes, a los efectos de brindar respuesta a uno de los requerimientos librado en relación al asunto de la referencia.

Adjunto en tal sentido, la respuesta al oficio en formato PDF.

Sin otro particular, los saludo cordialmente, quedando a disposición por cualquier aclaración que consideren necesaria.

Saludos.`;

  // ALIAS DE SAÍDA - DEVE SER UM ALIAS VÁLIDO DA CONTA EXECUTORA
  const ALIAS_EMAIL_SAIDA = "notificaciones@mercadolibre.com"; 

  let emailsEnviadosComSucesso = 0;
  let emailsNaoEnviados = 0;
  const issuesParaProcessar = {}; 
  const statusUpdates = []; 

  try {
    // === ABRE PLANILHA EXTERNA ===
    const planilha = SpreadsheetApp.openById(ID_PLANILHA_ORIGEM);
    const abaEmbargos = planilha.getSheetByName(NOME_ABA_EMBARGOS);

    if (!abaEmbargos) {
      // Usando Logger.log em vez de Browser.msgBox
      Logger.log(`ERRO CRÍTICO: A aba '${NOME_ABA_EMBARGOS}' não foi encontrada na planilha externa. Encerrando execução.`);
      return;
    }

    // Garante o cabeçalho de status na coluna Y
    const cabecalhoStatus = abaEmbargos.getRange(1, COLUNA_STATUS_NUMERO);
    if (cabecalhoStatus.getValue() !== NOME_CABECALHO_STATUS) {
      cabecalhoStatus.setValue(NOME_CABECALHO_STATUS);
      Logger.log(`Cabeçalho na coluna ${COLUNA_STATUS_NUMERO} (Y) definido como '${NOME_CABECALHO_STATUS}'.`);
    }

    // Lê todos os dados
    const dados = abaEmbargos.getDataRange().getValues();
    if (dados.length <= 1) {
      // Usando Logger.log em vez de Browser.msgBox
      Logger.log("AVISO: A aba 'EMBARGAR' está vazia ou contém apenas cabeçalhos. Encerrando execução.");
      return;
    }

    Logger.log(`Iniciando processamento de ${dados.length - 1} linhas na aba ${NOME_ABA_EMBARGOS}...`);

    // === 1. IDENTIFICAÇÃO DE ISSUES ÚNICOS ===
    for (let i = 1; i < dados.length; i++) {
      const row = dados[i];
      const issueNumber = row[COLUNA_ISSUE_INDEX] ? row[COLUNA_ISSUE_INDEX].toString().trim() : '';
      const email = row[COLUNA_EMAIL_INDEX] ? row[COLUNA_EMAIL_INDEX].toString().trim() : '';
      const rowNumber = i + 1;

      const statusAtual = row[COLUNA_STATUS_INDEX];

      if (statusAtual === "Enviado") {
        continue; 
      }

      if (!issueNumber || !email || !email.includes('@')) {
        statusUpdates.push({ row: rowNumber, col: COLUNA_STATUS_NUMERO, value: "Dados Incompletos" });
        continue;
      }

      if (!issuesParaProcessar[issueNumber]) {
        issuesParaProcessar[issueNumber] = { email: email, rowNumber: rowNumber };
      } else {
        statusUpdates.push({ row: rowNumber, col: COLUNA_STATUS_NUMERO, value: "Duplicidade de Issue" });
      }
    }

    const issuesUnicosCount = Object.keys(issuesParaProcessar).length;
    Logger.log(`Total de Issues únicos a processar: ${issuesUnicosCount}`);
    
    if (issuesUnicosCount === 0) {
        // Usando Logger.log em vez de Browser.msgBox
        Logger.log("AVISO: Não há novos Issues para processar ou todos já foram enviados. Encerrando execução.");
        return;
    }

    // === 2. ENVIO DE E-MAILS ===
    for (const issueNumber in issuesParaProcessar) {
      const { email, rowNumber } = issuesParaProcessar[issueNumber];
      const nomeArquivoPdf = `${issueNumber}.pdf`;

      let pdfBlob = null;
      for (const folderId of PASTAS_DE_BUSCA_IDS) {
        try {
          const pasta = DriveApp.getFolderById(folderId);
          const arquivos = pasta.getFilesByName(nomeArquivoPdf);
          if (arquivos.hasNext()) {
            pdfBlob = arquivos.next().getBlob();
            Logger.log(`✅ PDF '${nomeArquivoPdf}' encontrado na pasta ID: ${folderId}`);
            break;
          }
        } catch (e) {
          Logger.log(`⚠️ Erro ao acessar ou processar pasta '${folderId}': ${e.message}`);
        }
      }

      if (pdfBlob) {
        try {
          const assuntoFinal = ASSUNTO_EMAIL_PADRAO + issueNumber;
          
          GmailApp.sendEmail(email, assuntoFinal, CORPO_EMAIL_PADRAO, {
            htmlBody: CORPO_EMAIL_PADRAO.replace(/\n/g, '<br>'),
            attachments: [pdfBlob],
            from: ALIAS_EMAIL_SAIDA // Alias de saída
          });

          Logger.log(`✉️ Enviado para '${email}' com anexo '${nomeArquivoPdf}'. Linha: ${rowNumber}`);
          statusUpdates.push({ row: rowNumber, col: COLUNA_STATUS_NUMERO, value: "Enviado" });
          emailsEnviadosComSucesso++;
        } catch (e) {
          Logger.log(`❌ Erro ao enviar e-mail para '${email}': ${e.message}`);
          statusUpdates.push({ row: rowNumber, col: COLUNA_STATUS_NUMERO, value: "Erro no Envio" });
          emailsNaoEnviados++;
        }
      } else {
        Logger.log(`📁 PDF '${nomeArquivoPdf}' não encontrado para Issue '${issueNumber}'. Linha: ${rowNumber}`);
        statusUpdates.push({ row: rowNumber, col: COLUNA_STATUS_NUMERO, value: "PDF Não Encontrado" });
        emailsNaoEnviados++;
      }
    }

    // === 3. ATUALIZA STATUS NA PLANILHA ===
    statusUpdates.forEach(update => {
      abaEmbargos.getRange(update.row, update.col).setValue(update.value);
    });

    const resumo = `Processamento concluído!

✅ E-mails enviados: ${emailsEnviadosComSucesso}
⚠️ E-mails com falha/PDF ausente: ${emailsNaoEnviados}
Total de Issues únicos processados: ${issuesUnicosCount}

Verifique a coluna '${NOME_CABECALHO_STATUS}' para o resultado por linha.`;

    Logger.log("--- Fim do processamento ---");
    // Usando Logger.log para o resumo final
    Logger.log(`RESUMO DO ENVIO:\n${resumo}`);

  } catch (e) {
    // Tratamento de Erro Crítico
    Logger.log(`ERRO CRÍTICO no processo: ${e.message} - Linha: ${e.lineNumber}`);
    Logger.log(`ERRO CRÍTICO: Ocorreu um erro inesperado: ${e.message}. Verifique o Logger para detalhes.`);
  }
}