/**
 * Script para processar emails de solicitação de aprovação de regalos
 * e inserir os dados na planilha do Google Sheets
 */

// ID da planilha (extraído da URL)
const SPREADSHEET_ID = '1zZKbLVkwo7HDanWbliIy76NgmPf6c_l02UaqXk1zFt0';
const SHEET_NAME = 'aprovados';
const SHEET_NAO_APROVADOS = 'Não Aprovados';
const SHEET_NAO_APROVADOS_VALOR = 'Não Aprovados Valor';
const LABEL_NAME = 'Processados_Analytics';
const VALOR_LIMITE_APROVACAO = 1000; // Aprovar apenas valores menores que 1000 dólares

/**
 * Função para servir a interface HTML
 */
function doGet() {
  const htmlOutput = HtmlService.createHtmlOutputFromFile('Interface')
    .setTitle('Processador de Emails - Aprovação de Regalos')
    .setWidth(600)
    .setHeight(500);
  return htmlOutput;
}

/**
 * Função principal que processa os emails (usa valor padrão)
 */
function processarEmailsAprovacao() {
  return processarEmailsComValorLimite(VALOR_LIMITE_APROVACAO);
}

/**
 * Função que processa os emails com valor limite customizado
 * @param {number} valorLimite - Valor limite de aprovação em USD
 * @return {Object} Objeto com resultado e estatísticas
 */
