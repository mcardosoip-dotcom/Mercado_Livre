// === CONFIGURAÇÕES ===
const SHEET_ID = '1kJN18L_Kmt4YqLzpq8-jbBZLDKN1WtQRWJCbY_FW8ww';
const SHEET_SOLICITACOES = 'Solicitações - Esteira';
const SHEET_NOVAS = 'Solicitações - Novas';
const SHEET_MAPPINGS = 'Mappings';
const SHEET_EMAILS = 'Dimensão'; // Adicionada constante para aba de e-mails
const DRIVE_RPA_FOLDER_ID = '186SkHC3HTMD-brVSRPIKwLMBsbhBxbGR';
const DRIVE_OUTROS_FOLDER_ID = '1tX9OZYP9w6Os8Jh-D0Y6ciPx5Gwyr7bI';
const DRIVE_TEMPLATES_ID = '19qMv4XpKpDWVVW9DiMhRoUKFz64BLzjA';
const EMAIL_RESPONSAVEL = 'marcelo.cardoso@mercadolivre.com';

// === PÁGINA INICIAL ===
function doGet(e) {
  const page = e && e.parameter && e.parameter.page ? e.parameter.page : 'Index';
  return HtmlService.createHtmlOutputFromFile(page)
    .setTitle('Nova Solicitação RPA');
}

// === MAPEAMENTOS ===
function getMappings() {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_MAPPINGS);
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 2).getValues(); // A–B (Grupo, Tipo)
  const grupos = [...new Set(data.map(r => r[0]))];
  const tipos = {};
  data.forEach(([grupo, tipo]) => {
    if (!tipos[grupo]) tipos[grupo] = [];
    tipos[grupo].push(tipo);
  });
  return { grupos, tipos };
}

// === DESCRIÇÃO E TEMPLATE (baseado na coluna C, download direto) ===
function getDescricaoRPA(tipoRPA) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const sheet = ss.getSheetByName(SHEET_MAPPINGS);
  const data = sheet.getRange(2, 2, sheet.getLastRow() - 1, 3).getValues(); // B–D (Tipo, NomeArquivo, Descrição)

  const linha = data.find(r => r[0] === tipoRPA);
  if (!linha) return { descricao: '', link: '' };

  const nomeArquivo = linha[1]?.trim();
  const descricao = linha[2] || 'Sem descrição disponível.';
  let link = '';

  if (nomeArquivo) {
    const folder = DriveApp.getFolderById(DRIVE_TEMPLATES_ID);
    const files = folder.getFiles();
    while (files.hasNext()) {
      const file = files.next();
      if (file.getName().trim().toLowerCase() === nomeArquivo.toLowerCase()) {
        const fileId = file.getId();
        link = `https://drive.google.com/uc?export=download&id=${fileId}`; // Força download direto
        break;
      }
    }
  }

  return { descricao, link };
}

// === UPLOAD DE ARQUIVOS (gera ID real do Drive) ===
function uploadArquivo(base64, nomeArquivo, mimeType) {
  const folder = DriveApp.getFolderById(DRIVE_RPA_FOLDER_ID);
  const idArquivo = Utilities.getUuid();
  const nomeComID = `${idArquivo}_${nomeArquivo}`;
  const blob = Utilities.newBlob(Utilities.base64Decode(base64), mimeType, nomeComID);
  const file = folder.createFile(blob);
  return {
    url: file.getUrl(),
    nomeArquivo: nomeComID,
    idArquivo: file.getId()
  };
}

function uploadArquivoOutros(base64, nomeArquivo, mimeType) {
  const folder = DriveApp.getFolderById(DRIVE_OUTROS_FOLDER_ID);
  const idArquivo = Utilities.getUuid();
  const nomeComID = `${idArquivo}_${nomeArquivo}`;
  const blob = Utilities.newBlob(Utilities.base64Decode(base64), mimeType, nomeComID);
  const file = folder.createFile(blob);
  return {
    url: file.getUrl(),
    nomeArquivo: nomeComID,
    idArquivo: file.getId()
  };
}

