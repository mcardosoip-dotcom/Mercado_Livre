/**
 * Script Standalone para Análise de Discrepância de Classes.
 * Compara a "Versão Anterior" com a "Versão Atual" (Consolidado).
 */
function analisarDiscrepanciaDeClasses() {
  // =============================================================
  // === CONFIGURAÇÕES (IDs e Nomes de Coluna CORRIGIDOS) ========
  // =============================================================
  
  // Planilha da Versão Anterior
  const ID_ANTERIOR = '1VBcwkH3VeMwr7zchk15Y0E5COxqoA0PtzfyiNIdsbjE'; 
  const NOME_ABA_ANTERIOR = '2025_Jun';
  // Corrigido para 'Classe_Final' (Assumindo que Versão Anterior usa o mesmo cabeçalho de saída)
  const COLUNA_CLASSE_ANTERIOR = 'Classe_Final'; 

  // Planilha da Versão Atual (Consolidado)
  const ID_ATUAL = '1zo6019x58F7YiTbijqpawmbFVWhBs8nhZEjYXyEjqxU'; 
  const NOME_ABA_ATUAL = 'Tabela_Final';
  const COLUNA_CLASSE_ATUAL = 'Classe_Final'; 

  // Planilha de Saída da Análise
  const ID_SAIDA_ANALISE = '1KV2qcBY99LslheMmKJaLcRAvTPjoWYvdZVXh0-5-fJw';
  const NOME_ABA_COMPARATIVO = 'Comparativo_Completo';
  const NOME_ABA_DISCREPANCIAS = 'Discrepancias';
  
  // Coluna chave para Merge e Padronização (Corrigido para 'nome' minúsculo)
  const COLUNA_CHAVE = 'nome';

  // ===============================================

  try {
    Logger.log('Iniciando análise de discrepância...');

    // 1. Abertura das Planilhas
    const planilhaAnterior = SpreadsheetApp.openById(ID_ANTERIOR);
    const planilhaAtual = SpreadsheetApp.openById(ID_ATUAL);
    const planilhaSaida = SpreadsheetApp.openById(ID_SAIDA_ANALISE);
    
    const abaAnterior = planilhaAnterior.getSheetByName(NOME_ABA_ANTERIOR);
    const abaAtual = planilhaAtual.getSheetByName(NOME_ABA_ATUAL);

    if (!abaAnterior) throw new Error(`Aba "${NOME_ABA_ANTERIOR}" não encontrada na Versão Anterior.`);
    if (!abaAtual) throw new Error(`Aba "${NOME_ABA_ATUAL}" não encontrada na Versão Atual.`);
    
    // --- Funções de Ajuda ---
    
    /** Padroniza o nome (strip().lower()). */
    const padronizarNome = (nome) => {
      return String(nome || '').trim().toLowerCase();
    };

    /** Pega o cabeçalho e os dados de uma aba. Tenta encontrar a coluna CHAVE ignorando case. */
    const getDadosComCabecalho = (aba, chaveColuna, classeColuna) => {
        const range = aba.getDataRange();
        if (range.getNumRows() < 1) return { header: [], data: [], nomeIdx: -1, classeIdx: -1 }; 
        const values = range.getValues();
        const header = values[0];
        const lowerHeader = header.map(h => String(h).toLowerCase());

        // Tenta encontrar o índice da coluna chave
        const nomeIdx = lowerHeader.indexOf(chaveColuna.toLowerCase());
        const classeIdx = lowerHeader.indexOf(classeColuna.toLowerCase());

        // Se o nome da coluna da planilha for exatamente igual, retorna o valor do cabeçalho original.
        // Se a busca lowerCase deu certo, mas a original é diferente (ex: Nome vs nome), usa o lowerCase para o lookup.
        
        return { 
            header: header, 
            data: values.slice(1),
            nomeIdx: nomeIdx !== -1 ? nomeIdx : header.indexOf(chaveColuna), // Tenta achar o exato
            classeIdx: classeIdx !== -1 ? classeIdx : header.indexOf(classeColuna) // Tenta achar o exato
        };
    };

    // --- 2. Leitura e Preparação da Versão Anterior ---
    const { header: hAnterior, data: dAnterior, nomeIdx: nomeIdxAnterior, classeIdx: classeIdxAnterior } = 
        getDadosComCabecalho(abaAnterior, COLUNA_CHAVE, COLUNA_CLASSE_ANTERIOR);
    
    // Revalidação com os novos índices
    if (nomeIdxAnterior === -1 || classeIdxAnterior === -1) {
      throw new Error(`Colunas chave ('${COLUNA_CHAVE}' e '${COLUNA_CLASSE_ANTERIOR}') não encontradas na Versão Anterior. (Verifique o uso de maiúsculas/minúsculas)`);
    }

    // Cria um Map para acesso rápido (Nome Padronizado -> Classe Anterior)
    const mapAnterior = new Map();
    dAnterior.forEach(row => {
      const nomePadronizado = padronizarNome(row[nomeIdxAnterior]);
      if (nomePadronizado) {
        // Armazena a classe E o nome original (para a saída)
        mapAnterior.set(nomePadronizado, {
          Classe: row[classeIdxAnterior] || null,
          NomeOriginal: row[nomeIdxAnterior] 
        });
      }
    });
    Logger.log(`Versão Anterior carregada: ${mapAnterior.size} registros únicos.`);


    // --- 3. Leitura e Preparação da Versão Atual ---
    const { header: hAtual, data: dAtual, nomeIdx: nomeIdxAtual, classeIdx: classeIdxAtual } = 
        getDadosComCabecalho(abaAtual, COLUNA_CHAVE, COLUNA_CLASSE_ATUAL);
    
    // Revalidação com os novos índices
    if (nomeIdxAtual === -1 || classeIdxAtual === -1) {
      throw new Error(`Colunas chave ('${COLUNA_CHAVE}' e '${COLUNA_CLASSE_ATUAL}') não encontradas na Versão Atual.`);
    }
    
    // Lista de objetos da Versão Atual para iteração
    const listAtual = [];
    dAtual.forEach(row => {
        const nomePadronizado = padronizarNome(row[nomeIdxAtual]);
        if (nomePadronizado) {
            listAtual.push({
                NomePadronizado: nomePadronizado,
                Classe: row[classeIdxAtual] || null,
                NomeOriginal: row[nomeIdxAtual]
            });
        }
    });
    Logger.log(`Versão Atual carregada: ${listAtual.length} registros.`);


    // --- 4. Merge e Análise (Simulação de Outer Merge) ---
    Logger.log('Realizando merge e análise de discrepância...');

    const comparativoCompleto = [];
    const nomesJaProcessados = new Set();
    const nomeColunaClasseAnterior = 'Classe_Anterior'; 
    const nomeColunaClasseAtual = 'Classe_Atual'; 
    
    // Cabeçalho de saída
    const headerCompleto = ['Nome', nomeColunaClasseAnterior, nomeColunaClasseAtual, 'Existe_na_Anterior', 'Existe_na_Atual', 'Discrepancia_Classe'];
    comparativoCompleto.push(headerCompleto);
    
    // 4.1. Processa a Versão Atual e faz o merge
    listAtual.forEach(itemAtual => {
      const nomeP = itemAtual.NomePadronizado;
      const anterior = mapAnterior.get(nomeP);
      
      // As classes precisam ser tratadas como strings antes da comparação
      const classeAtual = String(itemAtual.Classe || '').trim();
      const classeAnterior = String(anterior ? anterior.Classe : '').trim();
      
      const existeAnterior = !!anterior;
      const existeAtual = true;
      
      // A discrepância só é verificada se existir nas duas bases e as classes forem diferentes (após trimming)
      const classesDiferentes = classeAnterior !== classeAtual;
      const discrepancia = existeAnterior && existeAtual && classesDiferentes;
      
      // Cria a linha de resultado
      comparativoCompleto.push([
        itemAtual.NomeOriginal,
        classeAnterior,
        classeAtual,
        existeAnterior,
        existeAtual,
        discrepancia
      ]);
      
      nomesJaProcessados.add(nomeP);
    });

    // 4.2. Processa os itens que estavam APENAS na Versão Anterior
    mapAnterior.forEach((itemAnterior, nomeP) => {
      if (!nomesJaProcessados.has(nomeP)) {
        // Item estava na Versão Anterior, mas não na Versão Atual
        comparativoCompleto.push([
          itemAnterior.NomeOriginal,
          String(itemAnterior.Classe || '').trim(),
          '', // Classe Atual é vazia/nula
          true,
          false, // Não existe na Atual
          false  // Não é considerado discrepância (só existe em uma versão)
        ]);
      }
    });


    // --- 5. Filtrar e Gravar Resultados ---
    Logger.log('Gravando resultados na Planilha de Saída...');
    
    // 5.1. Filtrar Discrepâncias
    const discrepanciasFiltradas = comparativoCompleto.filter((row, index) => {
        // Pula o cabeçalho (index 0)
        if (index === 0) return false;
        // Retorna apenas as linhas onde a coluna 'Discrepancia_Classe' é TRUE (índice 5)
        return row[5] === true;
    });
    
    // Adiciona o cabeçalho ao array de discrepâncias
    const discrepanciasOutput = [headerCompleto, ...discrepanciasFiltradas];


    // 5.2. Gravar no arquivo de Saída
    
    // Gravar Comparativo Completo
    let abaComparativo = planilhaSaida.getSheetByName(NOME_ABA_COMPARATIVO);
    if (!abaComparativo) abaComparativo = planilhaSaida.insertSheet(NOME_ABA_COMPARATIVO);
    abaComparativo.clearContents();
    abaComparativo.getRange(1, 1, comparativoCompleto.length, headerCompleto.length).setValues(comparativoCompleto);
    abaComparativo.setFrozenRows(1);
    
    // Gravar Discrepâncias
    let abaDiscrepancias = planilhaSaida.getSheetByName(NOME_ABA_DISCREPANCIAS);
    if (!abaDiscrepancias) abaDiscrepancias = planilhaSaida.insertSheet(NOME_ABA_DISCREPANCIAS);
    abaDiscrepancias.clearContents();
    
    // Só grava se houverem discrepâncias além do cabeçalho
    if (discrepanciasOutput.length > 1) {
        abaDiscrepancias.getRange(1, 1, discrepanciasOutput.length, headerCompleto.length).setValues(discrepanciasOutput);
    } else {
        // Garante que o cabeçalho seja gravado mesmo que não haja discrepâncias
        abaDiscrepancias.getRange(1, 1, 1, headerCompleto.length).setValues([headerCompleto]);
    }
    abaDiscrepancias.setFrozenRows(1);

    
    Logger.log(`✅ Análise Concluída! Total de ${discrepanciasFiltradas.length} discrepâncias de classe encontradas.`);

  } catch (e) {
    Logger.log(`❌ ERRO FATAL na análise de discrepância: ${e.toString()}`);
    throw e;
  }
}