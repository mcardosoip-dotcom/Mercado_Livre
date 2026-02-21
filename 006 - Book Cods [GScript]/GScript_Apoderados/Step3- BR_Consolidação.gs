// --- CONFIGURAÇÕES GERAIS ---

/* IDs e Nomes das Planilhas/Abas */
const ID_PLANILHA_ORIGEM = '1Ro5If85-7E--0At8q0SamKsR-mnVlJgwIY5YBRwpKJE';
const ID_PLANILHA_DESTINO = '1zo6019x58F7YiTbijqpawmbFVWhBs8nhZEjYXyEjqxU';
const NOME_ABA_DESTINO = 'Nomes_e_classes';
const NOME_ABA_FINAL = 'Tabela_Final'; // Nova aba final
const ID_PLANILHA_REGRAS = '1EohsmWblwSVujLowqe1025y4Y3T6sgvs-V6NtPIuRIU';
const NOME_ABA_REGRAS = 'Regras';

/* Nomes das Abas de Origem */
const ABAS_ORIGEM = [
  "Base People",
  "Base Exceção a classe",
  "Base de estrangeiros",
  "Base Jurídico",
  "Base de novos pedidos"
];

/* Cabeçalho Padrão (10 colunas) */
const CABECALHO_PADRAO = [
  "nome", "cargo", "cpf", "divisao", "area_nome", "subarea_nome", 
  "categoria", "oab", "email", "classe" // Coluna J (índice 9)
];

/* Colunas Adicionais de Classificação (8 colunas) */
const COLUNAS_ADICIONAIS_CLASSIFICACAO = [
  "Classe_Cruzamento1", "Classe_Cruzamento2", "Classe_Cruzamento3",
  "Base Exceção a classe (Classe por Nome)", "Base de estrangeiros (Classe por Nome)", 
  "Base Jurídico (Classe por Nome)", "Base de novos pedidos (Classe por Nome)",
  "Classe_final" 
]; 

/* Cabeçalho completo (10 Padrão + 1 Fonte + 8 Classificação = 19 Colunas) */
const consolidatedHeader = [...CABECALHO_PADRAO, "fonte", ...COLUNAS_ADICIONAIS_CLASSIFICACAO];

/* Hierarquia de Classificação (Prioridade para preenchimento da Classe_final) */
const COLUNAS_PRIORIDADE = [ 
  "Base Exceção a classe (Classe por Nome)", 
  "Classe_Cruzamento3",
  "Classe_Cruzamento2",
  "Classe_Cruzamento1",
  "Base de estrangeiros (Classe por Nome)",
  "Base Jurídico (Classe por Nome)",
  "Base de novos pedidos (Classe por Nome)"
];

// Mapeamento de índices para as colunas do cabeçalho padrão (0-9)
const INDEX = {
  nome: 0, cargo: 1, cpf: 2, divisao: 3, area_nome: 4, 
  subarea_nome: 5, categoria: 6, oab: 7, email: 8, classe: 9,
};

// Mapeamento de índices para as colunas ADICIONAIS no array final (10-18)
const INDEX_ADICIONAL = {
  // A coluna 'fonte' está no índice 10, mas não é usada neste Map
  Classe_Cruzamento1: 11, Classe_Cruzamento2: 12, Classe_Cruzamento3: 13,
  'Base Exceção a classe (Classe por Nome)': 14, 'Base de estrangeiros (Classe por Nome)': 15, 
  'Base Jurídico (Classe por Nome)': 16, 'Base de novos pedidos (Classe por Nome)': 17,
  Classe_final: 18, 
};


// --- FUNÇÃO PRINCIPAL ---