// === FUNÇÕES DE ENVIO DE E-MAILS ===

function enviarEmailSolicitante(dados) {
  const assunto = '✅ Solicitação Recebida - Robô ATS';
  
  const corpo = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #3483FA 0%, #2968C8 100%); padding: 30px; text-align: center;">
        <h1 style="color: #FFE600; margin: 0; font-size: 24px;">Solicitação Recebida!</h1>
      </div>
      
      <div style="background: #f5f5f5; padding: 30px;">
        <p style="font-size: 16px; color: #333;">Olá <strong>${dados.nome}</strong>,</p>
        
        <p style="font-size: 14px; color: #666; line-height: 1.6;">
          Recebemos sua solicitação de apoio do <strong>Robô ATS</strong> e ela será analisada pela nossa equipe.
          Retornaremos em breve com mais informações sobre o andamento.
        </p>
        
        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3483FA;">
          <h3 style="color: #3483FA; margin-top: 0;">Resumo da sua solicitação:</h3>
          <table style="width: 100%; font-size: 14px; color: #333;">
            <tr>
              <td style="padding: 8px 0; font-weight: bold; width: 150px;">ID da Solicitação:</td>
              <td style="padding: 8px 0;">${dados.id}</td>
            </tr>
            ${dados.grupo ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Grupo:</td>
              <td style="padding: 8px 0;">${dados.grupo}</td>
            </tr>
            ` : ''}
            ${dados.tipoRPA ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Tipo de RPA:</td>
              <td style="padding: 8px 0;">${dados.tipoRPA}</td>
            </tr>
            ` : ''}
            ${dados.descricao ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Descrição:</td>
              <td style="padding: 8px 0;">${dados.descricao}</td>
            </tr>
            ` : ''}
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Prazo:</td>
              <td style="padding: 8px 0;">${dados.prazo}</td>
            </tr>
            ${dados.notas ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Observações:</td>
              <td style="padding: 8px 0;">${dados.notas}</td>
            </tr>
            ` : ''}
            ${dados.linkArquivo ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Anexo:</td>
              <td style="padding: 8px 0;"><a href="${dados.linkArquivo}" style="color: #3483FA;">Ver arquivo</a></td>
            </tr>
            ` : ''}
            ${dados.linkArquivoExterno ? `
            <tr>
              <td style="padding: 8px 0; font-weight: bold;">Link Externo:</td>
              <td style="padding: 8px 0;"><a href="${dados.linkArquivoExterno}" style="color: #3483FA;">Ver link</a></td>
            </tr>
            ` : ''}
          </table>
        </div>
        
        <div style="background: linear-gradient(135deg, #FFE600 0%, #ffd700 100%); padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <p style="font-size: 15px; color: #333; margin: 0 0 15px 0; font-weight: bold;">
            📊 Acompanhe sua solicitação em tempo real
          </p>
          <a href="https://script.google.com/a/macros/mercadolivre.com/s/AKfycbwZeBxv8hylAWRGjnr9sL57Xanaz2QPoFBCQ9uWrGL-c-smE50GiyhW-X7bXcg81j4/exec" 
             style="display: inline-block; background: #3483FA; color: white; padding: 14px 32px; 
                    text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            🔍 Ver Status da Solicitação
          </a>
          <p style="font-size: 12px; color: #666; margin: 15px 0 0 0;">
            Clique no botão acima para acessar o painel de acompanhamento
          </p>
        </div>
        
        <p style="font-size: 14px; color: #666; line-height: 1.6;">
          Caso tenha alguma dúvida, entre em contato com nossa equipe.
        </p>
        
        <p style="font-size: 14px; color: #666;">
          att<br>
          <strong style="color: #3483FA;">Legal Analytics</strong>
        </p>
      </div>
      
      <div style="background: #333; padding: 20px; text-align: center;">
        <p style="color: #999; font-size: 12px; margin: 0;">
          Este é um e-mail automático. Por favor, não responda.
        </p>
      </div>
    </div>
  `;
  
  MailApp.sendEmail({
    to: dados.email,
    subject: assunto,
    htmlBody: corpo
  });
}

function getEmailsResponsaveis() {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_EMAILS);
    if (!sheet) {
      console.log('Aba "Dimensão" não encontrada, usando e-mail padrão');
      return [EMAIL_RESPONSAVEL];
    }
    
    const lastRow = sheet.getLastRow();
    if (lastRow < 2) {
      console.log('Nenhum e-mail encontrado na planilha, usando e-mail padrão');
      return [EMAIL_RESPONSAVEL];
    }
    
    // Lê coluna A a partir da linha 2
    const emails = sheet.getRange(2, 1, lastRow - 1, 1).getValues()
      .map(row => row[0])
      .filter(email => email && email.toString().trim() !== '' && email.toString().includes('@'))
      .map(email => email.toString().trim());
    
    if (emails.length === 0) {
      console.log('Nenhum e-mail válido encontrado, usando e-mail padrão');
      return [EMAIL_RESPONSAVEL];
    }
    
    return emails;
  } catch (error) {
    console.log('Erro ao buscar e-mails: ' + error.message + ', usando e-mail padrão');
    return [EMAIL_RESPONSAVEL];
  }
}

