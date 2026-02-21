/**
 * Script para extrair dados do Google Doc e inserir na planilha
 * SEGUNDA BASE DE DADOS
 * Coluna A: Classe
 * Coluna B: Nome
 */

function transporDadosDocParaPlanilha2() {
  const DOC_ID = '1rydlU1tfRipgQ-P-uILgsXvwNq4UGXci20WfkkznESY';
  const SHEET_ID = '15xxGjUdYiEIYf07a1o3mT120tg0vc_cud0jeKH0xMJk';
  const SHEET_NAME = 'Resultado';
  
  try {
    Logger.log('=== INICIANDO TRANSPOSIÇÃO DE DADOS (BASE 2) ===');
    Logger.log('Acessando documento...');
    const doc = DocumentApp.openById(DOC_ID);
    const body = doc.getBody();
    const text = body.getText();
    
    Logger.log('Extraindo dados do documento...');
    const dados = extrairDados(text);
    
    Logger.log(`\n✓ Total de nomes extraídos: ${dados.length}`);
    
    if (dados.length === 0) {
      Logger.log('⚠ AVISO: Nenhum nome foi extraído. Verifique o formato do documento.');
      return;
    }
    
    const contagemPorClasse = {};
    dados.forEach(registro => {
      if (!contagemPorClasse[registro.classe]) {
        contagemPorClasse[registro.classe] = 0;
      }
      contagemPorClasse[registro.classe]++;
    });
    
    Logger.log('\n--- Resumo por Classe ---');
    Object.keys(contagemPorClasse).sort().forEach(classe => {
      Logger.log(`Classe ${classe}: ${contagemPorClasse[classe]} nomes`);
    });
    
    Logger.log('\nAcessando planilha...');
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Aba "${SHEET_NAME}" não encontrada na planilha.`);
    }
    
    const linhaInicial = sheet.getLastRow();
    if (linhaInicial === 0) {
      sheet.appendRow(['Classe', 'Nome']);
      Logger.log('Cabeçalhos adicionados.');
    }
    
    Logger.log('\nInserindo dados na planilha...');
    let nomesInseridos = 0;
    dados.forEach(registro => {
      sheet.appendRow([registro.classe, registro.nome]);
      nomesInseridos++;
    });
    
    const linhaFinal = sheet.getLastRow();
    
    Logger.log('\n=== TRANSPOSIÇÃO CONCLUÍDA ===');
    Logger.log(`✓ ${nomesInseridos} nomes foram transpostos com sucesso!`);
    Logger.log(`✓ Dados inseridos da linha ${linhaInicial + 1} até a linha ${linhaFinal}`);
    Logger.log(`✓ Planilha: "${SHEET_NAME}"`);
    
  } catch (error) {
    Logger.log('\n=== ERRO NA TRANSPOSIÇÃO ===');
    Logger.log('ERRO: ' + error.toString());
  }
}

/**
 * Função para extrair Classe e Nome do texto
 * Padrão: "Nome Completo, DNI número;"
 */
function extrairDados(text) {
  const dados = [];
  
  // Dividir o texto em seções por classe
  const secoes = text.split(/Apoderados\s+Clase?\s+([A-G])/i);
  
  for (let i = 1; i < secoes.length; i += 2) {
    const classe = secoes[i].toUpperCase();
    const conteudo = secoes[i + 1];
    
    if (!conteudo) continue;
    
    // Dividir por ponto e vírgula para separar cada pessoa
    const pessoas = conteudo.split(';');
    
    pessoas.forEach(pessoa => {
      pessoa = pessoa.trim();
      
      if (!pessoa) return;
      
      // Extrair o nome (tudo antes da vírgula)
      const match = pessoa.match(/^([^,]+),/);
      
      if (match) {
        const nome = match[1].trim();
        
        if (nome && nome.match(/[a-zA-ZáéíóúÁÉÍÓÚñÑ]/)) {
          dados.push({
            classe: classe,
            nome: nome
          });
        }
      }
    });
  }
  
  return dados;
}

/**
 * Função de teste para a segunda base
 */
function testarExtracao2() {
  const DOC_ID = '1rydlU1tfRipgQ-P-uILgsXvwNq4UGXci20WfkkznESY';
  
  Logger.log('=== TESTE DE EXTRAÇÃO (BASE 2) ===\n');
  
  const doc = DocumentApp.openById(DOC_ID);
  const body = doc.getBody();
  const text = body.getText();
  
  Logger.log('--- TENTANDO EXTRAIR DADOS ---');
  const dados = extrairDados(text);
  
  Logger.log(`\n✓ Total extraído: ${dados.length} nomes`);
  
  if (dados.length > 0) {
    const contagemPorClasse = {};
    dados.forEach(registro => {
      if (!contagemPorClasse[registro.classe]) {
        contagemPorClasse[registro.classe] = 0;
      }
      contagemPorClasse[registro.classe]++;
    });
    
    Logger.log('\n--- Resumo por Classe ---');
    Object.keys(contagemPorClasse).sort().forEach(classe => {
      Logger.log(`Classe ${classe}: ${contagemPorClasse[classe]} nomes`);
    });
    
    Logger.log('\n--- Primeiros 10 registros ---');
    dados.slice(0, 10).forEach(d => Logger.log(`${d.classe} - ${d.nome}`));
  }
}

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Importar Dados')
    .addItem('Importar Base 1', 'transporDadosDocParaPlanilha')
    .addItem('Importar Base 2', 'transporDadosDocParaPlanilha2')
    .addToUi();
}