function processarConsolidacaoEClassificacao() {
  Logger.log("--- INÍCIO DO PROCESSO DE CONSOLIDAÇÃO E CLASSIFICAÇÃO ---");
  
  try {
    // 1. Acesso às Planilhas
    const ssOrigem = SpreadsheetApp.openById(ID_PLANILHA_ORIGEM);
    const ssDestino = SpreadsheetApp.openById(ID_PLANILHA_DESTINO);
    const ssRegras = SpreadsheetApp.openById(ID_PLANILHA_REGRAS);
    
    // 2. Consolidação e Desduplicação (NOVA LÓGICA DE PRIORIDADE APLICADA AQUI)
    const consolidatedData = consolidarDados(ssOrigem); 
    Logger.log(`[CONSOLIDAÇÃO] Total de linhas consolidadas após desduplicação: ${consolidatedData.length}`);
    
    // Prepara a base consolidada para escrita inicial (19 colunas)
    const dataToWrite = [consolidatedHeader, ...consolidatedData.map(row => {
      const emptyAdditionalColumns = Array(COLUNAS_ADICIONAIS_CLASSIFICACAO.length).fill('');
      return [...row, ...emptyAdditionalColumns];
    })];
    
    // Escreve a base consolidada inicial na aba de destino
    escreverDados(ssDestino, NOME_ABA_DESTINO, dataToWrite);
    Logger.log(`[ESCRITA INICIAL] Linhas iniciais gravadas na aba ${NOME_ABA_DESTINO}.`);
    
    // Releitura dos dados da aba de destino para processamento in-loco
    const sheetDestino = ssDestino.getSheetByName(NOME_ABA_DESTINO);
    if (!sheetDestino) { throw new Error(`Aba de destino '${NOME_ABA_DESTINO}' não encontrada.`); }

    const totalRows = sheetDestino.getLastRow();
    if (totalRows <= 1) { Logger.log("Nenhuma linha para processar após a consolidação."); return; }
    
    // Lê o Range completo (excluindo cabeçalho)
    const finalData = sheetDestino.getRange(2, 1, totalRows - 1, consolidatedHeader.length).getValues();
    
    // 3. Preparar e carregar as Regras de Cruzamento
    const rulesMap = carregarRegras(ssRegras, NOME_ABA_REGRAS);
    
    // 4. Preparar as Bases de Classe por Nome
    const classePorNomeMaps = carregarClassesPorNome(ssOrigem);
    
    // 5. Cruzamentos e Definição da Classe Final (Iteração por linha)
    let countC1 = 0, countC2 = 0, countC3 = 0;
    
    for (let i = 0; i < finalData.length; i++) {
      const row = finalData[i];
      
      // 5.1. Cruzamento para classificação (Regras)
      const cargo = String(row[INDEX.cargo]).trim();
      const divisao = String(row[INDEX.divisao]).trim();
      const area_nome = String(row[INDEX.area_nome]).trim();
      
      const ruleEntry = rulesMap.get(cargo) || null;
      
      // ... (Lógica de cruzamentos C1, C2, C3, Classes por Nome) ...
      if (ruleEntry && ruleEntry.c1) { row[INDEX_ADICIONAL.Classe_Cruzamento1] = ruleEntry.c1; countC1++; }
      if (ruleEntry && ruleEntry.c2.get(divisao)) { row[INDEX_ADICIONAL.Classe_Cruzamento2] = ruleEntry.c2.get(divisao); countC2++; }
      if (ruleEntry && ruleEntry.c3.get(divisao) && ruleEntry.c3.get(divisao).get(area_nome)) { row[INDEX_ADICIONAL.Classe_Cruzamento3] = ruleEntry.c3.get(divisao).get(area_nome); countC3++; }
      
      const nome = String(row[INDEX.nome]).trim();
      const colunasPorNome = {
        'Base Exceção a classe (Classe por Nome)': 'Base Exceção a classe', 'Base de estrangeiros (Classe por Nome)': 'Base de estrangeiros', 
        'Base Jurídico (Classe por Nome)': 'Base Jurídico', 'Base de novos pedidos (Classe por Nome)': 'Base de novos pedidos'
      };
      for (const colunaAdicional in colunasPorNome) {
        const nomeDaAba = colunasPorNome[colunaAdicional];
        const valorClasse = classePorNomeMaps[nomeDaAba].get(nome) || '';
        row[INDEX_ADICIONAL[colunaAdicional]] = valorClasse;
      }
      
      // 5.3. Definição da Classe final (hierarquia)
      let classeFinal = '';
      for (const colNome of COLUNAS_PRIORIDADE) {
        const valor = row[INDEX_ADICIONAL[colNome]];
        if (valor && String(valor).trim() !== '') {
          classeFinal = valor;
          break;
        }
      }
      row[INDEX_ADICIONAL.Classe_final] = classeFinal;
      
      // 6. Regra adicional obrigatória (OAB e Cargo)
      const oab = String(row[INDEX.oab]).trim();
      const cargoFinal = String(row[INDEX.cargo]).trim();
      
      if (oab !== '' && (cargoFinal === 'Gerente' || cargoFinal === 'Gerente Senior')) {
        row[INDEX_ADICIONAL.Classe_final] = 'D'; // Sobrescreve
      }
    }
    
    Logger.log(`[CRUZAMENTOS] Matches C1 (cargo): ${countC1}`);
    Logger.log(`[CRUZAMENTOS] Matches C2 (cargo/divisao): ${countC2}`);
    Logger.log(`[CRUZAMENTOS] Matches C3 (cargo/divisao/area): ${countC3}`);
    
    // 7. Gravação final da aba Nomes_e_classes
    sheetDestino.getRange(2, 1, finalData.length, finalData[0].length).setValues(finalData);
    Logger.log(`[ESCRITA FINAL] ${finalData.length} linhas processadas e gravadas com as classificações finais.`);
    
    // 8. Geração da Tabela Final (Executa a função ajustada)
    gerarTabelaFinal(ssDestino);
    
    Logger.log("--- FIM DO PROCESSO ---");
    
  } catch (e) {
    Logger.log(`ERRO: ${e.toString()}`);
  }
}

