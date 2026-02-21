/**
 * Envia um email formatado em HTML para Marcelo Cardoso com quatro planilhas anexadas como XLSX,
 * detalhando o processo (Input, Resultado, Regras e Discrepância).
 */
function enviarEmailProcessamentoDados() {
  const DESTINATARIO = "marcelo.cardoso@mercadolivre.com,ext_alcarjul@mercadolivre.com ";
  const ASSUNTO = "📊 Relatório Apoderados - Brasil";
  
  // Lista de planilhas a serem anexadas
  const planilhasParaAnexar = [
    {
      id: "1Ro5If85-7E--0At8q0SamKsR-mnVlJgwIY5YBRwpKJE",
      nomeArquivo: "01_Base_Input.xlsx",
      rotulo: "Base de Dados (Input)",
      icone: "📥",
      descricao: "Dados originais de entrada"
    },
    {
      id: "1zo6019x58F7YiTbijqpawmbFVWhBs8nhZEjYXyEjqxU",
      nomeArquivo: "02_Base_Resultado.xlsx",
      rotulo: "Resultado do Processamento",
      icone: "✅",
      descricao: "Dados processados e validados"
    },
    {
      id: "1EohsmWblwSVujLowqe1025y4Y3T6sgvs-V6NtPIuRIU",
      nomeArquivo: "03_Base_Regras_Aplicadas.xlsx",
      rotulo: "Base de Regras Utilizadas",
      icone: "📋",
      descricao: "Regras de negócio aplicadas"
    },
    {
      id: "1KV2qcBY99LslheMmKJaLcRAvTPjoWYvdZVXh0-5-fJw",
      nomeArquivo: "04_Analise_Discrepancia.xlsx",
      rotulo: "Análise de Discrepância",
      icone: "🔍",
      descricao: "Inconsistências identificadas"
    }
  ];

  const anexos = [];
  const token = ScriptApp.getOAuthToken();
  const exportFormat = "xlsx";
  const cardsArquivos = [];

  // 1. Processar e obter os anexos (Blob)
  for (const planilha of planilhasParaAnexar) {
    try {
      const exportUrl = `https://docs.google.com/spreadsheets/export?exportFormat=${exportFormat}&id=${planilha.id}`;

      const params = {
        method: "GET",
        headers: {
          "Authorization": "Bearer " + token
        },
        muteHttpExceptions: true
      };

      const response = UrlFetchApp.fetch(exportUrl, params);
      
      if (response.getResponseCode() === 200) {
        const blob = response.getBlob();
        blob.setName(planilha.nomeArquivo);
        anexos.push(blob);
        
        cardsArquivos.push(`
          <div style="background: white; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(45, 50, 119, 0.1); border-left: 4px solid #FFE600;">
            <div style="display: flex; align-items: start; gap: 12px;">
              <div style="font-size: 32px; line-height: 1;">${planilha.icone}</div>
              <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #2D3277; font-size: 16px; font-weight: 600;">${planilha.rotulo}</h3>
                <p style="margin: 0 0 8px 0; color: #666; font-size: 14px;">${planilha.descricao}</p>
                <div style="display: inline-block; background: #F5F5F5; padding: 6px 12px; border-radius: 6px; font-size: 12px; color: #2D3277; font-family: monospace;">
                  📎 ${planilha.nomeArquivo}
                </div>
              </div>
            </div>
          </div>
        `);
        
        Logger.log(`Planilha ${planilha.nomeArquivo} anexada com sucesso.`);
      } else {
        cardsArquivos.push(`
          <div style="background: #FFEBEE; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #F44336;">
            <div style="display: flex; align-items: start; gap: 12px;">
              <div style="font-size: 32px; line-height: 1;">⚠️</div>
              <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #C62828; font-size: 16px; font-weight: 600;">${planilha.rotulo}</h3>
                <p style="margin: 0; color: #D32F2F; font-size: 14px;">Erro ao exportar (${planilha.nomeArquivo})</p>
              </div>
            </div>
          </div>
        `);
        Logger.log(`ERRO ao exportar ${planilha.nomeArquivo}. Código: ${response.getResponseCode()}`);
      }

    } catch (e) {
      cardsArquivos.push(`
        <div style="background: #FFEBEE; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #F44336;">
          <div style="display: flex; align-items: start; gap: 12px;">
            <div style="font-size: 32px; line-height: 1;">❌</div>
            <div style="flex: 1;">
              <h3 style="margin: 0 0 8px 0; color: #C62828; font-size: 16px; font-weight: 600;">${planilha.rotulo}</h3>
              <p style="margin: 0; color: #D32F2F; font-size: 14px;">Erro de execução (${planilha.nomeArquivo})</p>
            </div>
          </div>
        </div>
      `);
      Logger.log(`Exceção ao processar a planilha ${planilha.nomeArquivo}: ${e.toString()}`);
    }
  }

  // 2. Construir o Corpo do Email em HTML com design Mercado Livre
  const htmlBody = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
      </head>
      <body style="margin: 0; padding: 0; background-color: #F5F5F5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        
        <!-- Container Principal -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #F5F5F5; padding: 40px 20px;">
          <tr>
            <td align="center">
              <table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%;">
                
                <!-- Header com cores Mercado Livre -->
                <tr>
                  <td style="background: linear-gradient(135deg, #2D3277 0%, #3D4287 100%); border-radius: 16px 16px 0 0; padding: 40px 32px; text-align: center;">
                    <h1 style="margin: 0; color: #FFE600; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                      📊 Apoderados - Brasil
                    </h1>
                    <p style="margin: 12px 0 0 0; color: #FFFFFF; font-size: 16px; opacity: 0.95;">
                      Dados processados e prontos para análise
                    </p>
                  </td>
                </tr>
                
                <!-- Corpo do Email -->
                <tr>
                  <td style="background: #FFFFFF; padding: 40px 32px;">
                    
                    <p style="margin: 0 0 24px 0; color: #333; font-size: 16px; line-height: 1.6;">
                      Olá <strong style="color: #2D3277;">Marcelo</strong>,
                    </p>
                    
                    <p style="margin: 0 0 32px 0; color: #555; font-size: 15px; line-height: 1.6;">
                      Seguem os arquivos de dados referentes ao último ciclo de processamento. Todos os documentos foram convertidos para o formato <strong>XLSX</strong> e estão anexados neste email.
                    </p>
                    
                    <!-- Banner de Destaque -->
                    <div style="background: linear-gradient(135deg, #FFE600 0%, #FFD700 100%); border-radius: 12px; padding: 24px; margin-bottom: 32px; border: 2px solid #2D3277;">
                      <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="font-size: 48px; line-height: 1;">📦</div>
                        <div>
                          <h2 style="margin: 0 0 8px 0; color: #2D3277; font-size: 20px; font-weight: 700;">
                            ${anexos.length} Arquivos Anexados
                          </h2>
                          <p style="margin: 0; color: #2D3277; font-size: 14px; opacity: 0.8;">
                            Formato XLSX • Prontos para download
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Cards dos Arquivos -->
                    <h2 style="margin: 0 0 20px 0; color: #2D3277; font-size: 20px; font-weight: 700;">
                      📋 Arquivos Incluídos
                    </h2>
                    
                    ${cardsArquivos.join('')}
                    
                    <!-- Mensagem de Rodapé -->
                    <div style="margin-top: 40px; padding-top: 32px; border-top: 2px solid #F0F0F0;">
                      <p style="margin: 0 0 16px 0; color: #555; font-size: 15px; line-height: 1.6;">
                        Permanecemos à disposição para qualquer esclarecimento ou detalhamento sobre as regras aplicadas.
                      </p>
                      <p style="margin: 0; color: #333; font-size: 15px;">
                        Atenciosamente,<br>
                        <strong style="color: #2D3277;">Legal Analytics</strong>
                      </p>
                    </div>
                    
                  </td>
                </tr>
                
                <!-- Footer -->
                <tr>
                  <td style="background: #2D3277; border-radius: 0 0 16px 16px; padding: 24px 32px; text-align: center;">
                    <p style="margin: 0; color: #FFE600; font-size: 13px; font-weight: 600;">
                      Mercado Livre • Legal Analytics
                    </p>
                    <p style="margin: 8px 0 0 0; color: #FFFFFF; font-size: 12px; opacity: 0.7;">
                      Email gerado automaticamente • ${new Date().toLocaleDateString('pt-BR')}
                    </p>
                  </td>
                </tr>
                
              </table>
            </td>
          </tr>
        </table>
        
      </body>
    </html>
  `;
  
  // 3. Enviar o email
  if (anexos.length > 0) {
    try {
      MailApp.sendEmail({
        to: DESTINATARIO,
        subject: ASSUNTO,
        htmlBody: htmlBody,
        attachments: anexos
      });
      Logger.log(`Email enviado com sucesso para ${DESTINATARIO} com ${anexos.length} anexos.`);
    } catch (e) {
      Logger.log(`ERRO FATAL ao enviar o email: ${e.toString()}`);
    }
  } else {
    MailApp.sendEmail({
      to: DESTINATARIO,
      subject: ASSUNTO + " ⚠️ [ERRO NA EXPORTAÇÃO]",
      htmlBody: htmlBody
    });
    Logger.log("Nenhum arquivo anexado com sucesso. Foi enviado um email de aviso.");
  }
}