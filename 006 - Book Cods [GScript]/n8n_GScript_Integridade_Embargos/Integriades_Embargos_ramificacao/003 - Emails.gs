/**
 * Script para exportar relatórios.
 * RAMIFICAÇÃO: Inclui abas consolidadas (CRUCE_1 a 4_CONSOLIDADO com coluna Fonte).
 * As abas individuais CRUCE_1/1_2, 2/2_2, 3/3_2, 4/4_2 estão ocultas no Sheets.
 */
function exportarRelatoriosCrucePorEmail() {
  const SPREADSHEET_ID_ORIGEM = "1hrKq2U9y7LuTZqiIpmizk4j72FTyweZcnZShawPDhgY";

  const SHEET_NAMES_TO_EXPORT = [
    "RESUMO",
    "CRUCE_1_CONSOLIDADO",
    "CRUCE_2_CONSOLIDADO",
    "CRUCE_3_CONSOLIDADO",
    "CRUCE_4_CONSOLIDADO",
    "CRUCE_5_TESTE_CBU",
    "CRUCE_6_DUPLICADOS",
    "CRUCE_7_DEBT_TYPE_INCORRETO",
    "RESUMO_2"
  ];

  const LABEL_MAP = {
    "CRUCE_1_CONSOLIDADO": "1. Valor transferido > Retido (DISB + Transfer Admin)",
    "CRUCE_2_CONSOLIDADO": "2. Erro no ID da Deuda (DISB + Transfer Admin)",
    "CRUCE_3_CONSOLIDADO": "3. Enlighten não executou (DISB + Transfer Admin)",
    "CRUCE_4_CONSOLIDADO": "4. Valor menor que retido (DISB + Transfer Admin)",
    "CRUCE_5_TESTE_CBU": "5. CBU Inválido (Regra 22 digitos)",
    "CRUCE_6_DUPLICADOS": "6. Casos Duplicados (debt ID + Valor)",
    "CRUCE_7_DEBT_TYPE_INCORRETO": "7. Debt Type Incorreto (Planilha vs BQ)"
  };

  const RECEPTOR_EMAIL = "melissa.pace@mercadolivre.com,ext_angesilv@mercadolivre.com,ext_danillos@mercadolivre.com,felipe.pmisura@mercadolivre.com,valeria.raverta@mercadolibre.com,ext_grmarcan@mercadolivre.com,murillo.franca@mercadolivre.com";
  const ASSUNTO_EMAIL = "Reporte Diário: Cruces de Validação de Retenções";
  const NOME_ARQUIVO_ANEXO = "Relatorio_Cruces_Validacao.xlsx";

  let fileBlob;
  let tempSpreadsheetId = null;
  let summaryCounts = {};

  try {
    const spreadsheetOrigem = SpreadsheetApp.openById(SPREADSHEET_ID_ORIGEM);

    const tempSheetName = "Relatorio Cruces TEMP " + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm");
    const tempSpreadsheet = SpreadsheetApp.create(tempSheetName);
    tempSpreadsheetId = tempSpreadsheet.getId();
    const defaultSheet = tempSpreadsheet.getSheets()[0];

    Logger.log('INFORMAÇÃO: Iniciando processamento...');

    let sheetsCopied = 0;

    SHEET_NAMES_TO_EXPORT.forEach((nomeHoja) => {
      const hojaOrigem = spreadsheetOrigem.getSheetByName(nomeHoja);
      if (!hojaOrigem) return;

      const rangoDatos = hojaOrigem.getDataRange();
      const datos = rangoDatos.getValues();

      if (nomeHoja !== "RESUMO" && nomeHoja !== "RESUMO_2") {
        let qtd = 0;
        if (datos.length > 1) {
          const primeiraCelulaDados = String(datos[1][0]).trim();
          if (primeiraCelulaDados === "Nenhum caso encontrado") {
            qtd = 0;
          } else {
            qtd = datos.length - 1;
          }
        }
        summaryCounts[nomeHoja] = qtd;
      }

      const hojaDestino = tempSpreadsheet.insertSheet(nomeHoja);
      sheetsCopied++;

      if (datos.length > 0) {
        hojaDestino.getRange(1, 1, datos.length, datos[0].length).setValues(datos);
      }
    });

    if (sheetsCopied > 0) {
      if (tempSpreadsheet.getSheets().length > 1) {
        tempSpreadsheet.deleteSheet(defaultSheet);
      }

      // Limpar CRUCE 4 da aba RESUMO (não enviar no primeiro bloco)
      const abaResumoTemp = tempSpreadsheet.getSheetByName("RESUMO");
      if (abaResumoTemp) {
        const dadosResumo = abaResumoTemp.getDataRange().getValues();
        for (let i = dadosResumo.length - 1; i >= 0; i--) {
          const valorCelulaA = String(dadosResumo[i][0]);
          if (valorCelulaA.includes("CRUCE_4_VALOR_MENOR_QUE_RETIDO")) {
            abaResumoTemp.deleteRow(i + 1);
          }
        }
      }

      SpreadsheetApp.flush();

      // Tabela: Cruces (inclui consolidados 1–4 + 5, 6, 7)
      const ordemExibicao = [
        "CRUCE_1_CONSOLIDADO",
        "CRUCE_2_CONSOLIDADO",
        "CRUCE_3_CONSOLIDADO",
        "CRUCE_4_CONSOLIDADO",
        "CRUCE_5_TESTE_CBU",
        "CRUCE_6_DUPLICADOS",
        "CRUCE_7_DEBT_TYPE_INCORRETO"
      ];

      let linhasTabelaHtml = "";
      ordemExibicao.forEach(key => {
        const label = LABEL_MAP[key];
        const qtd = summaryCounts[key] || 0;
        const estiloQtd = qtd > 0 ? "color: #D32F2F;" : "color: #333;";
        linhasTabelaHtml += `
          <tr>
            <td style="padding: 12px; border-bottom: 1px solid #eee; color: #333;">${label}</td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; text-align: right; font-weight: bold; ${estiloQtd}">${qtd}</td>
          </tr>
        `;
      });

      const TEXTO_EMAIL_HTML = `
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px 0;">
            <tr>
              <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                  <tr>
                    <td style="background: linear-gradient(135deg, #FFE600 0%, #FFF159 100%); padding: 30px 40px; text-align: center;">
                      <h1 style="margin: 0; color: #333333; font-size: 24px; font-weight: 600;">RELATÓRIO DIÁRIO</h1>
                      <p style="margin: 8px 0 0 0; color: #666666; font-size: 14px; font-weight: 500;">Cruces de Validação de Retenções</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 40px 40px 30px 40px;">
                      <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px;"><strong>Olá!</strong></p>
                      <p style="margin: 0 0 20px 0; color: #333333; font-size: 15px; line-height: 1.6;">
                        Segue abaixo o resumo dos casos identificados hoje. O detalhe completo encontra-se no arquivo anexo.
                        Cruces 1 a 4 incluem dados de DISB_DEBT e Transfer Admin na mesma aba (coluna Fonte).
                      </p>
                      <p style="margin: 16px 0 8px 0; color: #666; font-size: 14px; font-weight: 600;">Cruces (consolidados + demais)</p>
                      <table width="100%" cellpadding="0" cellspacing="0" style="margin: 20px 0; border: 1px solid #eee; border-radius: 6px; overflow: hidden;">
                        <thead>
                          <tr style="background-color: #f9f9f9;">
                            <th style="padding: 12px; text-align: left; color: #666; font-size: 13px; text-transform: uppercase;">Cruce</th>
                            <th style="padding: 12px; text-align: right; color: #666; font-size: 13px; text-transform: uppercase;">Quantidade</th>
                          </tr>
                        </thead>
                        <tbody>
                          ${linhasTabelaHtml}
                        </tbody>
                      </table>
                      <p style="margin: 20px 0 10px 0; color: #333333; font-size: 16px; font-weight: 600;">Obrigado!</p>
                      <p style="margin: 0; color: #3483FA; font-size: 15px; font-weight: 500;">Legal Ops Automation</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="background-color: #2D3277; padding: 15px; text-align: center;">
                      <p style="margin: 0; color: #ffffff; font-size: 12px;">Anexo: Relatório consolidado (.xlsx)</p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
      `;

      const url = tempSpreadsheet.getUrl();
      const exportUrl = url.replace('/edit', '/export') + '?exportFormat=xlsx';

      const params = {
        method: "get",
        headers: { "Authorization": "Bearer " + ScriptApp.getOAuthToken() },
        muteHttpExceptions: true
      };

      fileBlob = UrlFetchApp.fetch(exportUrl, params).getBlob();
      fileBlob.setName(NOME_ARQUIVO_ANEXO);

      MailApp.sendEmail({
        to: RECEPTOR_EMAIL,
        subject: ASSUNTO_EMAIL,
        htmlBody: TEXTO_EMAIL_HTML,
        attachments: [fileBlob]
      });

      Logger.log("SUCESSO: Email enviado para " + RECEPTOR_EMAIL);

    } else {
      Logger.log("ERRO: Nenhuma aba encontrada.");
    }

  } catch (e) {
    Logger.log("ERRO FINAL: " + e.toString());
  } finally {
    if (tempSpreadsheetId) {
      try {
        DriveApp.getFileById(tempSpreadsheetId).setTrashed(true);
      } catch (e) {
        Logger.log("Erro na limpeza: " + e.toString());
      }
    }
  }
}