function processarEmailsComValorLimite(valorLimite) {
  try {
    // Validar valor limite
    if (typeof valorLimite !== 'number' || valorLimite < 0) {
      return {
        success: false,
        message: 'Valor limite inválido. Deve ser um número maior ou igual a zero.'
      };
    }
    
    // Obter ou criar a label
    const label = obterOuCriarLabel(LABEL_NAME);
    
    // Buscar emails que contenham "Solicitud de aprobación de Nuevo regalo" no assunto:
    // - Estão na caixa de entrada (in:inbox)
    // - Não estão lidos (is:unread)
    // - NÃO têm a label (não processados)
    // Usa subject: sem aspas para buscar emails que CONTÉM a string, não apenas exato
    const query = 'subject:Solicitud de aprobación de Nuevo regalo in:inbox is:unread -label:' + LABEL_NAME;
    const threads = GmailApp.search(query, 0, 50); // Buscar até 50 emails
    
    if (threads.length === 0) {
      Logger.log('Nenhum email encontrado com o assunto especificado ou todos já foram processados.');
      return {
        success: true,
        message: 'Nenhum email encontrado para processar.',
        estatisticas: {
          total: 0,
          aprovados: 0,
          naoAprovadosValor: 0,
          naoAprovadosErro: 0
        }
      };
    }
    
    // Abrir a planilha
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    
    // Obter ou criar todas as abas necessárias
    const sheetAprovados = obterOuCriarAba(spreadsheet, SHEET_NAME);
    const sheetNaoAprovados = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS);
    const sheetNaoAprovadosValor = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS_VALOR);
    
    // Contadores para estatísticas
    let totalProcessados = 0;
    let totalAprovados = 0;
    let totalNaoAprovadosValor = 0;
    let totalNaoAprovadosErro = 0;
    
    // Processar cada thread de email
    threads.forEach(function(thread) {
      const messages = thread.getMessages();
      
      // Verificar se o thread já tem a label (dupla verificação)
      const threadLabels = thread.getLabels();
      let threadJaTemLabel = false;
      for (let i = 0; i < threadLabels.length; i++) {
        if (threadLabels[i].getName() === LABEL_NAME) {
          threadJaTemLabel = true;
          break;
        }
      }
      
      if (threadJaTemLabel) {
        Logger.log('Thread já possui label, pulando thread.');
        return;
      }
      
      let threadProcessado = false;
      
      messages.forEach(function(message) {
        try {
          // Verificar se o email já foi processado (verificado em todas as planilhas)
          const messageId = message.getId();
          
          // Verificar se o email está na caixa de entrada e não está lido
          if (message.isInInbox() === false) {
            Logger.log('Email não está na caixa de entrada, pulando: ' + message.getSubject());
            return;
          }
          
          if (message.isUnread() === false) {
            Logger.log('Email já está lido, pulando: ' + message.getSubject());
            return;
          }
          
          // Verificar se o assunto contém "Solicitud de aprobación de Nuevo regalo"
          const subject = message.getSubject();
          if (!subject.includes('Solicitud de aprobación de Nuevo regalo')) {
            Logger.log('Email com assunto que não contém "Solicitud de aprobación de Nuevo regalo", pulando: ' + subject);
            return;
          }
          
          // Verificar se já foi processado em qualquer aba
          if (emailJaProcessadoEmQualquerAba(spreadsheet, messageId)) {
            Logger.log('Email já processado, pulando: ' + subject);
            return;
          }
          
          // Extrair informações do email (subject já foi obtido acima)
          const date = message.getDate();
          
          // Ler o corpo completo do email (texto plano e HTML)
          const plainBody = message.getPlainBody() || '';
          const htmlBody = message.getBody() || '';
          
          // Combinar ambos os formatos para garantir que capturamos todo o conteúdo
          // Converter HTML para texto simples removendo tags
          let bodyText = plainBody;
          if (htmlBody) {
            // Remover tags HTML mas manter o texto
            const htmlText = htmlBody.replace(/<[^>]+>/g, ' ')
                                     .replace(/&nbsp;/g, ' ')
                                     .replace(/&amp;/g, '&')
                                     .replace(/&lt;/g, '<')
                                     .replace(/&gt;/g, '>')
                                     .replace(/&quot;/g, '"')
                                     .replace(/\s+/g, ' ')
                                     .trim();
            
            // Combinar ambos, priorizando o texto plano mas adicionando conteúdo do HTML
            if (htmlText && htmlText.length > plainBody.length) {
              bodyText = plainBody + '\n' + htmlText;
            }
          }
          
          // Usar o corpo completo para busca
          const body = bodyText;
          
          Logger.log('Tamanho do corpo do email: ' + body.length + ' caracteres');
          
          // Extrair o valor do email
          // Formato esperado: "Monto total en dolares: USD U$S1.072,87"
          // Vamos buscar linha por linha primeiro (mais confiável)
          let valorMatch = null;
          const linhas = body.split(/\r?\n/);
          
          // Busca linha por linha - mais preciso
          for (let i = 0; i < linhas.length; i++) {
            const linha = linhas[i].trim();
            
            // Verificar se a linha contém "Monto total en dolares"
            if (linha.toLowerCase().includes('monto total en dolares')) {
              Logger.log('Linha encontrada: ' + linha);
              
              // Remover asteriscos e outros caracteres de formatação markdown
              const linhaLimpa = linha.replace(/\*/g, '').replace(/_/g, '').replace(/`/g, '').trim();
              
              // Padrão 1: "*Monto total en dolares*: USD U$S1.072,87" (com asteriscos, sem espaço entre U$S e número)
              valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
              
              // Padrão 2: "*Monto total en dolares*: USD U$S 1.072,87" (com asteriscos, com espaço)
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
              }
              
              // Padrão 3: "*Monto total en dolares*: USD 1.072,87" (com asteriscos, sem U$S)
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s+([\d.,]+)/i);
              }
              
              // Padrão 4: Qualquer número após "Monto total en dolares:"
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
              }
              
              // Padrão 5: Mais simples - busca qualquer sequência de dígitos, pontos e vírgulas após ":"
              if (!valorMatch) {
                const indice = linhaLimpa.toLowerCase().indexOf('monto total en dolares:');
                if (indice !== -1) {
                  const depoisDoisPontos = linhaLimpa.substring(indice + 'monto total en dolares:'.length);
                  valorMatch = depoisDoisPontos.match(/([\d.,]+)/);
                }
              }
              
              // Padrão 6: Busca direta na linha original (caso tenha formatação especial)
              if (!valorMatch) {
                // Buscar após "dolares:" qualquer coisa até encontrar número
                const matchDolares = linha.match(/dolares[:\s]*[^\d]*([\d.,]+)/i);
                if (matchDolares) {
                  valorMatch = matchDolares;
                }
              }
              
              if (valorMatch) {
                Logger.log('Valor encontrado na linha ' + (i + 1) + ': ' + valorMatch[1]);
                break;
              } else {
                Logger.log('Nenhum padrão de valor encontrado na linha: ' + linha);
              }
            }
          }
          
          // Se não encontrou linha por linha, tenta no corpo completo (removendo asteriscos)
          if (!valorMatch) {
            // Remover asteriscos do corpo para busca
            const bodyLimpo = body.replace(/\*/g, '');
            
            // Padrão 1: "Monto total en dolares: USD U$S1.072,87" (sem espaço)
            valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
            
            // Padrão 2: "Monto total en dolares: USD U$S 1.072,87" (com espaço)
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
            }
            
            // Padrão 3: Qualquer coisa após "Monto total en dolares:" até encontrar número
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
            }
            
            // Padrão 4: Busca direta após "dolares:"
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/dolares[:\s]*[^\d]*([\d.,]+)/i);
            }
          }
          
          let valor = '';
          let valorNumerico = null;
          let erroProcessamento = false;
          let mensagemErro = '';
          
          if (valorMatch && valorMatch[1]) {
            const valorExtraido = valorMatch[1].trim();
            valor = 'USD U$S' + valorExtraido;
            
            // Converter valor para número
            // Formato esperado: 1.072,87 (ponto como milhar, vírgula como decimal)
            // Ou: 1,072.87 (vírgula como milhar, ponto como decimal)
            let valorLimpo = valorExtraido;
            
            // Detectar formato: se tem vírgula e ponto, verificar qual é decimal
            if (valorLimpo.includes(',') && valorLimpo.includes('.')) {
              // Se vírgula vem depois do ponto, vírgula é decimal (ex: 1.072,87)
              if (valorLimpo.indexOf(',') > valorLimpo.indexOf('.')) {
                valorLimpo = valorLimpo.replace(/\./g, '').replace(',', '.');
              } else {
                // Se ponto vem depois da vírgula, ponto é decimal (ex: 1,072.87)
                valorLimpo = valorLimpo.replace(/,/g, '');
              }
            } else if (valorLimpo.includes(',')) {
              // Só tem vírgula - pode ser decimal ou milhar
              // Se tem mais de 3 dígitos antes da vírgula, é milhar
              const partes = valorLimpo.split(',');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/,/g, '');
              } else {
                valorLimpo = valorLimpo.replace(',', '.');
              }
            } else if (valorLimpo.includes('.')) {
              // Só tem ponto - pode ser decimal ou milhar
              // Se tem mais de 3 dígitos antes do ponto, é milhar
              const partes = valorLimpo.split('.');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/\./g, '');
              }
            }
            
            valorNumerico = parseFloat(valorLimpo);
            
            if (isNaN(valorNumerico)) {
              erroProcessamento = true;
              mensagemErro = 'Erro ao converter valor numérico: ' + valorExtraido;
            } else {
              Logger.log('Valor extraído: ' + valorExtraido + ' -> ' + valorNumerico);
            }
          } else {
            erroProcessamento = true;
            mensagemErro = 'Valor não encontrado no email';
            
            // Log detalhado para debug
            Logger.log('Valor não encontrado. Buscando linha com "Monto total en dolares"...');
            const linhas = body.split('\n');
            for (let i = 0; i < linhas.length; i++) {
              if (linhas[i].toLowerCase().includes('monto total en dolares')) {
                Logger.log('Linha encontrada (' + (i + 1) + '): ' + linhas[i]);
                // Mostrar também as linhas próximas
                for (let j = Math.max(0, i - 1); j <= Math.min(linhas.length - 1, i + 2); j++) {
                  Logger.log('  Linha ' + (j + 1) + ': ' + linhas[j]);
                }
                break;
              }
            }
            Logger.log('Corpo do email (primeiros 1000 chars): ' + body.substring(0, 1000));
          }
          
          // Extrair o link "Aprobar" do corpo do email (usar HTML original para links)
          const linkAprobar = extrairLinkAprobar(body, htmlBody);
          
          if (!linkAprobar) {
            if (!erroProcessamento) {
              erroProcessamento = true;
              mensagemErro = 'Link de aprovação não encontrado';
            }
          }
          
          // Preparar dados para inserção
          const rowData = [
            subject,
            date,
            valor,
            linkAprobar || '',
            messageId,
            ''
          ];
          
          // Decidir em qual aba inserir baseado nas regras
          let sheetDestino = null;
          let status = '';
          let deveAprovar = false;
          
          if (erroProcessamento) {
            // Erro no processamento -> aba "Não Aprovados"
            sheetDestino = sheetNaoAprovados;
            status = 'Erro: ' + mensagemErro;
            rowData[5] = status;
            totalNaoAprovadosErro++;
            Logger.log('Email com erro, inserindo em "Não Aprovados": ' + subject);
          } else if (valorNumerico >= valorLimite) {
            // Valor >= valorLimite -> aba "Não Aprovados Valor"
            sheetDestino = sheetNaoAprovadosValor;
            status = 'Valor acima do limite (USD ' + valorNumerico + ' >= ' + valorLimite + ')';
            rowData[5] = status;
            totalNaoAprovadosValor++;
            Logger.log('Email com valor acima do limite, inserindo em "Não Aprovados Valor": ' + subject);
          } else {
            // Valor < valorLimite e sem erro -> aba "aprovados"
            sheetDestino = sheetAprovados;
            status = 'Processado - Aguardando aprovação';
            rowData[5] = status;
            deveAprovar = true;
            totalAprovados++;
            Logger.log('Email aprovado, inserindo em "aprovados": ' + subject);
          }
          
          // Inserir dados na aba apropriada
          sheetDestino.appendRow(rowData);
          totalProcessados++;
          
          // Tentar aprovar automaticamente se valor < 1000 e link disponível
          if (deveAprovar && linkAprobar) {
            try {
              Logger.log('Tentando aprovar automaticamente: ' + linkAprobar);
              
              // Primeiro tenta GET (método mais comum para links de aprovação)
              let response = UrlFetchApp.fetch(linkAprobar, {
                'method': 'get',
                'followRedirects': true,
                'muteHttpExceptions': true,
                'headers': {
                  'User-Agent': 'Mozilla/5.0 (compatible; GoogleAppsScript)'
                }
              });
              
              const statusCode = response.getResponseCode();
              
              // Se GET não funcionou (código diferente de 200), tenta POST
              if (statusCode !== 200) {
                Logger.log('GET retornou código ' + statusCode + ', tentando POST...');
                response = UrlFetchApp.fetch(linkAprobar, {
                  'method': 'post',
                  'followRedirects': true,
                  'muteHttpExceptions': true,
                  'headers': {
                    'User-Agent': 'Mozilla/5.0 (compatible; GoogleAppsScript)',
                    'Content-Type': 'application/x-www-form-urlencoded'
                  }
                });
              }
              
              // Obter a última linha após inserir os dados
              const ultimaLinha = sheetAprovados.getLastRow();
              const finalStatusCode = response.getResponseCode();
              
              if (finalStatusCode === 200 || finalStatusCode === 201 || finalStatusCode === 302) {
                // Atualizar status na planilha
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Aprovado automaticamente');
                Logger.log('Aprovado automaticamente com sucesso! Código: ' + finalStatusCode);
              } else {
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Erro na aprovação: código ' + finalStatusCode);
                Logger.log('Erro ao aprovar: código ' + finalStatusCode + '. Resposta: ' + response.getContentText().substring(0, 200));
              }
              
              // Pequeno delay para evitar muitas requisições
              Utilities.sleep(500);
              
            } catch (error) {
              const ultimaLinha = sheetAprovados.getLastRow();
              sheetAprovados.getRange(ultimaLinha, 6).setValue('Erro na aprovação: ' + error.toString());
              Logger.log('Erro ao aprovar link: ' + linkAprobar + ' - ' + error.toString());
            }
          }
          
          threadProcessado = true;
          
        } catch (error) {
          // Em caso de erro inesperado, inserir na aba "Não Aprovados"
          try {
            const subject = message.getSubject();
            const date = message.getDate();
            const messageId = message.getId();
            
            const rowData = [
              subject,
              date,
              'Erro na extração',
              '',
              messageId,
              'Erro inesperado: ' + error.toString()
            ];
            
            sheetNaoAprovados.appendRow(rowData);
            totalNaoAprovadosErro++;
            totalProcessados++;
            Logger.log('Erro inesperado ao processar email, inserido em "Não Aprovados": ' + error.toString());
          } catch (erroInserir) {
            Logger.log('Erro crítico ao inserir email com erro: ' + erroInserir.toString());
          }
        }
        
        // Marcar email como lido
        message.markRead();
        Logger.log('Email marcado como lido: ' + message.getSubject());
      });
      
      // Aplicar a label ao thread se pelo menos uma mensagem foi processada
      if (threadProcessado) {
        thread.addLabel(label);
        Logger.log('Label aplicada ao thread.');
      }
    });
    
    Logger.log('Processamento concluído!');
    
    // Retornar resultado com estatísticas
    return {
      success: true,
      message: 'Processamento concluído com sucesso!',
      estatisticas: {
        total: totalProcessados,
        aprovados: totalAprovados,
        naoAprovadosValor: totalNaoAprovadosValor,
        naoAprovadosErro: totalNaoAprovadosErro
      }
    };
    
  } catch (error) {
    Logger.log('Erro ao processar emails: ' + error.toString());
    return {
      success: false,
      message: 'Erro ao processar emails: ' + error.toString(),
      estatisticas: {
        total: totalProcessados || 0,
        aprovados: totalAprovados || 0,
        naoAprovadosValor: totalNaoAprovadosValor || 0,
        naoAprovadosErro: totalNaoAprovadosErro || 0
      }
    };
  }
}

/**
 * Extrai o link "Aprobar" do corpo do email
 * @param {string} plainBody - Corpo do email em texto plano
 * @param {string} htmlBody - Corpo do email em HTML
 * @return {string} URL do link Aprobar ou string vazia
 */
function extrairLinkAprobar(plainBody, htmlBody) {
  try {
    // Tentar extrair do HTML primeiro (mais preciso)
    if (htmlBody) {
      // Procurar por links que contenham "Aprobar" no texto
      const htmlMatch = htmlBody.match(/<a[^>]*>.*?Aprobar.*?<\/a>/i);
      if (htmlMatch) {
        const linkMatch = htmlMatch[0].match(/href=["']([^"']+)["']/i);
        if (linkMatch) {
          return linkMatch[1];
        }
      }
      
      // Procurar por qualquer link que contenha "aprobar" na URL
      const urlMatch = htmlBody.match(/href=["']([^"']*aprobar[^"']*)["']/i);
      if (urlMatch) {
        return urlMatch[1];
      }
    }
    
    // Tentar extrair do texto plano (menos preciso)
    if (plainBody) {
      // Procurar por URLs próximas à palavra "Aprobar"
      const lines = plainBody.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes('aprobar')) {
          // Procurar URL na mesma linha ou próxima
          const urlRegex = /(https?:\/\/[^\s]+)/i;
          const urlMatch = lines[i].match(urlRegex) || 
                          (i + 1 < lines.length ? lines[i + 1].match(urlRegex) : null);
          if (urlMatch) {
            return urlMatch[1];
          }
        }
      }
    }
    
    return '';
  } catch (error) {
    Logger.log('Erro ao extrair link Aprobar: ' + error.toString());
    return '';
  }
}

/**
 * Verifica se o email já foi processado em qualquer aba
 * @param {Spreadsheet} spreadsheet - Planilha
 * @param {string} messageId - ID do email
 * @return {boolean} true se já foi processado
 */
function emailJaProcessadoEmQualquerAba(spreadsheet, messageId) {
  try {
    const abas = [SHEET_NAME, SHEET_NAO_APROVADOS, SHEET_NAO_APROVADOS_VALOR];
    
    for (let i = 0; i < abas.length; i++) {
      const sheet = spreadsheet.getSheetByName(abas[i]);
      if (sheet) {
        const data = sheet.getDataRange().getValues();
        
        // A coluna E (índice 4) contém o ID do email
        for (let j = 1; j < data.length; j++) { // Começar do índice 1 para pular cabeçalho
          if (data[j][4] === messageId) {
            return true;
          }
        }
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
    const cabecalhos = ['Título', 'Data/Hora Recebimento', 'Valor (USD)', 'Link Aprobar', 'ID Email', 'Status'];
    
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
 * Função para aprovar automaticamente usando o link extraído
 * Aprova apenas casos com valor < 1000 dólares
 * ATENÇÃO: Use com cuidado - esta função fará requisições HTTP para os links
 */
function aprovarAutomaticamente() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      Logger.log('Aba "aprovados" não encontrada.');
      return;
    }
    
    const data = sheet.getDataRange().getValues();
    
    // Processar linhas que têm link mas status não é "Aprovado"
    for (let i = 1; i < data.length; i++) {
      const valorTexto = data[i][2]; // Coluna C (índice 2) - Valor
      const linkAprobar = data[i][3]; // Coluna D (índice 3) - Link
      const status = data[i][5]; // Coluna F (índice 5) - Status
      
      // Extrair valor numérico
      let valorNumerico = null;
      if (valorTexto && valorTexto.includes('USD')) {
        const valorMatch = valorTexto.match(/([\d.,]+)/);
        if (valorMatch) {
          const valorLimpo = valorMatch[1].replace(/\./g, '').replace(',', '.');
          valorNumerico = parseFloat(valorLimpo);
        }
      }
      
      // Aprovar apenas se:
      // - Tem link válido
      // - Status não é "Aprovado" ou "Aprovado automaticamente"
      // - Valor é menor que o limite (ou não foi possível extrair o valor)
      const podeAprovar = linkAprobar && 
                         linkAprobar.startsWith('http') && 
                         status !== 'Aprovado' && 
                         status !== 'Aprovado automaticamente' &&
                         (valorNumerico === null || valorNumerico < VALOR_LIMITE_APROVACAO);
      
      if (podeAprovar) {
        try {
          // Fazer requisição GET para o link
          const response = UrlFetchApp.fetch(linkAprobar, {
            'method': 'get',
            'followRedirects': true,
            'muteHttpExceptions': true
          });
          
          if (response.getResponseCode() === 200) {
            // Atualizar status na planilha
            sheet.getRange(i + 1, 6).setValue('Aprovado automaticamente');
            Logger.log('Aprovado: ' + linkAprobar);
          } else {
            sheet.getRange(i + 1, 6).setValue('Erro na aprovação: código ' + response.getResponseCode());
            Logger.log('Erro ao aprovar: código ' + response.getResponseCode());
          }
          
          // Pequeno delay para evitar muitas requisições
          Utilities.sleep(1000);
          
        } catch (error) {
          Logger.log('Erro ao aprovar link: ' + linkAprobar + ' - ' + error.toString());
          sheet.getRange(i + 1, 6).setValue('Erro: ' + error.toString());
        }
      } else if (valorNumerico !== null && valorNumerico >= VALOR_LIMITE_APROVACAO) {
        Logger.log('Pulando aprovação - valor acima do limite: USD ' + valorNumerico);
      }
    }
    
    Logger.log('Processo de aprovação automática concluído.');
    
  } catch (error) {
    Logger.log('Erro na aprovação automática: ' + error.toString());
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
    if (trigger.getHandlerFunction() === 'processarEmailsAprovacao') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Criar novo trigger para executar a cada hora
  ScriptApp.newTrigger('processarEmailsAprovacao')
    .timeBased()
    .everyHours(1)
    .create();
  
  Logger.log('Trigger criado com sucesso! O script executará automaticamente a cada hora.');
}