function enviarEmailResponsavel(dados) {
  const tipoSolicitacao = dados.tipoRPA ? 'Solicitação Padrão' : 'Nova Solicitação de RPA';
  const assunto = `🎫 [TICKET] ${tipoSolicitacao} - ${dados.nome}`;
  
  const corpo = `
    <div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #2968C8 0%, #1a4d8f 100%); padding: 25px;">
        <h1 style="color: #FFE600; margin: 0; font-size: 22px;">🎫 Novo Ticket - Robô ATS</h1>
        <p style="color: white; margin: 10px 0 0 0; font-size: 14px;">${tipoSolicitacao}</p>
      </div>
      
      <div style="background: #f8f9fa; padding: 25px;">
        <div style="background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
          <h2 style="color: #3483FA; margin-top: 0; border-bottom: 2px solid #FFE600; padding-bottom: 10px;">
            Informações do Ticket
          </h2>
          
          <table style="width: 100%; font-size: 14px; color: #333; border-collapse: collapse;">
            <tr style="background: #f8f9fa;">
              <td style="padding: 12px; font-weight: bold; width: 180px; border: 1px solid #e0e0e0;">ID do Ticket:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><code style="background: #FFE600; padding: 4px 8px; border-radius: 4px; font-weight: bold;">${dados.id}</code></td>
            </tr>
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Data/Hora:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;">${new Date().toLocaleString('pt-BR')}</td>
            </tr>
            <tr style="background: #f8f9fa;">
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Solicitante:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><strong>${dados.nome}</strong></td>
            </tr>
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">E-mail:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><a href="mailto:${dados.email}" style="color: #3483FA;">${dados.email}</a></td>
            </tr>
            ${dados.grupo ? `
            <tr style="background: #f8f9fa;">
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Grupo:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;">${dados.grupo}</td>
            </tr>
            ` : ''}
            ${dados.tipoRPA ? `
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Tipo de RPA:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><strong style="color: #3483FA;">${dados.tipoRPA}</strong></td>
            </tr>
            ` : ''}
            ${dados.descricao ? `
            <tr style="background: #f8f9fa;">
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Descrição:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;">${dados.descricao}</td>
            </tr>
            ` : ''}
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">⏰ Prazo:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><strong style="color: #d32f2f;">${dados.prazo}</strong></td>
            </tr>
            ${dados.notas ? `
            <tr style="background: #f8f9fa;">
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0; vertical-align: top;">Observações:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;">${dados.notas}</td>
            </tr>
            ` : ''}
            ${dados.linkArquivo ? `
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Anexo:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><a href="${dados.linkArquivo}" 
                 style="color: #3483FA;">Acessar Arquivo no Drive</a></td>
            </tr>
            ` : ''}
            ${dados.linkArquivoExterno ? `
            <tr>
              <td style="padding: 12px; font-weight: bold; border: 1px solid #e0e0e0;">Link Externo:</td>
              <td style="padding: 12px; border: 1px solid #e0e0e0;"><a href="${dados.linkArquivoExterno}" 
                 style="color: #3483FA;">Ver link</a></td>
            </tr>
            ` : ''}
          </table>
          
          <div style="margin-top: 25px; padding: 15px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #FFE600;">
            <p style="margin: 0; font-size: 13px; color: #856404;">
              <strong>⚠️ Ação Necessária:</strong> Analisar a solicitação e retornar ao solicitante dentro do prazo estabelecido.
            </p>
          </div>
        </div>
      </div>
      
      <div style="background: #333; padding: 20px; text-align: center;">
        <p style="color: #999; font-size: 12px; margin: 0;">
          Sistema de Gestão de Solicitações - Robô ATS | Mercado Livre
        </p>
      </div>
    </div>
  `;
  
  const emailsResponsaveis = getEmailsResponsaveis();
  const destinatarios = emailsResponsaveis.join(',');
  
  MailApp.sendEmail({
    to: destinatarios,
    subject: assunto,
    htmlBody: corpo
  });
}

