function copiarTodasAsBases() {
  // ============================
  // 1) ARQUIVOS E ABAS DO PRIMEIRO BLOCO
  // ============================
  const ORIGEM_1 = "1uTfJZtBL2O2Hk525NnQJCsObxWaohueD77dMArOK25U";
  const DESTINO_1 = "1Ro5If85-7E--0At8q0SamKsR-mnVlJgwIY5YBRwpKJE";

  // Lista de todas as abas para COPIAR
  const ABAS_1 = [
    "Base People",
    "Base de estrangeiros",
    "Base Exceção a classe",
    "Base Jurídico",
    "Base de novos pedidos"
  ];

  // Lista de abas para FORMATAR CPF (Coluna C)
  // * "Base de estrangeiros" foi removida intencionalmente desta lista
  const ABAS_PARA_FORMATAR_CPF = [
    "Base People",
    "Base Exceção a classe",
    "Base Jurídico",
    "Base de novos pedidos"
  ];

  // ============================
  // 2) ARQUIVOS E ABAS DO SEGUNDO BLOCO
  // ============================
  const ORIGEM_2 = "1L1wFbtA3MKvV4FrnGXTSDH3RhMYm3y4yYB2d-sLrzD4";
  const DESTINO_2 = "1EohsmWblwSVujLowqe1025y4Y3T6sgvs-V6NtPIuRIU";

  const ABAS_2 = ["Regras"];

  // --- EXECUÇÃO ---

  // 1. Executa cópia do Bloco 1 (Copia todas, inclusive estrangeiros)
  copiarAbas(ORIGEM_1, DESTINO_1, ABAS_1);
  
  // 2. APLICA A FORMATAÇÃO DE CPF (Loop nas abas selecionadas)
  // Aplica na coluna C (índice 3)
  Logger.log("--- Iniciando formatação de CPFs ---");
  ABAS_PARA_FORMATAR_CPF.forEach(nomeAba => {
      formatarColunaCpf(DESTINO_1, nomeAba, 3);
  });

  // 3. Executa cópia do Bloco 2
  copiarAbas(ORIGEM_2, DESTINO_2, ABAS_2);

  Logger.log("✔ Processo concluído: Cópia e formatação finalizadas.");
}

// =======================================================
// FUNÇÃO DE FORMATAÇÃO → Limpa caracteres e aplica máscara CPF
// =======================================================
function formatarColunaCpf(idPlanilha, nomeAba, numColuna) {
  try {
    const ss = SpreadsheetApp.openById(idPlanilha);
    const aba = ss.getSheetByName(nomeAba);
    
    if (!aba) {
      Logger.log("⚠️ Aba não encontrada para formatar CPF: " + nomeAba);
      return;
    }

    const lastRow = aba.getLastRow();
    if (lastRow < 2) return; // Se só tiver cabeçalho ou estiver vazia

    // Define o intervalo da coluna (da linha 2 até a última)
    const range = aba.getRange(2, numColuna, lastRow - 1, 1);
    
    // 1. Limpeza: Pega os valores e remove tudo que não for número
    const values = range.getValues();
    const cleanValues = values.map(row => {
      let val = row[0];
      if (val) {
        // Converte para string e remove tudo que não é dígito (pontos, traços, espaços)
        val = val.toString().replace(/\D/g, ""); 
      }
      return [val];
    });
    
    // Devolve os valores limpos (apenas números) para a planilha
    range.setValues(cleanValues);

    // 2. Aplica a formatação visual personalizada
    // Máscara: 000.000.000-00 (adiciona zeros à esquerda se necessário)
    range.setNumberFormat('000"."000"."000"-"00');

    Logger.log("✓ CPF limpo e formatado na aba: " + nomeAba);

  } catch (e) {
    Logger.log("❌ Erro ao formatar CPF na aba " + nomeAba + ": " + e);
  }
}

// =======================================================
// FUNÇÃO GENÉRICA → copia abas entre arquivos
// =======================================================
function copiarAbas(ORIGEM_ID, DESTINO_ID, ABAS) {
  try {
    const ssOrigem = SpreadsheetApp.openById(ORIGEM_ID);
    const ssDestino = SpreadsheetApp.openById(DESTINO_ID);

    ABAS.forEach(nomeAba => {
      const abaOrigem = ssOrigem.getSheetByName(nomeAba);
      let abaDestino = ssDestino.getSheetByName(nomeAba);

      if (!abaOrigem) {
        Logger.log("⚠️ Aba não encontrada na origem: " + nomeAba);
        return;
      }

      // Se não existir no destino, cria
      if (!abaDestino) {
        // Logger.log("⚠️ Aba não encontrada no destino. Criando: " + nomeAba);
        ssDestino.insertSheet(nomeAba);
        abaDestino = ssDestino.getSheetByName(nomeAba);
      }

      // Limpa conteúdo anterior
      abaDestino.clearContents();
      abaDestino.clearFormats();

      // Copia valores e formatos
      const rangeOrigem = abaOrigem.getDataRange();
      const valores = rangeOrigem.getValues();
      const formatos = rangeOrigem.getNumberFormats();

      // Ajusta tamanho da área destino
      if (valores.length > 0) {
        abaDestino
          .getRange(1, 1, valores.length, valores[0].length)
          .setValues(valores);

        abaDestino
          .getRange(1, 1, formatos.length, formatos[0].length)
          .setNumberFormats(formatos);
      }

      Logger.log("✓ Aba copiada: " + nomeAba);
    });

  } catch (e) {
    Logger.log("❌ Erro ao processar arquivo: " + e);
    throw e;
  }
}