// --- FUNÇÕES AUXILIARES ---

/**
 * [ETAPA 2] Lê todas as abas de origem, consolida, trata CPF e desduplica.
 * **Lógica de Duplicidade Revisada:** Prioriza 'Base Exceção a classe', depois 'Base Jurídico'.
 */
function consolidarDados(ssOrigem) {
  const consolidated = new Map(); 
  let totalRead = 0;
  let duplicatedCount = 0;
  const INDEX_FONTE = 10; // Índice da coluna 'fonte' no array da linha.

  for (const sheetName of ABAS_ORIGEM) {
    const sheet = ssOrigem.getSheetByName(sheetName);
    if (!sheet || sheet.getLastRow() <= 1) continue;
    
    const rows = sheet.getDataRange().getValues().slice(1);
    totalRead += rows.length;
    
    for (const row of rows) {
      let cpf = String(row[INDEX.cpf]).trim();
      const source = sheetName;
      
      // 2. Regra de CPF (Formatação)
      if (source !== 'Base de estrangeiros' && cpf !== '') {
        const digits = cpf.replace(/[^0-9]/g, '');
        if (digits.length === 11) {
          row[INDEX.cpf] = digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
        } else {
          row[INDEX.cpf] = cpf; 
        }
      } else {
        row[INDEX.cpf] = cpf;
      }
      
      const newRow = [...row, source]; // Adiciona a coluna 'fonte' (11 colunas)
      const key = newRow[INDEX.cpf]; 
      
      // 2. Duplicidade: Aplicar nova hierarquia
      if (key !== '') {
        const existingRow = consolidated.get(key);
        
        if (!existingRow) {
          // Caso 1: Não existe, apenas adiciona.
          consolidated.set(key, newRow);
        } else {
          // Caso 2: Duplicidade, aplicar regras de prioridade.
          const existingSource = existingRow[INDEX_FONTE]; 
          let shouldReplace = false;

          // PRIORIDADE MÁXIMA: Base Exceção a classe
          if (source === 'Base Exceção a classe') {
             // Se a nova fonte é Base Exceção a classe, ela sempre ganha (exceto de si mesma).
            if (existingSource !== 'Base Exceção a classe') {
              shouldReplace = true;
            }
          } 
          // SEGUNDA PRIORIDADE: Base Jurídico
          else if (source === 'Base Jurídico') {
            // Se a nova fonte é Base Jurídico, ela só ganha se a existente for de menor prioridade.
            if (existingSource !== 'Base Exceção a classe' && existingSource !== 'Base Jurídico') {
                  shouldReplace = true;
            }
          }
          // Para outras fontes, shouldReplace = false por padrão.

          if (shouldReplace) {
            consolidated.set(key, newRow);
            duplicatedCount++;
          }
          // Senão, mantém o existingRow (princípio do "first-found" para fontes de menor prioridade).
        }
      } else {
        // Se o CPF estiver vazio, adiciona a linha com uma chave única (sem desduplicação)
        consolidated.set(Symbol(), newRow);
      }
    }
  }
  
  Logger.log(`[CONSOLIDAÇÃO] Total de linhas lidas: ${totalRead}`);
  Logger.log(`[CONSOLIDAÇÃO] Total de registros duplicados sobrescritos/ignorados: ${duplicatedCount}`);
  return Array.from(consolidated.values());
}

