function copiarDadosDaPlanilhaExterna() {
  const LINK_PLANILHA_PRINCIPAL = 'https://docs.google.com/spreadsheets/d/1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI/edit';
  const PLANILHA_PRINCIPAL_ID = extrairIdDaUrl(LINK_PLANILHA_PRINCIPAL);

  const NOME_ABA_QUERY_SOURCE = "Query_Suporte_Resultado";
  const NOME_ABA_REVISAO = "Revisão_manual";
  const NOME_ABA_DESTINO = "EMBARGAR";
  const NOME_ABA_PARAMETRO = "Parametros";

  const INDEX_E = 4;
  const INDEX_F = 5;
  const INDEX_G = 6;
  const INDEX_J = 9;
  const INDEX_MARKET_FOND = 15;
  const COLUNA_QTD_INDEX = 22;
  const INDEX_X = 23;

  const planilhaAtual = SpreadsheetApp.openById(PLANILHA_PRINCIPAL_ID);

  const abaEmbargarDestino = planilhaAtual.getSheetByName(NOME_ABA_DESTINO);
  if (!abaEmbargarDestino) {
    throw new Error("A aba 'EMBARGAR' não foi encontrada.");
  }

  const abaRevisaoManual =
    planilhaAtual.getSheetByName(NOME_ABA_REVISAO) || planilhaAtual.insertSheet(NOME_ABA_REVISAO);

  if (abaRevisaoManual.getLastRow() > 1) {
    abaRevisaoManual
      .getRange(2, 1, abaRevisaoManual.getLastRow() - 1, abaRevisaoManual.getLastColumn())
      .clearContent();
  }

  const abaQuerySuporte = planilhaAtual.getSheetByName(NOME_ABA_QUERY_SOURCE);
  let dadosSuporte = null;

  if (abaQuerySuporte && abaQuerySuporte.getLastRow() > 0) {
    dadosSuporte = abaQuerySuporte
      .getRange(1, 1, abaQuerySuporte.getLastRow(), abaQuerySuporte.getLastColumn())
      .getValues();
  }

  const abaParametro = planilhaAtual.getSheetByName(NOME_ABA_PARAMETRO);
  if (!abaParametro) {
    throw new Error("A aba 'Parametros' não foi encontrada.");
  }

  const linkPlanilhaExterna = abaParametro.getRange("B3").getValue();
  if (!linkPlanilhaExterna) {
    throw new Error("Parâmetro B3 vazio.");
  }

  const planilhaExternaId = extrairIdDaUrl(linkPlanilhaExterna);
  const planilhaExterna = SpreadsheetApp.openById(planilhaExternaId);
  const abaEmbargarOrigem = planilhaExterna.getSheetByName("EMBARGAR");

  if (!abaEmbargarOrigem) {
    throw new Error("A aba 'EMBARGAR' não existe na planilha externa.");
  }

  if (abaEmbargarDestino.getLastRow() > 0) {
    abaEmbargarDestino.getRange(1, 1, abaEmbargarDestino.getLastRow(), 25).clearContent();
  }

  const valoresCopiados = abaEmbargarOrigem
    .getRange(1, 1, abaEmbargarOrigem.getLastRow(), abaEmbargarOrigem.getLastColumn())
    .getValues();

  abaEmbargarDestino
    .getRange(1, 1, valoresCopiados.length, valoresCopiados[0].length)
    .setValues(valoresCopiados);

  // Limpar linhas sem informações necessárias nas colunas A e Q
  const ultimaLinhaAntesLimpeza = abaEmbargarDestino.getLastRow();
  if (ultimaLinhaAntesLimpeza > 1) {
    const dadosParaLimpeza = abaEmbargarDestino
      .getRange(1, 1, ultimaLinhaAntesLimpeza, abaEmbargarDestino.getLastColumn())
      .getValues();
    
    const COLUNA_A_INDEX = 0; // Coluna A (índice 0)
    const COLUNA_Q_INDEX = 16; // Coluna Q (índice 16)
    const linhasParaManter = [];
    const linhasParaRemover = [];
    
    for (let i = 0; i < dadosParaLimpeza.length; i++) {
      if (i === 0) {
        // Sempre manter o cabeçalho
        linhasParaManter.push(dadosParaLimpeza[i]);
        continue;
      }
      
      const valorColunaA = dadosParaLimpeza[i][COLUNA_A_INDEX];
      const valorColunaQ = dadosParaLimpeza[i][COLUNA_Q_INDEX];
      
      // Verificar se as colunas A e Q estão vazias ou sem informação necessária
      const colunaAVazia = !valorColunaA || 
                           String(valorColunaA).trim() === "" || 
                           String(valorColunaA).toLowerCase() === "null" ||
                           String(valorColunaA).toLowerCase() === "undefined";
      
      const colunaQVazia = !valorColunaQ || 
                           String(valorColunaQ).trim() === "" || 
                           String(valorColunaQ).toLowerCase() === "null" ||
                           String(valorColunaQ).toLowerCase() === "undefined";
      
      // Se ambas as colunas estiverem vazias, marcar para remoção
      if (colunaAVazia && colunaQVazia) {
        linhasParaRemover.push(i + 1); // +1 porque deleteRow usa índice baseado em 1
      } else {
        linhasParaManter.push(dadosParaLimpeza[i]);
      }
    }
    
    // Remover linhas de trás para frente para não afetar os índices
    for (let i = linhasParaRemover.length - 1; i >= 0; i--) {
      abaEmbargarDestino.deleteRow(linhasParaRemover[i]);
    }
    
    // Reescrever os dados mantidos (incluindo cabeçalho)
    if (linhasParaManter.length > 0) {
      abaEmbargarDestino
        .getRange(1, 1, linhasParaManter.length, linhasParaManter[0].length)
        .setValues(linhasParaManter);
    }
  }

  if (dadosSuporte && dadosSuporte.length > 1) {
    const mapaCalculos = {};

    for (let i = 1; i < dadosSuporte.length; i++) {
      const usuario = dadosSuporte[i][1];
      const valor = parseFloat(String(dadosSuporte[i][3]).replace(/[^0-9\.]+/g, '')) || 0;

      if (usuario) {
        if (!mapaCalculos[usuario]) {
          mapaCalculos[usuario] = { count: 0, totalValor: 0 };
        }
        mapaCalculos[usuario].count++;
        mapaCalculos[usuario].totalValor += valor;
      }
    }

    const dadosEmbargar = abaEmbargarDestino
      .getRange(1, 1, abaEmbargarDestino.getLastRow(), 13)
      .getValues();

    const novosDados = [];
    const USER_ID_INDEX = 12;

    for (let i = 0; i < dadosEmbargar.length; i++) {
      if (i === 0) {
        novosDados.push(["QTD_EMBARGOS", "VALOR_SOMADO"]);
        continue;
      }

      const info = mapaCalculos[dadosEmbargar[i][USER_ID_INDEX]] || { count: 0, totalValor: 0 };
      novosDados.push([info.count, info.totalValor]);
    }

    abaEmbargarDestino
      .getRange(1, 23, novosDados.length, 2)
      .setValues(novosDados);
  }

  // Preencher coluna AB com DEB_DEBT_PAID_AMOUNT quando USER_ID corresponder
  if (dadosSuporte && dadosSuporte.length > 1) {
    const mapaPaidAmount = {};
    
    // Criar mapa: DEB_DEBT_USER_ID (col B, index 1) -> DEB_DEBT_PAID_AMOUNT (col D, index 3)
    for (let i = 1; i < dadosSuporte.length; i++) {
      const debDebtUserId = dadosSuporte[i][1]; // Coluna B
      const debDebtPaidAmount = dadosSuporte[i][3]; // Coluna D
      
      if (debDebtUserId) {
        // Se houver múltiplos registros para o mesmo USER_ID, manter o último valor
        mapaPaidAmount[debDebtUserId] = debDebtPaidAmount;
      }
    }
    
    // Preencher coluna AB (index 27) na aba EMBARGAR
    const ultimaLinhaParaAB = abaEmbargarDestino.getLastRow();
    if (ultimaLinhaParaAB > 1) {
      const dadosEmbargar = abaEmbargarDestino
        .getRange(1, 1, ultimaLinhaParaAB, abaEmbargarDestino.getLastColumn())
        .getValues();
      
      const USER_ID_INDEX = 12; // Coluna M
      const COLUNA_AB_INDEX = 27; // Coluna AB
      const valoresColunaAB = [];
      
      for (let i = 0; i < dadosEmbargar.length; i++) {
        if (i === 0) {
          // Cabeçalho com o nome da coluna
          valoresColunaAB.push(["DEB_DEBT_PAID_AMOUNT"]);
          continue;
        }
        
        const userId = dadosEmbargar[i][USER_ID_INDEX];
        const paidAmount = mapaPaidAmount[userId] || "";
        valoresColunaAB.push([paidAmount]);
      }
      
      // Escrever os valores na coluna AB
      if (valoresColunaAB.length > 0) {
        abaEmbargarDestino
          .getRange(1, COLUNA_AB_INDEX + 1, valoresColunaAB.length, 1)
          .setValues(valoresColunaAB);
      }
    }
  }

  const ultimaLinhaEmbargar = abaEmbargarDestino.getLastRow();
  if (ultimaLinhaEmbargar > 1) {
    const dadosEmbargar = abaEmbargarDestino
      .getRange(1, 1, ultimaLinhaEmbargar, 24)
      .getValues();

    const linhasParaRevisao = [];

    if (abaRevisaoManual.getLastRow() === 0) {
      abaRevisaoManual.appendRow(dadosEmbargar[0]);
    }

    for (let i = dadosEmbargar.length - 1; i >= 1; i--) {
      const linha = dadosEmbargar[i];
      const qtd = linha[COLUNA_QTD_INDEX];
      const marketFond = linha[INDEX_MARKET_FOND];

      if (qtd !== 1 && marketFond === false) {
        linhasParaRevisao.push(linha);
        abaEmbargarDestino.deleteRow(i + 1);
      }
    }

    if (linhasParaRevisao.length > 0) {
      linhasParaRevisao.reverse();
      abaRevisaoManual
        .getRange(
          abaRevisaoManual.getLastRow() + 1,
          1,
          linhasParaRevisao.length,
          linhasParaRevisao[0].length
        )
        .setValues(linhasParaRevisao);
    }
  }

  const ultimaLinhaFinal = abaEmbargarDestino.getLastRow();
  if (ultimaLinhaFinal > 1) {
    const rangeFinal = abaEmbargarDestino
      .getRange(2, 1, ultimaLinhaFinal - 1, abaEmbargarDestino.getLastColumn());

    const dadosFinais = rangeFinal.getValues();

    for (let i = 0; i < dadosFinais.length; i++) {
      dadosFinais[i][INDEX_J] = dadosFinais[i][INDEX_X];

      if (dadosFinais[i][INDEX_E]) dadosFinais[i][INDEX_E] = String(dadosFinais[i][INDEX_E]).toUpperCase();
      if (dadosFinais[i][INDEX_F]) dadosFinais[i][INDEX_F] = String(dadosFinais[i][INDEX_F]).toUpperCase();
      if (dadosFinais[i][INDEX_G]) dadosFinais[i][INDEX_G] = String(dadosFinais[i][INDEX_G]).toUpperCase();
    }

    rangeFinal.setValues(dadosFinais);
  }

  SpreadsheetApp.flush();
}

function extrairIdDaUrl(url) {
  const match = url.match(/\/spreadsheets\/d\/([a-zA-Z0-9_-]+)/);
  return match ? match[1] : null;
}
