/**
 * Script para procesar emails de solicitud de aprobación de regalos
 * e insertar los datos en la hoja de cálculo de Google Sheets
 */

// ID de la hoja de cálculo (extraído de la URL)
const SPREADSHEET_ID = '1zZKbLVkwo7HDanWbliIy76NgmPf6c_l02UaqXk1zFt0';
const SHEET_NAME = 'aprovados';
const SHEET_NAO_APROVADOS = 'No Aprobados';
const SHEET_NAO_APROVADOS_VALOR = 'No Aprobados Valor';
const SHEET_CONFIG = 'Config';
// const LABEL_NAME = 'Processados_Analytics'; // Não é mais necessário - duplicação controlada por messageId
const VALOR_LIMITE_APROVACAO_PADRAO = 1400; // Valor padrão inicial para o límite de aprobación
const EMAIL_ALERTA = 'mariano.tercelan@mercadolibre.com'; // Email para alertas

/**
 * Retorna o login de rede (e-mail) da pessoa que está executando o script.
 * Usado para controle na coluna G das abas Aprovados e No Aprobados.
 * @return {string} E-mail do usuário ou string vazia em caso de falha
 */
function obterLoginRede() {
  try {
    return Session.getActiveUser().getEmail() || '';
  } catch (e) {
    return '';
  }
}

/**
 * Obtiene o crea la hoja de configuración con el valor de corte
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 * @return {Sheet} Hoja de configuración
 */
function obterOuCriarAbaConfig(spreadsheet) {
  try {
    // Validar que spreadsheet no sea undefined
    if (!spreadsheet) {
      Logger.log('Error: spreadsheet es undefined en obterOuCriarAbaConfig');
      // Intentar abrir la hoja de cálculo si no se proporcionó
      spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
      if (!spreadsheet) {
        throw new Error('No se pudo abrir la hoja de cálculo con ID: ' + SPREADSHEET_ID);
      }
    }
    
    let sheet = spreadsheet.getSheetByName(SHEET_CONFIG);
    
    if (!sheet) {
      // Crear nueva hoja de configuración
      sheet = spreadsheet.insertSheet(SHEET_CONFIG);
      
      // Agregar encabezados y valor inicial
      sheet.getRange(1, 1).setValue('Parámetro');
      sheet.getRange(1, 2).setValue('Valor');
      sheet.getRange(2, 1).setValue('Valor Límite de Aprobación (USD)');
      sheet.getRange(2, 2).setValue(VALOR_LIMITE_APROVACAO_PADRAO);
      
      // Formatear encabezados
      sheet.getRange(1, 1, 1, 2).setFontWeight('bold');
      sheet.getRange(1, 1, 1, 2).setBackground('#4285f4');
      sheet.getRange(1, 1, 1, 2).setFontColor('#ffffff');
      
      // Ajustar ancho de columnas
      sheet.setColumnWidth(1, 300);
      sheet.setColumnWidth(2, 200);
      
      Logger.log('Hoja de configuración creada con valor inicial: ' + VALOR_LIMITE_APROVACAO_PADRAO);
    } else {
      // Verificar si tiene el encabezado configurado
      const nomeParametro = sheet.getRange(2, 1).getValue();
      if (!nomeParametro || nomeParametro === '') {
        // Si no tiene el encabezado, agregarlo
        sheet.getRange(2, 1).setValue('Valor Límite de Aprobación (USD)');
        Logger.log('Encabezado agregado a la hoja de configuración');
      }
      // No preencher automaticamente o valor - se estiver vazio, será usado 1000 como padrão
    }
    
    return sheet;
  } catch (error) {
    Logger.log('Error al obtener/crear hoja de configuración: ' + error.toString());
    throw error;
  }
}

/**
 * Obtiene el valor límite de aprobación desde la hoja de configuración
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 * @return {number} Valor límite de aprobación en dólares
 */
function obterValorLimiteAprovacao(spreadsheet) {
  try {
    // Validar que spreadsheet no sea undefined
    if (!spreadsheet) {
      Logger.log('Error: spreadsheet es undefined en obterValorLimiteAprovacao, intentando abrir...');
      spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
      if (!spreadsheet) {
        Logger.log('No se pudo abrir la hoja de cálculo, usando valor por defecto: 1000');
        return 1000;
      }
    }
    
    const sheetConfig = obterOuCriarAbaConfig(spreadsheet);
    const valorLimite = sheetConfig.getRange(2, 2).getValue();
    
    // Si el campo está vacío, usar 1000 como valor por defecto
    if (!valorLimite || valorLimite === '') {
      Logger.log('Campo de valor límite vacío, usando valor por defecto: 1000');
      return 1000;
    }
    
    // Validar que sea un número válido
    const valorNumerico = parseFloat(valorLimite);
    
    if (isNaN(valorNumerico) || valorNumerico < 0) {
      Logger.log('Valor límite inválido en la configuración, usando valor por defecto: 1000');
      return 1000;
    }
    
    Logger.log('Usando valor límite de la configuración: ' + valorNumerico);
    return valorNumerico;
  } catch (error) {
    Logger.log('Error al obtener valor límite de aprobación, usando valor por defecto: 1000 - ' + error.toString());
    return 1000;
  }
}

/**
 * Función principal que procesa los emails
 */