/**
 * [ETAPA FINAL] Gera a aba 'Tabela_Final' contendo Classe_Final, nome, cpf e fonte.
 * MODIFICADO: Agora inclui a coluna K (fonte) vinda da aba de destino.
 */
function gerarTabelaFinal(ssDestino) {
  Logger.log("--- INÍCIO DA GERAÇÃO DA TABELA FINAL ---");
  
  try {
    const sheetOrigem = ssDestino.getSheetByName(NOME_ABA_DESTINO);
    
    if (!sheetOrigem) {
      Logger.log(`ERRO: A aba de origem '${NOME_ABA_DESTINO}' não foi encontrada.`);
      return;
    }

    const lastRow = sheetOrigem.getLastRow();
    const lastCol = sheetOrigem.getLastColumn();
    
    if (lastRow <= 1) {
      Logger.log(`A aba ${NOME_ABA_DESTINO} não contém dados para serem copiados.`);
      // Cabeçalho ajustado para 4 colunas
      const dataVazia = [["Classe_Final", "nome", "cpf", "fonte"]];
      escreverDados(ssDestino, NOME_ABA_FINAL, dataVazia);
      return;
    }

    // 1. Ler os dados
    const dataOrigem = sheetOrigem.getRange(1, 1, lastRow, lastCol).getValues();
    
    // Índices de interesse: Classe_Final (S=18), nome (A=0), cpf (C=2), fonte (K=10)
    const INDEX_FINAL = INDEX_ADICIONAL.Classe_final; 
    const INDEX_NOME = INDEX.nome; 
    const INDEX_CPF = INDEX.cpf; 
    const INDEX_FONTE = 10; // Adicionado: Índice da coluna 'fonte'

    const tabelaFinalData = [];

    // 2. Processar e reordenar
    tabelaFinalData.push(["Classe_Final", "nome", "cpf", "fonte"]); // Cabeçalho atualizado
    
    let linhasProcessadas = 0;
    for (let i = 1; i < dataOrigem.length; i++) {
      const row = dataOrigem[i];
      
      const classeFinal = row[INDEX_FINAL];
      const nome = row[INDEX_NOME];
      const cpf = row[INDEX_CPF];
      const fonte = row[INDEX_FONTE]; // Captura a fonte
      
      tabelaFinalData.push([classeFinal, nome, cpf, fonte]);
      linhasProcessadas++;
    }

    // ----------------------------------------------------
    // Ordenação
    // ----------------------------------------------------
    
    // Remove o cabeçalho antes de ordenar
    const header = tabelaFinalData.shift(); 
    
    tabelaFinalData.sort((a, b) => {
      const classeA = String(a[0]).toLowerCase(); // Coluna A da Tabela Final (Classe_Final)
      const classeB = String(b[0]).toLowerCase();
      
      const nomeA = String(a[1]).toLowerCase(); // Coluna B da Tabela Final (Nome)
      const nomeB = String(b[1]).toLowerCase();

      // 1. Classificar por Classe_Final ascendente
      if (classeA < classeB) return -1;
      if (classeA > classeB) return 1;

      // 2. Classificar por Nome ascendente (desempate)
      if (nomeA < nomeB) return -1;
      if (nomeA > nomeB) return 1;

      return 0;
    });
    
    // Adiciona o cabeçalho de volta
    tabelaFinalData.unshift(header);
    
    // 3. Escrever na aba Tabela_Final
    escreverDados(ssDestino, NOME_ABA_FINAL, tabelaFinalData);
    
    Logger.log(`[TABELA FINAL] ${linhasProcessadas} linhas gravadas na aba '${NOME_ABA_FINAL}'.`);
    Logger.log("--- FIM DA GERAÇÃO DA TABELA FINAL ---");
    
  } catch (e) {
    Logger.log(`ERRO na geração da Tabela Final: ${e.toString()}`);
  }
}