// === SALVAR SOLICITAÇÃO PADRÃO ===
function salvarSolicitacao(formData) {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_SOLICITACOES);
  const id = Utilities.getUuid();
  const now = new Date();
  const linkDireto = formData.idArquivo
    ? `https://drive.google.com/file/d/${formData.idArquivo}/view?usp=sharing`
    : '';

  sheet.appendRow([
    id,
    now,
    formData.grupo,
    formData.tipoRPA,
    formData.nome,
    formData.email,
    formData.prazo,
    linkDireto,
    formData.nomeArquivo || '',
    formData.idArquivo || '',
    formData.notas || '',
    formData.linkArquivoExterno || '' // Campo de link externo fornecido pelo usuário
  ]);

  const dadosEmail = {
    id: id,
    grupo: formData.grupo,
    tipoRPA: formData.tipoRPA,
    nome: formData.nome,
    email: formData.email,
    prazo: formData.prazo,
    linkArquivo: linkDireto,
    nomeArquivo: formData.nomeArquivo || '',
    notas: formData.notas || '',
    linkArquivoExterno: formData.linkArquivoExterno || ''
  };
  
  try {
    enviarEmailSolicitante(dadosEmail);
    enviarEmailResponsavel(dadosEmail);
  } catch (error) {
    console.log('Erro ao enviar e-mails: ' + error.message);
  }

  return id;
}

// === SALVAR SOLICITAÇÃO "NOVA RPA" ===
function salvarSolicitacaoOutros(formData) {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NOVAS);
  const id = Utilities.getUuid();
  const now = new Date();
  const linkDireto = formData.idArquivo
    ? `https://drive.google.com/file/d/${formData.idArquivo}/view?usp=sharing`
    : '';

  sheet.appendRow([
    id,
    now,
    formData.nome,
    formData.email,
    formData.prazo,
    formData.notas,
    formData.descricao || '',
    linkDireto,
    formData.nomeArquivo || '',
    formData.idArquivo || ''
  ]);

  const dadosEmail = {
    id: id,
    nome: formData.nome,
    email: formData.email,
    prazo: formData.prazo,
    notas: formData.notas,
    descricao: formData.descricao || '',
    linkArquivo: linkDireto,
    nomeArquivo: formData.nomeArquivo || ''
  };
  
  try {
    enviarEmailSolicitante(dadosEmail);
    enviarEmailResponsavel(dadosEmail);
  } catch (error) {
    console.log('Erro ao enviar e-mails: ' + error.message);
  }

  return id;
}