function processarEmailsAprovacao() {
  try {
    // Buscar emails que:
    // - Tienen la etiqueta "Pagos"
    // - Contienen "Nuevo regalo" en el asunto (o "Solicitud de aprobación de Nuevo regalo")
    // - NO contienen "Aprobada" en el asunto (excluir aprobaciones ya procesadas)
    // - Son de los últimos 5 días
    // Nota: La duplicación se controla verificando el messageId en las planillas
    // Nota: Se procesan todos los emails (leídos y no leídos)
    const query = 'label:Pagos subject:Nuevo regalo -subject:"Aprobada" newer_than:5d';
    const threads = GmailApp.search(query, 0, 50); // Buscar hasta 50 emails
    
    if (threads.length === 0) {
      Logger.log('No se encontraron emails con la etiqueta "Pagos" y asunto "Nuevo regalo" de los últimos 5 días, o todos ya fueron procesados.');
      // Enviar email de alerta incluso si no hay emails nuevos
      try {
        const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
        enviarEmailAlerta(spreadsheet);
      } catch (errorAlerta) {
        Logger.log('Error al enviar email de alerta: ' + errorAlerta.toString());
      }
      return;
    }
    
    Logger.log('Se encontraron ' + threads.length + ' hilos de email con la etiqueta "Pagos" para procesar.');
    
    // Abrir la hoja de cálculo
    let spreadsheet;
    try {
      spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
      if (!spreadsheet) {
        throw new Error('SpreadsheetApp.openById retornó null o undefined');
      }
    } catch (error) {
      Logger.log('Error al abrir la hoja de cálculo: ' + error.toString());
      throw new Error('No se pudo abrir la hoja de cálculo con ID: ' + SPREADSHEET_ID + '. Error: ' + error.toString());
    }
    
    // Obtener el valor límite de aprobación desde la hoja de configuración
    const VALOR_LIMITE_APROVACAO = obterValorLimiteAprovacao(spreadsheet);
    Logger.log('Valor límite de aprobación configurado: USD ' + VALOR_LIMITE_APROVACAO);
    
    // Obtener o crear todas las hojas necesarias
    const sheetAprovados = obterOuCriarAba(spreadsheet, SHEET_NAME);
    const sheetNaoAprovados = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS);
    const sheetNaoAprovadosValor = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS_VALOR);
    
    // Procesar cada hilo de email
    threads.forEach(function(thread) {
      const messages = thread.getMessages();
      
      let threadProcessado = false;
      
      messages.forEach(function(message) {
        try {
          // Verificar si el email ya fue procesado (verificado en todas las hojas)
          const messageId = message.getId();
          
          // Verificar si el email tiene la etiqueta "Pagos" y está archivado
          const messageLabels = message.getThread().getLabels();
          let tieneEtiquetaPagos = false;
          for (let j = 0; j < messageLabels.length; j++) {
            if (messageLabels[j].getName() === 'Pagos') {
              tieneEtiquetaPagos = true;
              break;
            }
          }
          
          if (!tieneEtiquetaPagos) {
            Logger.log('El email no tiene la etiqueta "Pagos", saltando: ' + message.getSubject());
            return;
          }
          
          // Verificar si el asunto contiene "Nuevo regalo" o "Solicitud de aprobación de Nuevo regalo"
          const subject = message.getSubject();
          if (!subject.toLowerCase().includes('nuevo regalo') && !subject.includes('Solicitud de aprobación de Nuevo regalo')) {
            Logger.log('Email con asunto que no contiene "Nuevo regalo" o "Solicitud de aprobación de Nuevo regalo", saltando: ' + subject);
            return;
          }
          
          // Verificar si ya fue procesado en cualquier hoja
          if (emailJaProcessadoEmQualquerAba(spreadsheet, messageId)) {
            Logger.log('Email ya procesado, saltando: ' + subject);
            return;
          }
          
          // Extraer información del email (subject ya fue obtenido arriba)
          const date = message.getDate();
          
          // Leer el cuerpo completo del email (texto plano y HTML)
          const plainBody = message.getPlainBody() || '';
          const htmlBody = message.getBody() || '';
          
          // Combinar ambos formatos para garantizar que capturamos todo el contenido
          // Convertir HTML a texto simple removiendo etiquetas
          let bodyText = plainBody;
          if (htmlBody) {
            // Remover etiquetas HTML pero mantener el texto
            const htmlText = htmlBody.replace(/<[^>]+>/g, ' ')
                                     .replace(/&nbsp;/g, ' ')
                                     .replace(/&amp;/g, '&')
                                     .replace(/&lt;/g, '<')
                                     .replace(/&gt;/g, '>')
                                     .replace(/&quot;/g, '"')
                                     .replace(/\s+/g, ' ')
                                     .trim();
            
            // Combinar ambos, priorizando el texto plano pero agregando contenido del HTML
            if (htmlText && htmlText.length > plainBody.length) {
              bodyText = plainBody + '\n' + htmlText;
            }
          }
          
          // Usar el cuerpo completo para búsqueda
          const body = bodyText;
          
          Logger.log('Tamaño del cuerpo del email: ' + body.length + ' caracteres');
          
          // Extraer el valor del email
          // Formato esperado: "Monto total en dolares: USD U$S1.072,87"
          // Vamos a buscar línea por línea primero (más confiable)
          let valorMatch = null;
          const linhas = body.split(/\r?\n/);
          
          // Búsqueda línea por línea - más preciso
          for (let i = 0; i < linhas.length; i++) {
            const linha = linhas[i].trim();
            
            // Verificar si la línea contiene "Monto total en dolares"
            if (linha.toLowerCase().includes('monto total en dolares')) {
              Logger.log('Línea encontrada: ' + linha);
              
              // Remover asteriscos y otros caracteres de formateo markdown
              const linhaLimpa = linha.replace(/\*/g, '').replace(/_/g, '').replace(/`/g, '').trim();
              
              // Patrón 1: "*Monto total en dolares*: USD U$S1.072,87" (con asteriscos, sin espacio entre U$S y número)
              valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
              
              // Patrón 2: "*Monto total en dolares*: USD U$S 1.072,87" (con asteriscos, con espacio)
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
              }
              
              // Patrón 3: "*Monto total en dolares*: USD 1.072,87" (con asteriscos, sin U$S)
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s+([\d.,]+)/i);
              }
              
              // Patrón 4: Cualquier número después de "Monto total en dolares:"
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
              }
              
              // Patrón 5: Más simple - busca cualquier secuencia de dígitos, puntos y comas después de ":"
              if (!valorMatch) {
                const indice = linhaLimpa.toLowerCase().indexOf('monto total en dolares:');
                if (indice !== -1) {
                  const depoisDoisPontos = linhaLimpa.substring(indice + 'monto total en dolares:'.length);
                  valorMatch = depoisDoisPontos.match(/([\d.,]+)/);
                }
              }
              
              // Patrón 6: Búsqueda directa en la línea original (caso tenga formateo especial)
              if (!valorMatch) {
                // Buscar después de "dolares:" cualquier cosa hasta encontrar número
                const matchDolares = linha.match(/dolares[:\s]*[^\d]*([\d.,]+)/i);
                if (matchDolares) {
                  valorMatch = matchDolares;
                }
              }
              
              if (valorMatch) {
                Logger.log('Valor encontrado en la línea ' + (i + 1) + ': ' + valorMatch[1]);
                break;
              } else {
                Logger.log('Ningún patrón de valor encontrado en la línea: ' + linha);
              }
            }
          }
          
          // Si no encontró línea por línea, intenta en el cuerpo completo (removiendo asteriscos)
          if (!valorMatch) {
            // Remover asteriscos del cuerpo para búsqueda
            const bodyLimpo = body.replace(/\*/g, '');
            
            // Patrón 1: "Monto total en dolares: USD U$S1.072,87" (sin espacio)
            valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
            
            // Patrón 2: "Monto total en dolares: USD U$S 1.072,87" (con espacio)
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
            }
            
            // Patrón 3: Cualquier cosa después de "Monto total en dolares:" hasta encontrar número
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
            }
            
            // Patrón 4: Búsqueda directa después de "dolares:"
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
            
            // Convertir valor a número
            // Formato esperado: 1.072,87 (punto como mil, coma como decimal)
            // O: 1,072.87 (coma como mil, punto como decimal)
            let valorLimpo = valorExtraido;
            
            // Detectar formato: si tiene coma y punto, verificar cuál es decimal
            if (valorLimpo.includes(',') && valorLimpo.includes('.')) {
              // Si coma viene después del punto, coma es decimal (ej: 1.072,87)
              if (valorLimpo.indexOf(',') > valorLimpo.indexOf('.')) {
                valorLimpo = valorLimpo.replace(/\./g, '').replace(',', '.');
              } else {
                // Si punto viene después de la coma, punto es decimal (ej: 1,072.87)
                valorLimpo = valorLimpo.replace(/,/g, '');
              }
            } else if (valorLimpo.includes(',')) {
              // Solo tiene coma - puede ser decimal o mil
              // Si tiene más de 3 dígitos antes de la coma, es mil
              const partes = valorLimpo.split(',');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/,/g, '');
              } else {
                valorLimpo = valorLimpo.replace(',', '.');
              }
            } else if (valorLimpo.includes('.')) {
              // Solo tiene punto - puede ser decimal o mil
              // Si tiene más de 3 dígitos antes del punto, es mil
              const partes = valorLimpo.split('.');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/\./g, '');
              }
            }
            
            valorNumerico = parseFloat(valorLimpo);
            
            if (isNaN(valorNumerico)) {
              erroProcessamento = true;
              mensagemErro = 'Error al convertir valor numérico: ' + valorExtraido;
            } else {
              Logger.log('Valor extraído: ' + valorExtraido + ' -> ' + valorNumerico);
            }
          } else {
            erroProcessamento = true;
            mensagemErro = 'Valor no encontrado en el email';
            
            // Log detallado para depuración
            Logger.log('Valor no encontrado. Buscando línea con "Monto total en dolares"...');
            const linhas = body.split('\n');
            for (let i = 0; i < linhas.length; i++) {
              if (linhas[i].toLowerCase().includes('monto total en dolares')) {
                Logger.log('Línea encontrada (' + (i + 1) + '): ' + linhas[i]);
                // Mostrar también las líneas próximas
                for (let j = Math.max(0, i - 1); j <= Math.min(linhas.length - 1, i + 2); j++) {
                  Logger.log('  Línea ' + (j + 1) + ': ' + linhas[j]);
                }
                break;
              }
            }
            Logger.log('Cuerpo del email (primeros 1000 chars): ' + body.substring(0, 1000));
          }
          
          // Extraer el enlace "Aprobar" del cuerpo del email (usar HTML original para enlaces)
          const linkAprobar = extrairLinkAprobar(body, htmlBody);
          
          if (!linkAprobar) {
            if (!erroProcessamento) {
              erroProcessamento = true;
              mensagemErro = 'Enlace de aprobación no encontrado';
            }
          }
          
          // Preparar datos para inserción
          const rowData = [
            subject,
            date,
            valor,
            linkAprobar || '',
            messageId,
            ''
          ];
          
          // Decidir en qué hoja insertar basado en las reglas
          let sheetDestino = null;
          let status = '';
          let deveAprovar = false;
          
          if (erroProcessamento) {
            // Error en el procesamiento -> hoja "No Aprobados"
            sheetDestino = sheetNaoAprovados;
            status = 'Error: ' + mensagemErro;
            rowData[5] = status;
            Logger.log('Email con error, insertando en "No Aprobados": ' + subject);
          } else if (valorNumerico >= VALOR_LIMITE_APROVACAO) {
            // Valor >= 1000 -> hoja "No Aprobados Valor"
            sheetDestino = sheetNaoAprovadosValor;
            status = 'Valor por encima del límite (USD ' + valorNumerico + ' >= ' + VALOR_LIMITE_APROVACAO + ')';
            rowData[5] = status;
            Logger.log('Email con valor por encima del límite, insertando en "No Aprobados Valor": ' + subject);
          } else {
            // Valor < 1000 y sin error -> hoja "aprovados"
            sheetDestino = sheetAprovados;
            status = 'Procesado - Esperando aprobación';
            rowData[5] = status;
            deveAprovar = true;
            Logger.log('Email aprobado, insertando en "aprovados": ' + subject);
          }
          
          // Para Aprovados e No Aprobados, incluir login de quem executou o robô (coluna G)
          if (sheetDestino === sheetAprovados || sheetDestino === sheetNaoAprovados) {
            rowData.push(obterLoginRede());
          }
          
          // Insertar datos en la hoja apropiada
          sheetDestino.appendRow(rowData);
          
          // Intentar aprobar automáticamente si valor < 1000 y enlace disponible
          if (deveAprovar && linkAprobar) {
            try {
              Logger.log('Intentando aprobar automáticamente: ' + linkAprobar);
              
              // Primero intenta GET (método más común para enlaces de aprobación)
              let response = UrlFetchApp.fetch(linkAprobar, {
                'method': 'get',
                'followRedirects': true,
                'muteHttpExceptions': true,
                'headers': {
                  'User-Agent': 'Mozilla/5.0 (compatible; GoogleAppsScript)'
                }
              });
              
              const statusCode = response.getResponseCode();
              
              // Si GET no funcionó (código diferente de 200), intenta POST
              if (statusCode !== 200) {
                Logger.log('GET retornó código ' + statusCode + ', intentando POST...');
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
              
              // Obtener la última línea después de insertar los datos
              const ultimaLinha = sheetAprovados.getLastRow();
              const finalStatusCode = response.getResponseCode();
              
              if (finalStatusCode === 200 || finalStatusCode === 201 || finalStatusCode === 302) {
                // Actualizar estado en la hoja de cálculo
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Aprobado automáticamente');
                Logger.log('Aprobado automáticamente con éxito! Código: ' + finalStatusCode);
              } else {
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Error en la aprobación: código ' + finalStatusCode);
                Logger.log('Error al aprobar: código ' + finalStatusCode + '. Respuesta: ' + response.getContentText().substring(0, 200));
              }
              
              // Pequeño retraso para evitar muchas solicitudes
              Utilities.sleep(500);
              
            } catch (error) {
              const ultimaLinha = sheetAprovados.getLastRow();
              sheetAprovados.getRange(ultimaLinha, 6).setValue('Error en la aprobación: ' + error.toString());
              Logger.log('Error al aprobar enlace: ' + linkAprobar + ' - ' + error.toString());
            }
          }
          
          threadProcessado = true;
          
        } catch (error) {
          // En caso de error inesperado, insertar en la hoja "No Aprobados"
          try {
            const subject = message.getSubject();
            const date = message.getDate();
            const messageId = message.getId();
            
            const rowData = [
              subject,
              date,
              'Error en la extracción',
              '',
              messageId,
              'Error inesperado: ' + error.toString(),
              obterLoginRede()
            ];
            
            sheetNaoAprovados.appendRow(rowData);
            Logger.log('Error inesperado al procesar email, insertado en "No Aprobados": ' + error.toString());
          } catch (erroInserir) {
            Logger.log('Error crítico al insertar email con error: ' + erroInserir.toString());
          }
        }
        
        // No marcar como leído si está archivado (ya fue procesado por el filtro de Gmail)
        // Los emails archivados ya fueron procesados y no necesitan ser marcados como leídos
        // message.markRead();
        // Logger.log('Email marcado como leído: ' + message.getSubject());
      });
      
      // Nota: Ya no se aplica etiqueta - la duplicación se controla por messageId en las planillas
    });
    
    Logger.log('Procesamiento concluido!');
    
    // Enviar email de alerta con el número de casos en "No Aprobados Valor"
    try {
      enviarEmailAlerta(spreadsheet);
    } catch (errorAlerta) {
      Logger.log('Error al enviar email de alerta: ' + errorAlerta.toString());
    }
    
  } catch (error) {
    Logger.log('Error al procesar emails: ' + error.toString());
    throw error;
  }
}

/**
 * Cuenta los casos en la hoja "No Aprobados Valor"
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 * @return {number} Número de casos (excluyendo encabezado)
 */
function contarCasosNoAprobadosValor(spreadsheet) {
  try {
    const sheet = spreadsheet.getSheetByName(SHEET_NAO_APROVADOS_VALOR);
    if (!sheet) {
      Logger.log('Hoja "No Aprobados Valor" no encontrada');
      return 0;
    }
    
    const lastRow = sheet.getLastRow();
    // Restar 1 para excluir el encabezado
    const totalCasos = lastRow > 1 ? lastRow - 1 : 0;
    
    Logger.log('Total de casos en "No Aprobados Valor": ' + totalCasos);
    return totalCasos;
  } catch (error) {
    Logger.log('Error al contar casos en "No Aprobados Valor": ' + error.toString());
    return 0;
  }
}

/**
 * Envía un email de alerta con el número de casos en "No Aprobados Valor"
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 */
function enviarEmailAlerta(spreadsheet) {
  try {
    const totalCasos = contarCasosNoAprobadosValor(spreadsheet);
    
    const subject = 'Alerta: Casos pendientes de aprobación - No Aprobados Valor';
    const body = 'Hola,\n\n' +
                'Se ha completado la ejecución del procesamiento de emails de aprobación de regalos.\n\n' +
                'Total de casos en la hoja "No Aprobados Valor": ' + totalCasos + '\n\n' +
                'Estos casos requieren revisión manual debido a que el valor excede el límite configurado.\n\n' +
                'Puedes revisar la planilla en: https://docs.google.com/spreadsheets/d/' + SPREADSHEET_ID + '/edit\n\n' +
                'Saludos,\n' +
                'Sistema de Aprobación Automática';
    
    MailApp.sendEmail({
      to: EMAIL_ALERTA,
      subject: subject,
      body: body
    });
    
    Logger.log('Email de alerta enviado a ' + EMAIL_ALERTA + ' con ' + totalCasos + ' casos');
  } catch (error) {
    Logger.log('Error al enviar email de alerta: ' + error.toString());
  }
}

/**
 * Extrae el enlace "Aprobar" del cuerpo del email
 * @param {string} plainBody - Cuerpo del email en texto plano
 * @param {string} htmlBody - Cuerpo del email en HTML
 * @return {string} URL del enlace Aprobar o cadena vacía
 */
function extrairLinkAprobar(plainBody, htmlBody) {
  try {
    // Intentar extraer del HTML primero (más preciso)
    if (htmlBody) {
      // Buscar enlaces que contengan "Aprobar" en el texto
      const htmlMatch = htmlBody.match(/<a[^>]*>.*?Aprobar.*?<\/a>/i);
      if (htmlMatch) {
        const linkMatch = htmlMatch[0].match(/href=["']([^"']+)["']/i);
        if (linkMatch) {
          return linkMatch[1];
        }
      }
      
      // Buscar cualquier enlace que contenga "aprobar" en la URL
      const urlMatch = htmlBody.match(/href=["']([^"']*aprobar[^"']*)["']/i);
      if (urlMatch) {
        return urlMatch[1];
      }
    }
    
    // Intentar extraer del texto plano (menos preciso)
    if (plainBody) {
      // Buscar URLs próximas a la palabra "Aprobar"
      const lines = plainBody.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes('aprobar')) {
          // Buscar URL en la misma línea o próxima
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
    Logger.log('Error al extraer enlace Aprobar: ' + error.toString());
    return '';
  }
}

/**
 * Verifica si el email ya fue procesado en cualquier hoja
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 * @param {string} messageId - ID del email
 * @return {boolean} true si ya fue procesado
 */
function emailJaProcessadoEmQualquerAba(spreadsheet, messageId) {
  try {
    const abas = [SHEET_NAME, SHEET_NAO_APROVADOS, SHEET_NAO_APROVADOS_VALOR];
    
    for (let i = 0; i < abas.length; i++) {
      const sheet = spreadsheet.getSheetByName(abas[i]);
      if (sheet) {
        const data = sheet.getDataRange().getValues();
        
        // La columna E (índice 4) contiene el ID del email
        for (let j = 1; j < data.length; j++) { // Comenzar del índice 1 para saltar encabezado
          if (data[j][4] === messageId) {
            return true;
          }
        }
      }
    }
    
    return false;
  } catch (error) {
    Logger.log('Error al verificar email procesado: ' + error.toString());
    return false;
  }
}

/**
 * Obtiene o crea una hoja en la hoja de cálculo
 * @param {Spreadsheet} spreadsheet - Hoja de cálculo
 * @param {string} sheetName - Nombre de la hoja
 * @return {Sheet} Hoja de la planilla
 */
function obterOuCriarAba(spreadsheet, sheetName) {
  try {
    let sheet = spreadsheet.getSheetByName(sheetName);
    // Aprovados e No Aprobados têm coluna G (Login de quem executou o robô)
    const comColunaLogin = (sheetName === SHEET_NAME || sheetName === SHEET_NAO_APROVADOS);
    const cabecalhos = comColunaLogin
      ? ['Título', 'Fecha/Hora Recepción', 'Valor (USD)', 'Enlace Aprobar', 'ID Email', 'Estado', 'Login (quien ejecutó)']
      : ['Título', 'Fecha/Hora Recepción', 'Valor (USD)', 'Enlace Aprobar', 'ID Email', 'Estado'];
    
    if (!sheet) {
      // Crear nueva hoja
      sheet = spreadsheet.insertSheet(sheetName);
      // Agregar encabezados
      sheet.appendRow(cabecalhos);
      Logger.log('Hoja creada: ' + sheetName);
    } else {
      // Verificar si la hoja ya tiene encabezado
      const primeiraLinha = sheet.getRange(1, 1, 1, cabecalhos.length).getValues()[0];
      const temCabecalho = primeiraLinha[0] === cabecalhos[0] && 
                          primeiraLinha[1] === cabecalhos[1] && 
                          primeiraLinha[2] === cabecalhos[2];
      
      if (!temCabecalho) {
        // Si no tiene encabezado, insertar en la primera línea
        sheet.insertRowBefore(1);
        sheet.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);
        Logger.log('Encabezado agregado a la hoja: ' + sheetName);
      }
    }
    
    return sheet;
  } catch (error) {
    Logger.log('Error al obtener/crear hoja: ' + sheetName + ' - ' + error.toString());
    throw error;
  }
}

/**
 * Función para aprobar automáticamente usando el enlace extraído
 * Aprueba solo casos con valor < 1000 dólares
 * ATENCIÓN: Use con cuidado - esta función hará solicitudes HTTP para los enlaces
 */
function aprovarAutomaticamente() {
  try {
    let spreadsheet;
    try {
      spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
      if (!spreadsheet) {
        throw new Error('SpreadsheetApp.openById retornó null o undefined');
      }
    } catch (error) {
      Logger.log('Error al abrir la hoja de cálculo: ' + error.toString());
      throw new Error('No se pudo abrir la hoja de cálculo con ID: ' + SPREADSHEET_ID + '. Error: ' + error.toString());
    }
    
    // Obtener el valor límite de aprobación desde la hoja de configuración
    const VALOR_LIMITE_APROVACAO = obterValorLimiteAprovacao(spreadsheet);
    Logger.log('Valor límite de aprobación configurado: USD ' + VALOR_LIMITE_APROVACAO);
    
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      Logger.log('Hoja "aprovados" no encontrada.');
      return;
    }
    
    const data = sheet.getDataRange().getValues();
    
    // Procesar líneas que tienen enlace pero estado no es "Aprobado"
    for (let i = 1; i < data.length; i++) {
      const valorTexto = data[i][2]; // Columna C (índice 2) - Valor
      const linkAprobar = data[i][3]; // Columna D (índice 3) - Enlace
      const status = data[i][5]; // Columna F (índice 5) - Estado
      
      // Extraer valor numérico
      let valorNumerico = null;
      if (valorTexto && valorTexto.includes('USD')) {
        const valorMatch = valorTexto.match(/([\d.,]+)/);
        if (valorMatch) {
          const valorLimpo = valorMatch[1].replace(/\./g, '').replace(',', '.');
          valorNumerico = parseFloat(valorLimpo);
        }
      }
      
      // Aprobar solo si:
      // - Tiene enlace válido
      // - Estado no es "Aprobado" o "Aprobado automáticamente"
      // - Valor es menor que 1000 (o no fue posible extraer el valor)
      const podeAprovar = linkAprobar && 
                         linkAprobar.startsWith('http') && 
                         status !== 'Aprobado' && 
                         status !== 'Aprobado automáticamente' &&
                         (valorNumerico === null || valorNumerico < VALOR_LIMITE_APROVACAO);
      
      if (podeAprovar) {
        try {
          // Hacer solicitud GET para el enlace
          const response = UrlFetchApp.fetch(linkAprobar, {
            'method': 'get',
            'followRedirects': true,
            'muteHttpExceptions': true
          });
          
          if (response.getResponseCode() === 200) {
            // Actualizar estado en la hoja de cálculo
            sheet.getRange(i + 1, 6).setValue('Aprobado automáticamente');
            Logger.log('Aprobado: ' + linkAprobar);
          } else {
            sheet.getRange(i + 1, 6).setValue('Error en la aprobación: código ' + response.getResponseCode());
            Logger.log('Error al aprobar: código ' + response.getResponseCode());
          }
          
          // Pequeño retraso para evitar muchas solicitudes
          Utilities.sleep(1000);
          
        } catch (error) {
          Logger.log('Error al aprobar enlace: ' + linkAprobar + ' - ' + error.toString());
          sheet.getRange(i + 1, 6).setValue('Error: ' + error.toString());
        }
      } else if (valorNumerico !== null && valorNumerico >= VALOR_LIMITE_APROVACAO) {
        Logger.log('Saltando aprobación - valor por encima del límite: USD ' + valorNumerico);
      }
    }
    
    Logger.log('Proceso de aprobación automática concluido.');
    
  } catch (error) {
    Logger.log('Error en la aprobación automática: ' + error.toString());
    throw error;
  }
}

/**
 * Obtiene o crea la etiqueta especificada
 * @param {string} labelName - Nombre de la etiqueta
 * @return {GmailLabel} Objeto de la etiqueta
 */
function obterOuCriarLabel(labelName) {
  try {
    // Intentar obtener la etiqueta existente
    let label = GmailApp.getUserLabelByName(labelName);
    
    // Si no existe, crear
    if (!label) {
      label = GmailApp.createLabel(labelName);
      Logger.log('Etiqueta creada: ' + labelName);
    } else {
      Logger.log('Etiqueta encontrada: ' + labelName);
    }
    
    return label;
  } catch (error) {
    Logger.log('Error al obtener/crear etiqueta: ' + error.toString());
    throw error;
  }
}

/**
 * Función para crear un activador que se ejecuta automáticamente
 * Puede ser configurado para ejecutarse periódicamente (ej: cada hora)
 */
function criarTrigger() {
  // Eliminar activadores existentes para evitar duplicados
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'processarEmailsAprovacao') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Crear nuevo activador para ejecutar cada hora
  ScriptApp.newTrigger('processarEmailsAprovacao')
    .timeBased()
    .everyHours(1)
    .create();
  
  Logger.log('Activador creado con éxito! El script se ejecutará automáticamente cada hora.');
}

/**
 * Función de prueba para verificar permisos y acceso a la hoja de cálculo
 * Ejecuta esta función manualmente para diagnosticar problemas de permisos
 */
function verificarPermisos() {
  try {
    Logger.log('=== Verificación de Permisos ===');
    Logger.log('ID de la hoja de cálculo: ' + SPREADSHEET_ID);
    
    // Verificar acceso a la planilla
    try {
      const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
      const nombre = spreadsheet.getName();
      const url = spreadsheet.getUrl();
      
      Logger.log('✓ Acceso exitoso a la hoja de cálculo');
      Logger.log('  Nombre: ' + nombre);
      Logger.log('  URL: ' + url);
      
      // Verificar acceso a las hojas
      const hojas = ['aprovados', 'No Aprobados', 'No Aprobados Valor', 'Config'];
      hojas.forEach(function(nombreHoja) {
        try {
          let sheet = spreadsheet.getSheetByName(nombreHoja);
          if (sheet) {
            Logger.log('✓ Hoja "' + nombreHoja + '" encontrada');
          } else {
            Logger.log('⚠ Hoja "' + nombreHoja + '" no existe (se creará automáticamente)');
          }
        } catch (error) {
          Logger.log('✗ Error al acceder a la hoja "' + nombreHoja + '": ' + error.toString());
        }
      });
      
      // Intentar escribir en una hoja de prueba
      try {
        let testSheet = spreadsheet.getSheetByName('aprovados');
        if (!testSheet) {
          testSheet = spreadsheet.insertSheet('aprovados');
        }
        const ultimaFila = testSheet.getLastRow();
        Logger.log('✓ Permisos de lectura/escritura verificados (última fila: ' + ultimaFila + ')');
      } catch (error) {
        Logger.log('✗ Error al verificar permisos de escritura: ' + error.toString());
      }
      
    } catch (error) {
      Logger.log('✗ ERROR: No se puede acceder a la hoja de cálculo');
      Logger.log('  Detalles: ' + error.toString());
      Logger.log('');
      Logger.log('SOLUCIONES:');
      Logger.log('1. Verifica que el ID de la hoja de cálculo sea correcto');
      Logger.log('2. Comparte la hoja de cálculo con la cuenta que ejecuta el script');
      Logger.log('3. Asegúrate de tener permisos de "Editor" en la hoja de cálculo');
      Logger.log('4. El ID debe ser el que aparece en la URL:');
      Logger.log('   https://docs.google.com/spreadsheets/d/[ID_AQUI]/edit');
      return;
    }
    
    // Verificar acceso a Gmail
    try {
      const threads = GmailApp.search('in:inbox', 0, 1);
      Logger.log('✓ Acceso a Gmail verificado');
    } catch (error) {
      Logger.log('✗ Error al acceder a Gmail: ' + error.toString());
    }
    
    Logger.log('=== Verificación Completada ===');
    
  } catch (error) {
    Logger.log('Error en la verificación: ' + error.toString());
  }
}

/**
 * Función para procesar emails con un valor límite dinámico (usada por la interfaz)
 * @param {number} valorLimite - Valor límite de aprobación en dólares
 * @return {Object} Objeto con resultado y estadísticas
 */
function processarEmailsComValorLimite(valorLimite) {
  try {
    // Validar valor límite
    if (isNaN(valorLimite) || valorLimite < 0) {
      return {
        success: false,
        message: 'El valor límite debe ser un número mayor o igual a cero.'
      };
    }
    
    // Buscar emails que:
    // - Tienen la etiqueta "Pagos"
    // - Contienen "Nuevo regalo" en el asunto
    // - NO contienen "Aprobada" en el asunto (excluir aprobaciones ya procesadas)
    // - Son de los últimos 5 días
    // Nota: La duplicación se controla verificando el messageId en las planillas
    // Nota: Se procesan todos los emails (leídos y no leídos)
    const query = 'label:Pagos subject:Nuevo regalo -subject:"Aprobada" newer_than:5d';
    const threads = GmailApp.search(query, 0, 50);
    
    if (threads.length === 0) {
      // Enviar email de alerta incluso si no hay emails nuevos
      try {
        const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
        enviarEmailAlerta(spreadsheet);
      } catch (errorAlerta) {
        Logger.log('Error al enviar email de alerta: ' + errorAlerta.toString());
      }
      
      return {
        success: true,
        message: 'No se encontraron emails con la etiqueta "Pagos" y asunto "Nuevo regalo" de los últimos 5 días, o todos ya fueron procesados.',
        estatisticas: {
          total: 0,
          aprovados: 0,
          naoAprovadosValor: 0,
          naoAprovadosErro: 0
        }
      };
    }
    
    Logger.log('Se encontraron ' + threads.length + ' hilos de email con la etiqueta "Pagos" para procesar.');
    
    // Abrir la hoja de cálculo
    let spreadsheet;
    try {
      spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    } catch (error) {
      return {
        success: false,
        message: 'Error al acceder a la hoja de cálculo: ' + error.toString()
      };
    }
    
    // Obtener o crear todas las hojas necesarias
    const sheetAprovados = obterOuCriarAba(spreadsheet, SHEET_NAME);
    const sheetNaoAprovados = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS);
    const sheetNaoAprovadosValor = obterOuCriarAba(spreadsheet, SHEET_NAO_APROVADOS_VALOR);
    
    // Contadores de estadísticas
    let totalProcessados = 0;
    let aprovados = 0;
    let naoAprovadosValor = 0;
    let naoAprovadosErro = 0;
    
    // Procesar cada hilo de email
    threads.forEach(function(thread) {
      const messages = thread.getMessages();
      
      let threadProcessado = false;
      
      messages.forEach(function(message) {
        try {
          const messageId = message.getId();
          
          // Verificar si el email tiene la etiqueta "Pagos" y está archivado
          const messageLabels = message.getThread().getLabels();
          let tieneEtiquetaPagos = false;
          for (let j = 0; j < messageLabels.length; j++) {
            if (messageLabels[j].getName() === 'Pagos') {
              tieneEtiquetaPagos = true;
              break;
            }
          }
          
          if (!tieneEtiquetaPagos) {
            return;
          }
          
          const subject = message.getSubject();
          if (!subject.toLowerCase().includes('nuevo regalo')) {
            return;
          }
          
          if (emailJaProcessadoEmQualquerAba(spreadsheet, messageId)) {
            return;
          }
          
          const date = message.getDate();
          const plainBody = message.getPlainBody() || '';
          const htmlBody = message.getBody() || '';
          
          let bodyText = plainBody;
          if (htmlBody) {
            const htmlText = htmlBody.replace(/<[^>]+>/g, ' ')
                                     .replace(/&nbsp;/g, ' ')
                                     .replace(/&amp;/g, '&')
                                     .replace(/&lt;/g, '<')
                                     .replace(/&gt;/g, '>')
                                     .replace(/&quot;/g, '"')
                                     .replace(/\s+/g, ' ')
                                     .trim();
            
            if (htmlText && htmlText.length > plainBody.length) {
              bodyText = plainBody + '\n' + htmlText;
            }
          }
          
          const body = bodyText;
          let valorMatch = null;
          const linhas = body.split(/\r?\n/);
          
          for (let i = 0; i < linhas.length; i++) {
            const linha = linhas[i].trim();
            
            if (linha.toLowerCase().includes('monto total en dolares')) {
              const linhaLimpa = linha.replace(/\*/g, '').replace(/_/g, '').replace(/`/g, '').trim();
              
              valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
              }
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:\s*USD\s+([\d.,]+)/i);
              }
              if (!valorMatch) {
                valorMatch = linhaLimpa.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
              }
              if (!valorMatch) {
                const indice = linhaLimpa.toLowerCase().indexOf('monto total en dolares:');
                if (indice !== -1) {
                  const depoisDoisPontos = linhaLimpa.substring(indice + 'monto total en dolares:'.length);
                  valorMatch = depoisDoisPontos.match(/([\d.,]+)/);
                }
              }
              if (!valorMatch) {
                const matchDolares = linha.match(/dolares[:\s]*[^\d]*([\d.,]+)/i);
                if (matchDolares) {
                  valorMatch = matchDolares;
                }
              }
              
              if (valorMatch) {
                break;
              }
            }
          }
          
          if (!valorMatch) {
            const bodyLimpo = body.replace(/\*/g, '');
            valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S([\d.,]+)/i);
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:\s*USD\s*U\$S\s+([\d.,]+)/i);
            }
            if (!valorMatch) {
              valorMatch = bodyLimpo.match(/Monto\s+total\s+en\s+dolares:[^\d]*([\d.,]+)/i);
            }
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
            
            let valorLimpo = valorExtraido;
            if (valorLimpo.includes(',') && valorLimpo.includes('.')) {
              if (valorLimpo.indexOf(',') > valorLimpo.indexOf('.')) {
                valorLimpo = valorLimpo.replace(/\./g, '').replace(',', '.');
              } else {
                valorLimpo = valorLimpo.replace(/,/g, '');
              }
            } else if (valorLimpo.includes(',')) {
              const partes = valorLimpo.split(',');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/,/g, '');
              } else {
                valorLimpo = valorLimpo.replace(',', '.');
              }
            } else if (valorLimpo.includes('.')) {
              const partes = valorLimpo.split('.');
              if (partes[0].length > 3) {
                valorLimpo = valorLimpo.replace(/\./g, '');
              }
            }
            
            valorNumerico = parseFloat(valorLimpo);
            
            if (isNaN(valorNumerico)) {
              erroProcessamento = true;
              mensagemErro = 'Error al convertir valor numérico: ' + valorExtraido;
            }
          } else {
            erroProcessamento = true;
            mensagemErro = 'Valor no encontrado en el email';
          }
          
          const linkAprobar = extrairLinkAprobar(body, htmlBody);
          
          if (!linkAprobar && !erroProcessamento) {
            erroProcessamento = true;
            mensagemErro = 'Enlace de aprobación no encontrado';
          }
          
          const rowData = [
            subject,
            date,
            valor,
            linkAprobar || '',
            messageId,
            ''
          ];
          
          let sheetDestino = null;
          let status = '';
          let deveAprovar = false;
          
          if (erroProcessamento) {
            sheetDestino = sheetNaoAprovados;
            status = 'Error: ' + mensagemErro;
            rowData[5] = status;
            naoAprovadosErro++;
          } else if (valorNumerico >= valorLimite) {
            sheetDestino = sheetNaoAprovadosValor;
            status = 'Valor por encima del límite (USD ' + valorNumerico + ' >= ' + valorLimite + ')';
            rowData[5] = status;
            naoAprovadosValor++;
          } else {
            sheetDestino = sheetAprovados;
            status = 'Procesado - Esperando aprobación';
            rowData[5] = status;
            deveAprovar = true;
            aprovados++;
          }
          
          // Para Aprovados e No Aprobados, incluir login de quem ejecutó el robot (columna G)
          if (sheetDestino === sheetAprovados || sheetDestino === sheetNaoAprovados) {
            rowData.push(obterLoginRede());
          }
          
          sheetDestino.appendRow(rowData);
          totalProcessados++;
          
          if (deveAprovar && linkAprobar) {
            try {
              let response = UrlFetchApp.fetch(linkAprobar, {
                'method': 'get',
                'followRedirects': true,
                'muteHttpExceptions': true,
                'headers': {
                  'User-Agent': 'Mozilla/5.0 (compatible; GoogleAppsScript)'
                }
              });
              
              const statusCode = response.getResponseCode();
              
              if (statusCode !== 200) {
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
              
              const ultimaLinha = sheetAprovados.getLastRow();
              const finalStatusCode = response.getResponseCode();
              
              if (finalStatusCode === 200 || finalStatusCode === 201 || finalStatusCode === 302) {
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Aprobado automáticamente');
              } else {
                sheetAprovados.getRange(ultimaLinha, 6).setValue('Error en la aprobación: código ' + finalStatusCode);
              }
              
              Utilities.sleep(500);
              
            } catch (error) {
              const ultimaLinha = sheetAprovados.getLastRow();
              sheetAprovados.getRange(ultimaLinha, 6).setValue('Error en la aprobación: ' + error.toString());
            }
          }
          
          // No marcar como leído si está archivado (ya fue procesado)
          // message.markRead();
          threadProcessado = true;
          
        } catch (error) {
          try {
            const subject = message.getSubject();
            const date = message.getDate();
            const messageId = message.getId();
            
            const rowData = [
              subject,
              date,
              'Error en la extracción',
              '',
              messageId,
              'Error inesperado: ' + error.toString(),
              obterLoginRede()
            ];
            
            sheetNaoAprovados.appendRow(rowData);
            naoAprovadosErro++;
            totalProcessados++;
          } catch (erroInserir) {
            Logger.log('Error crítico al insertar email con error: ' + erroInserir.toString());
          }
        }
      });
      
      // Nota: Ya no se aplica etiqueta - la duplicación se controla por messageId en las planillas
    });
    
    // Enviar email de alerta con el número de casos en "No Aprobados Valor"
    try {
      enviarEmailAlerta(spreadsheet);
    } catch (errorAlerta) {
      Logger.log('Error al enviar email de alerta: ' + errorAlerta.toString());
    }
    
    return {
      success: true,
      message: 'Procesamiento completado. ' + totalProcessados + ' email(s) procesado(s).',
      estatisticas: {
        total: totalProcessados,
        aprovados: aprovados,
        naoAprovadosValor: naoAprovadosValor,
        naoAprovadosErro: naoAprovadosErro
      }
    };
    
  } catch (error) {
    return {
      success: false,
      message: 'Error al procesar emails: ' + error.toString()
    };
  }
}