/**
 * [ETAPA 3] Carrega a planilha de regras em um objeto Map aninhado para busca eficiente.
 */
function carregarRegras(ssRegras, sheetName) {
  const sheet = ssRegras.getSheetByName(sheetName);
  if (!sheet || sheet.getLastRow() <= 1) { return new Map(); }
  
  const rows = sheet.getDataRange().getValues().slice(1);
  const rulesMap = new Map();
  
  const COL_REGRAS = { cargo: 0, divisao: 1, area_nome: 2, retorno: 4 };
  let count = 0;
  
  for (const row of rows) {
    const cargo = String(row[COL_REGRAS.cargo]).trim();
    const divisao = String(row[COL_REGRAS.divisao]).trim();
    const area_nome = String(row[COL_REGRAS.area_nome]).trim();
    const valorRetorno = String(row[COL_REGRAS.retorno]).trim();
    
    if (!cargo || !valorRetorno) continue;
    count++;

    if (!rulesMap.has(cargo)) {
      rulesMap.set(cargo, { c1: '', c2: new Map(), c3: new Map() });
    }
    
    const ruleEntry = rulesMap.get(cargo);
    
    if (ruleEntry.c1 === '') { ruleEntry.c1 = valorRetorno; }
    if (divisao !== '' && !ruleEntry.c2.has(divisao)) { ruleEntry.c2.set(divisao, valorRetorno); }
    
    if (divisao !== '' && area_nome !== '') {
      if (!ruleEntry.c3.has(divisao)) { ruleEntry.c3.set(divisao, new Map()); }
      if (!ruleEntry.c3.get(divisao).has(area_nome)) { ruleEntry.c3.get(divisao).set(area_nome, valorRetorno); }
    }
  }
  
  Logger.log(`[REGRAS] ${count} linhas de regras carregadas da aba '${sheetName}'.`);
  return rulesMap;
}

/**
 * [ETAPA 4] Carrega os dados das bases de origem em Maps para busca por "nome".
 */
function carregarClassesPorNome(ssOrigem) {
  const basesParaCruzamento = [
    "Base Exceção a classe", "Base de estrangeiros", 
    "Base Jurídico", "Base de novos pedidos"
  ];
  
  const classePorNomeMaps = {};
  
  for (const sheetName of basesParaCruzamento) {
    const sheet = ssOrigem.getSheetByName(sheetName);
    if (!sheet || sheet.getLastRow() <= 1) {
      Logger.log(`[ALERTA] Aba '${sheetName}' não disponível para cruzamento por nome.`);
      classePorNomeMaps[sheetName] = new Map();
      continue;
    }
    
    const rows = sheet.getDataRange().getValues().slice(1);
    const nameMap = new Map(); 
    let count = 0;
    
    for (const row of rows) {
      const nome = String(row[INDEX.nome]).trim();
      const classe = String(row[INDEX.classe]).trim();
      
      if (nome !== '') {
        nameMap.set(nome, classe);
        count++;
      }
    }
    
    classePorNomeMaps[sheetName] = nameMap;
    Logger.log(`[CRUZAMENTO POR NOME] ${count} entradas carregadas da aba '${sheetName}'.`);
  }
  
  return classePorNomeMaps;
}

/**
 * Função para escrever (ou reescrever/limpar) os dados na planilha de destino.
 */
function escreverDados(ss, sheetName, data) {
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  
  sheet.clearContents();
  
  if (data.length > 0 && data[0].length > 0) {
    sheet.getRange(1, 1, data.length, data[0].length).setValues(data);
  }
}