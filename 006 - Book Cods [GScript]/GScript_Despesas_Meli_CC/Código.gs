/**
 * Script para processar emails de notificação de transação do Citi
 * e inserir os dados na planilha do Google Sheets
 */

// ID da planilha (extraído da URL)
const SPREADSHEET_ID = '1pYY6aQLUJrTv3E_rgA-UiMRoG_FuQBvNLiXyoMLjERs';
const SHEET_NAME_CC = 'Despesas CC'; // Nome da aba para despesas do Citi
const LABEL_NAME_MELI = 'Processados_DespesasMeli';
const SUBJECT_FILTER = 'Notification of transaction';

/**
 * Função principal que processa os emails
 */
function processarEmailsTransacao() {
  try {
    // Obter ou criar a label
    const label = obterOuCriarLabel(LABEL_NAME_MELI);
    
    // Buscar emails que:
    // - Tenham o assunto "Notification of transaction"
    // - Sejam apenas de 2026 (after:2025/12/31 before:2027/1/1)
    // - Podem estar lidos ou não lidos
    // - Podem ter tags/labels ou não (busca todos, com e sem a tag de processados)
    const query = 'subject:"' + SUBJECT_FILTER + '" after:2025/12/31 before:2027/1/1';
    const threads = GmailApp.search(query, 0, 500); // Buscar até 500 emails (aumentado para pegar mais)
    
    if (threads.length === 0) {
      Logger.log('Nenhum email encontrado com os critérios especificados ou todos já foram processados.');
      return;
    }
    
    Logger.log('Encontrados ' + threads.length + ' threads de email para processar.');
    
    // Abrir a planilha
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    
    // Obter ou criar a aba
    const sheet = obterOuCriarAba(spreadsheet, SHEET_NAME_CC);
    
    // Processar cada thread de email
    threads.forEach(function(thread) {
      const messages = thread.getMessages();
      
      let threadProcessado = false;
      
      messages.forEach(function(message) {
        try {
          // Verificar se o email já foi processado (verificação principal para evitar duplicatas)
          const messageId = message.getId();
          
          // Verificar critérios: apenas assunto
          const subject = message.getSubject();
          
          if (!subject.includes(SUBJECT_FILTER)) {
            Logger.log('Email não contém "Notification of transaction" no assunto, pulando: ' + subject);
            return;
          }
          
          // Extrair informações do email
          const date = message.getDate();
          
          // Verificar se o email é de 2026
          const anoEmail = date.getFullYear();
          if (anoEmail !== 2026) {
            Logger.log('Email não é de 2026 (ano: ' + anoEmail + '), pulando: ' + subject);
            return;
          }
          
          // Verificar se já foi processado (verificação pela planilha, não pela label)
          if (emailJaProcessado(sheet, messageId)) {
            Logger.log('Email já processado (encontrado na planilha), pulando: ' + subject);
            return;
          }
          
          // Ler o corpo completo do email (texto plano e HTML)
          const plainBody = message.getPlainBody() || '';
          const htmlBody = message.getBody() || '';
          
          // Combinar ambos os formatos para garantir que capturamos todo o conteúdo
          let bodyText = plainBody;
          if (htmlBody) {
            // Remover tags HTML mas manter o texto
            const htmlText = htmlBody.replace(/<[^>]+>/g, ' ')
                                     .replace(/&nbsp;/g, ' ')
                                     .replace(/&amp;/g, '&')
                                     .replace(/&lt;/g, '<')
                                     .replace(/&gt;/g, '>')
                                     .replace(/&quot;/g, '"')
                                     .replace(/&#58;/g, ':')
                                     .replace(/\s+/g, ' ')
                                     .trim();
            
            // Combinar ambos, priorizando o texto plano mas adicionando conteúdo do HTML
            if (htmlText && htmlText.length > plainBody.length) {
              bodyText = plainBody + '\n' + htmlText;
            }
          }
          
          Logger.log('Processando email: ' + subject);
          Logger.log('Tamanho do corpo do email: ' + bodyText.length + ' caracteres');
          
          // Extrair data local do email
          // Formato esperado: "DATE: 16/01/2026" ou "DATE&#58; 16/01/2026"
          const dataLocal = extrairDataLocal(bodyText);
          
          // Extrair valor do email
          // Formato esperado: "15,200.00 ARS" ou "amount of 15,200.00 ARS"
          const valor = extrairValor(bodyText);
          
          // Extrair local onde foi gasto
          // Formato esperado: "at LUCCIANOS" ou "at LUCCIANOS."
          const local = extrairLocal(bodyText);
          
          // Preparar dados para inserção
          const rowData = [
            dataLocal || '',           // Data local
            valor || '',               // Valor
            local || '',               // Local
            date,                      // Data/hora do email
            subject,                   // Assunto
            messageId                  // ID do email
          ];
          
          // Inserir dados na planilha
          sheet.appendRow(rowData);
          Logger.log('Dados inseridos: Data=' + dataLocal + ', Valor=' + valor + ', Local=' + local);
          
          // Marcar email como lido (se ainda não estiver)
          if (!message.isRead()) {
            message.markRead();
            Logger.log('Email marcado como lido: ' + subject);
          }
          
          // Aplicar a label ao thread (sempre, mesmo que já tenha outras tags)
          try {
            thread.addLabel(label);
            Logger.log('Label "' + LABEL_NAME_MELI + '" aplicada ao thread.');
          } catch (labelError) {
            // Se a label já existir, não é um erro crítico
            Logger.log('Label já existe no thread ou erro ao aplicar: ' + labelError.toString());
          }
          
          threadProcessado = true;
          
        } catch (error) {
          // Em caso de erro inesperado, logar mas continuar
          Logger.log('Erro ao processar email: ' + error.toString());
          Logger.log('Stack trace: ' + error.stack);
        }
      });
      
      // Nota: A label já é aplicada individualmente para cada mensagem processada acima
      // Isso garante que mesmo e-mails já processados anteriormente recebam a label
    });
    
    Logger.log('Processamento concluído!');
    
  } catch (error) {
    Logger.log('Erro ao processar emails: ' + error.toString());
    throw error;
  }
}

/**
 * Extrai a data local do corpo do email
 * @param {string} bodyText - Corpo do email em texto
 * @return {string} Data no formato DD/MM/YYYY ou string vazia
 */
function extrairDataLocal(bodyText) {
  try {
    // Padrão 1: "DATE: 16/01/2026" ou "DATE&#58; 16/01/2026"
    let dataMatch = bodyText.match(/DATE\s*[:\u003A]\s*(\d{1,2}\/\d{1,2}\/\d{4})/i);
    
    // Padrão 2: "DATE 16/01/2026" (sem dois pontos)
    if (!dataMatch) {
      dataMatch = bodyText.match(/DATE\s+(\d{1,2}\/\d{1,2}\/\d{4})/i);
    }
    
    // Padrão 3: Buscar qualquer data no formato DD/MM/YYYY próxima à palavra "DATE"
    if (!dataMatch) {
      const linhas = bodyText.split(/\r?\n/);
      for (let i = 0; i < linhas.length; i++) {
        const linha = linhas[i].trim();
        if (linha.toUpperCase().includes('DATE')) {
          // Buscar data na mesma linha
          const match = linha.match(/(\d{1,2}\/\d{1,2}\/\d{4})/);
          if (match) {
            dataMatch = match;
            break;
          }
          // Buscar data na próxima linha
          if (i + 1 < linhas.length) {
            const matchNext = linhas[i + 1].trim().match(/(\d{1,2}\/\d{1,2}\/\d{4})/);
            if (matchNext) {
              dataMatch = matchNext;
              break;
            }
          }
        }
      }
    }
    
    if (dataMatch && dataMatch[1]) {
      Logger.log('Data encontrada: ' + dataMatch[1]);
      return dataMatch[1];
    }
    
    Logger.log('Data não encontrada no email');
    return '';
  } catch (error) {
    Logger.log('Erro ao extrair data local: ' + error.toString());
    return '';
  }
}

/**
 * Extrai o valor do corpo do email
 * @param {string} bodyText - Corpo do email em texto
 * @return {string} Valor com moeda (ex: "15,200.00 ARS") ou string vazia
 */
function extrairValor(bodyText) {
  try {
    // Padrão 1: "amount of 15,200.00 ARS" ou "amount of 15,200.00 ARS at"
    let valorMatch = bodyText.match(/amount\s+of\s+([\d,]+\.?\d*)\s+ARS/i);
    
    // Padrão 2: "15,200.00 ARS" (buscar padrão de valor com vírgula como milhar e ponto como decimal)
    if (!valorMatch) {
      valorMatch = bodyText.match(/([\d,]+\.\d{2})\s+ARS/i);
    }
    
    // Padrão 3: "15,200.00 ARS" (buscar qualquer número seguido de ARS)
    if (!valorMatch) {
      valorMatch = bodyText.match(/([\d,]+\.?\d*)\s+ARS/i);
    }
    
    // Padrão 4: Buscar linha por linha por "amount" ou "ARS"
    if (!valorMatch) {
      const linhas = bodyText.split(/\r?\n/);
      for (let i = 0; i < linhas.length; i++) {
        const linha = linhas[i].trim();
        
        // Se a linha contém "amount" ou "ARS", buscar valor
        if (linha.toLowerCase().includes('amount') || linha.includes('ARS')) {
          // Remover asteriscos e outros caracteres de formatação
          const linhaLimpa = linha.replace(/\*/g, '').replace(/_/g, '').replace(/`/g, '').trim();
          
          // Buscar padrão de valor
          const match = linhaLimpa.match(/([\d,]+\.?\d*)\s*ARS/i);
          if (match) {
            valorMatch = match;
            break;
          }
          
          // Buscar após "amount of"
          const matchAmount = linhaLimpa.match(/amount\s+of\s+([\d,]+\.?\d*)/i);
          if (matchAmount) {
            valorMatch = matchAmount;
            break;
          }
        }
      }
    }
    
    if (valorMatch && valorMatch[1]) {
      const valorExtraido = valorMatch[1].trim();
      const valorFormatado = valorExtraido + ' ARS';
      Logger.log('Valor encontrado: ' + valorFormatado);
      return valorFormatado;
    }
    
    Logger.log('Valor não encontrado no email');
    
    // Log detalhado para debug
    Logger.log('Buscando linha com "amount" ou "ARS"...');
    const linhas = bodyText.split('\n');
    for (let i = 0; i < linhas.length; i++) {
      if (linhas[i].toLowerCase().includes('amount') || linhas[i].includes('ARS')) {
        Logger.log('Linha encontrada (' + (i + 1) + '): ' + linhas[i]);
      }
    }
    
    return '';
  } catch (error) {
    Logger.log('Erro ao extrair valor: ' + error.toString());
    return '';
  }
}

/**
 * Extrai o local onde foi gasto do corpo do email
 * @param {string} bodyText - Corpo do email em texto
 * @return {string} Nome do local (ex: "LUCCIANOS") ou string vazia
 */
function extrairLocal(bodyText) {
  try {
    // Padrão 1: "amount of 15,200.00 ARS at LUCCIANOS" ou "amount of 15,200.00 ARS at LUCCIANOS."
    let localMatch = bodyText.match(/amount\s+of\s+[\d,]+\.?\d*\s+ARS\s+at\s+([A-Za-z0-9\s]+?)(?:\.|$|\n)/i);
    
    // Padrão 2: "at LUCCIANOS" (buscar após "at" que vem depois de ARS)
    if (!localMatch) {
      localMatch = bodyText.match(/ARS\s+at\s+([A-Za-z0-9\s]+?)(?:\.|$|\n)/i);
    }
    
    // Padrão 3: "was made in the amount of ... at LUCCIANOS"
    if (!localMatch) {
      localMatch = bodyText.match(/was\s+made\s+in\s+the\s+amount\s+of\s+[\d,]+\.?\d*\s+ARS\s+at\s+([A-Za-z0-9\s]+?)(?:\.|$|\n)/i);
    }
    
    // Padrão 4: Buscar linha por linha por "at" após "ARS"
    if (!localMatch) {
      const linhas = bodyText.split(/\r?\n/);
      for (let i = 0; i < linhas.length; i++) {
        const linha = linhas[i].trim();
        
        // Se a linha contém "ARS" e "at", buscar local
        if (linha.includes('ARS') && linha.toLowerCase().includes('at')) {
          // Remover asteriscos e outros caracteres de formatação
          const linhaLimpa = linha.replace(/\*/g, '').replace(/_/g, '').replace(/`/g, '').trim();
          
          // Buscar padrão "at NOME"
          const match = linhaLimpa.match(/at\s+([A-Za-z0-9\s]+?)(?:\.|$)/i);
          if (match) {
            localMatch = match;
            break;
          }
        }
      }
    }
    
    // Padrão 5: Buscar qualquer texto após "at" que não seja muito longo (máximo 50 caracteres)
    if (!localMatch) {
      const matchAt = bodyText.match(/at\s+([A-Za-z0-9\s]{1,50}?)(?:\.|$|\n|,)/i);
      if (matchAt && !matchAt[1].toLowerCase().includes('account') && 
          !matchAt[1].toLowerCase().includes('transaction')) {
        localMatch = matchAt;
      }
    }
    
    if (localMatch && localMatch[1]) {
      const localExtraido = localMatch[1].trim();
      Logger.log('Local encontrado: ' + localExtraido);
      return localExtraido;
    }
    
    Logger.log('Local não encontrado no email');
    
    // Log detalhado para debug
    Logger.log('Buscando linha com "at"...');
    const linhas = bodyText.split('\n');
    for (let i = 0; i < linhas.length; i++) {
      if (linhas[i].toLowerCase().includes('at') && linhas[i].includes('ARS')) {
        Logger.log('Linha encontrada (' + (i + 1) + '): ' + linhas[i]);
      }
    }
    
    return '';
  } catch (error) {
    Logger.log('Erro ao extrair local: ' + error.toString());
    return '';
  }
}

/**
 * Verifica se o email já foi processado
 * @param {Sheet} sheet - Aba da planilha
 * @param {string} messageId - ID do email
 * @return {boolean} true se já foi processado
 */
function emailJaProcessado(sheet, messageId) {
  try {
    const data = sheet.getDataRange().getValues();
    
    // A coluna F (índice 5) contém o ID do email
    for (let j = 1; j < data.length; j++) { // Começar do índice 1 para pular cabeçalho
      if (data[j][5] === messageId) {
        return true;
      }
    }
    
    return false;
  } catch (error) {
    Logger.log('Erro ao verificar email processado: ' + error.toString());
    return false;
  }
}

/**
 * Obtém ou cria uma aba na planilha
 * @param {Spreadsheet} spreadsheet - Planilha
 * @param {string} sheetName - Nome da aba
 * @return {Sheet} Aba da planilha
 */
function obterOuCriarAba(spreadsheet, sheetName) {
  try {
    let sheet = spreadsheet.getSheetByName(sheetName);
    const cabecalhos = ['Data Local', 'Valor', 'Local', 'Data/Hora Email', 'Assunto', 'ID Email'];
    
    if (!sheet) {
      // Criar nova aba
      sheet = spreadsheet.insertSheet(sheetName);
      // Adicionar cabeçalhos
      sheet.appendRow(cabecalhos);
      Logger.log('Aba criada: ' + sheetName);
    } else {
      // Verificar se a aba já tem cabeçalho
      const primeiraLinha = sheet.getRange(1, 1, 1, cabecalhos.length).getValues()[0];
      const temCabecalho = primeiraLinha[0] === cabecalhos[0] && 
                          primeiraLinha[1] === cabecalhos[1] && 
                          primeiraLinha[2] === cabecalhos[2];
      
      if (!temCabecalho) {
        // Se não tem cabeçalho, inserir na primeira linha
        sheet.insertRowBefore(1);
        sheet.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);
        Logger.log('Cabeçalho adicionado à aba: ' + sheetName);
      }
    }
    
    return sheet;
  } catch (error) {
    Logger.log('Erro ao obter/criar aba: ' + sheetName + ' - ' + error.toString());
    throw error;
  }
}

/**
 * Obtém ou cria a label especificada
 * @param {string} labelName - Nome da label
 * @return {GmailLabel} Objeto da label
 */
function obterOuCriarLabel(labelName) {
  try {
    // Tentar obter a label existente
    let label = GmailApp.getUserLabelByName(labelName);
    
    // Se não existir, criar
    if (!label) {
      label = GmailApp.createLabel(labelName);
      Logger.log('Label criada: ' + labelName);
    } else {
      Logger.log('Label encontrada: ' + labelName);
    }
    
    return label;
  } catch (error) {
    Logger.log('Erro ao obter/criar label: ' + error.toString());
    throw error;
  }
}

/**
 * Função para criar um trigger que executa automaticamente
 * Pode ser configurado para executar periodicamente (ex: a cada hora)
 */
function criarTrigger() {
  // Deletar triggers existentes para evitar duplicatas
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'processarEmailsTransacao') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Criar novo trigger para executar a cada hora
  ScriptApp.newTrigger('processarEmailsTransacao')
    .timeBased()
    .everyHours(1)
    .create();
  
  Logger.log('Trigger criado com sucesso! O script executará automaticamente a cada hora.');
}
