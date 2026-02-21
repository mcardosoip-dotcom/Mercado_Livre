// ====================================================================
// GOOGLE APPS SCRIPT - GERAÇÃO DE PDFs A PARTIR DE PLANILHA
// EXECUÇÃO: rode a função runPdfGenerator()
// ====================================================================

/**
 * Função principal para executar o gerador de PDFs
 */
function runPdfGenerator() {
  PDF_GENERATOR.run()
}

const PDF_GENERATOR = (() => {
  // ====================================================================
  // CONFIGURAÇÕES
  // ====================================================================
  const CONFIG = {
    // IDs da planilha e aba de origem
    SHEET_ID: "1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI",
    SHEET_NAME: "EMBARGAR",

    // IDs dos templates do Google Docs para cada tipo de PDF
    TEMPLATE_COM_SALDO_ID: "1mOyVIlLwh_OacDfRbxJsQjr34yxrECrJJijFdD36vx4",
    TEMPLATE_SALDO_ZERO_ID: "13Re7IcqYgytAgClR1LdpBuOuGkzz2ZZFG4EMuTxYuB8",
    TEMPLATE_MARKET_FOND_ID: "13Re7IcqYgytAgClR1LdpBuOuGkzz2ZZFG4EMuTxYuB8",

    // IDs das pastas do Google Drive onde os PDFs serão salvos
    FOLDER_COM_SALDO_ID: "1pkdoMkXljhS0yEEi-CV8t4Ct_HJdnn_p",
    FOLDER_SEM_SALDO_ID: "1oJzt3p1xczU_6TCgf_Ss6zSD_9DIFwo9",
    FOLDER_MARKET_FOND_ID: "1KO8G-sk5SFWPrdtbvyM5PeKem_up9IMh",

    // Índices das colunas na planilha (baseado em 0)
    MARKET_FOND_COLUMN_INDEX: 15,        // Coluna P
    AMOUNT_AVAILABLE_COLUMN_INDEX: 27,    // Coluna AB (DEB_DEBT_PAID_AMOUNT)

    // Mapeamento de nomes de colunas de valor para padronização
    // Todas essas colunas serão tratadas como "valor_somado"
    VALUE_COLUMN_MAP: {
      valor_somado: "valor_somado",
      monto_disponible: "valor_somado",
      total_amount: "valor_somado",
      amount_total: "valor_somado",
      valor_total: "valor_somado",
    },

    // Nomes das colunas chave (após normalização)
    CHAVE_ISSUE: "issue",
    CHAVE_METADATA: "metadata",

    // Campos obrigatórios que serão extraídos da primeira linha de cada grupo
    REQUIRED_FIRST_ROW_KEYS: [
      "seizing_entity",  // Entidade que está embargando
      "cause",           // Causa do embargo
      "case_number",     // Número do caso
      "tax_id",          // CPF/CNPJ
    ],
  }

  // ====================================================================
  // FUNÇÃO PRINCIPAL DE EXECUÇÃO
  // ====================================================================

  /**
   * Função principal que orquestra todo o processo de geração de PDFs
   */
  function run() {
    try {
      Logger.log("=== INÍCIO DA EXECUÇÃO ===")

      // 1. Carregar e preparar os dados da planilha
      const data = loadAndPrepareData()
      if (!data.length) {
        Logger.log("Nenhuma linha para processar")
        return
      }

      // 2. Agrupar dados por ISSUE e calcular totais
      const grouped = groupAndAggregate(data)

      // 3. Gerar e exportar os PDFs
      generateAndExportPdfs(grouped)

      // 4. Chamar webhook Verdi após conclusão do processo
      callVerdiWebhook(grouped.size)

      Logger.log("=== FIM DA EXECUÇÃO ===")
    } catch (e) {
      Logger.log(`ERRO FATAL: ${e.message}`)
      Logger.log(e.stack)
      throw e
    }
  }

  // ====================================================================
  // CARREGAMENTO E PREPARAÇÃO DE DADOS
  // ====================================================================

  /**
   * Carrega os dados da planilha e os prepara para processamento
   * @returns {Array} Array de objetos com os dados normalizados
   */
  function loadAndPrepareData() {
    // Abrir a planilha e aba especificadas
    const sheet = SpreadsheetApp
      .openById(CONFIG.SHEET_ID)
      .getSheetByName(CONFIG.SHEET_NAME)

    if (!sheet) {
      throw new Error("Aba não encontrada")
    }

    // Obter todos os dados da planilha
    const values = sheet.getDataRange().getValues()
    
    // Primeira linha são os cabeçalhos - normalizar nomes das colunas
    const header = values[0].map(normalizeCol)
    
    // Restante são os dados (sem o cabeçalho)
    const rows = values.slice(1)

    // Validar que a coluna ISSUE existe
    if (!header.includes(CONFIG.CHAVE_ISSUE)) {
      throw new Error("Coluna ISSUE não encontrada")
    }

    // Normalizar nomes das colunas de valor para "valor_somado"
    let valueColumnFound = false
    Object.keys(CONFIG.VALUE_COLUMN_MAP).forEach(columnName => {
      const columnIndex = header.indexOf(columnName)
      if (columnIndex !== -1) {
        header[columnIndex] = CONFIG.VALUE_COLUMN_MAP[columnName]
        valueColumnFound = true
      }
    })

    if (!valueColumnFound) {
      throw new Error("Coluna de valor não encontrada")
    }

    // Converter cada linha em um objeto com propriedades nomeadas
    return rows.map(row => {
      const rowObject = {}
      
      // Mapear cada coluna do cabeçalho para o valor correspondente
      header.forEach((columnName, index) => {
        rowObject[columnName] = row[index]
      })
      
      // Adicionar valores brutos das colunas especiais (antes da normalização)
      rowObject.__market_fond_raw = row[CONFIG.MARKET_FOND_COLUMN_INDEX]
      rowObject.__amount_available_raw = row[CONFIG.AMOUNT_AVAILABLE_COLUMN_INDEX]
      
      return rowObject
    })
  }

  /**
   * Normaliza o nome de uma coluna para formato padrão
   * Remove acentos, converte para minúsculas, substitui espaços por underscore
   * @param {string} col - Nome da coluna original
   * @returns {string} Nome da coluna normalizado
   */
  function normalizeCol(col) {
    return String(col)
      .trim()                                    // Remove espaços no início/fim
      .toLowerCase()                             // Converte para minúsculas
      .normalize("NFD")                          // Decompõe caracteres acentuados
      .replace(/[\u0300-\u036f]/g, "")          // Remove diacríticos (acentos)
      .replace(/\s+/g, "_")                       // Substitui espaços por underscore
      .replace(/[^a-z0-9_]/g, "")                // Remove caracteres especiais
  }

  // ====================================================================
  // AGRUPAMENTO E AGREGAÇÃO DE DADOS
  // ====================================================================

  /**
   * Agrupa os dados por ISSUE e calcula totais e contagens
   * @param {Array} data - Array de objetos com os dados das linhas
   * @returns {Map} Map com ISSUE como chave e dados agregados como valor
   */
  function groupAndAggregate(data) {
    const grouped = new Map()

    data.forEach(row => {
      // Extrair e validar o ISSUE
      const issue = String(row[CONFIG.CHAVE_ISSUE] || "").trim()
      
      // Pular linhas sem ISSUE válido
      if (!issue || issue === "" || issue === "undefined" || issue === "null") {
        return
      }
      
      // Extrair valores numéricos
      const valorSomado = parseFloat(row.valor_somado) || 0
      const marketFond = toBoolean(row.__market_fond_raw)
      const amountAvailable = parseFloat(row.__amount_available_raw) || 0

      // Se é a primeira linha deste ISSUE, criar o grupo
      if (!grouped.has(issue)) {
        // Extrair campos obrigatórios da primeira linha do grupo
        const firstRow = {}
        CONFIG.REQUIRED_FIRST_ROW_KEYS.forEach(key => {
          firstRow[key] = row[key] ?? ""
        })
        
        // Adicionar informações especiais
        firstRow.market_fond = marketFond
        firstRow.amount_available = amountAvailable

        // Criar estrutura do grupo
        grouped.set(issue, {
          issue: issue,
          firstRow: firstRow,
          totalValorSomado: 0,
          uniqueUserIds: new Set(),
        })
      }

      // Adicionar valor ao total do grupo
      const group = grouped.get(issue)
      group.totalValorSomado += valorSomado

      // Extrair USER_IDs únicos do metadata (se existir)
      if (row[CONFIG.CHAVE_METADATA]) {
        extractUserIdsFromMetadata(row[CONFIG.CHAVE_METADATA], group.uniqueUserIds)
      }
    })

    return grouped
  }

  /**
   * Converte um valor para booleano
   * Aceita: true, "true", "sim", "1", "yes", "y"
   * @param {*} value - Valor a ser convertido
   * @returns {boolean} Valor booleano
   */
  function toBoolean(value) {
    if (value === true) return true
    
    const stringValue = String(value).trim().toLowerCase()
    return stringValue === "true" || 
           stringValue === "sim" || 
           stringValue === "1" || 
           stringValue === "yes" || 
           stringValue === "y"
  }

  /**
   * Extrai USER_IDs únicos do campo metadata (JSON)
   * @param {string} metadataStr - String JSON com os metadados
   * @param {Set} userIdSet - Set onde os USER_IDs serão adicionados
   */
  function extractUserIdsFromMetadata(metadataStr, userIdSet) {
    try {
      const metadata = JSON.parse(metadataStr)
      
      if (metadata && metadata.user_data) {
        // Extrair USER_IDs de "subsidy" e "market_fond"
        ["subsidy", "market_fond"].forEach(key => {
          if (Array.isArray(metadata.user_data[key])) {
            metadata.user_data[key].forEach(item => {
              if (item && item.user_id) {
                userIdSet.add(item.user_id)
              }
            })
          }
        })
      }
    } catch (error) {
      // Ignorar erros de parsing JSON
    }
  }

  // ====================================================================
  // GERAÇÃO E EXPORTAÇÃO DE PDFs
  // ====================================================================

  /**
   * Remove da pasta todos os arquivos com o mesmo nome do PDF (exato ou duplicados (1), (2), etc.)
   * Assim o novo PDF substitui o anterior em vez de criar cópias.
   * @param {Folder} folder - Pasta do Drive
   * @param {string} pdfName - Nome do arquivo (ex: "ISSUE123.pdf")
   */
  function removeExistingFilesByName(folder, pdfName) {
    const baseName = pdfName.replace(/\.pdf$/i, "")
    const duplicatePattern = new RegExp("^" + escapeRegex(baseName) + "\\s*\\(\\d+\\)\\.pdf$", "i")

    // Remover arquivo com nome exato
    const exactFiles = folder.getFilesByName(pdfName)
    while (exactFiles.hasNext()) {
      exactFiles.next().setTrashed(true)
    }

    // Remover duplicados do tipo "nome (1).pdf", "nome (2).pdf", etc.
    const allFiles = folder.getFiles()
    while (allFiles.hasNext()) {
      const file = allFiles.next()
      if (duplicatePattern.test(file.getName())) {
        file.setTrashed(true)
      }
    }
  }

  /**
   * Gera e exporta os PDFs para as pastas apropriadas
   * @param {Map} groupedData - Map com dados agrupados por ISSUE
   */
  function generateAndExportPdfs(groupedData) {
    // Formatar data atual no formato brasileiro
    const today = Utilities.formatDate(
      new Date(),
      Session.getScriptTimeZone(),
      "dd 'de' MMMM 'de' yyyy"
    )

    // Obter referências às pastas de destino
    const folderComSaldo = DriveApp.getFolderById(CONFIG.FOLDER_COM_SALDO_ID)
    const folderSemSaldo = DriveApp.getFolderById(CONFIG.FOLDER_SEM_SALDO_ID)
    const folderMarketFond = DriveApp.getFolderById(CONFIG.FOLDER_MARKET_FOND_ID)

    Logger.log(`Total de issues a processar: ${groupedData.size}`)

    // Processar cada grupo (ISSUE)
    groupedData.forEach(group => {
      const { issue, firstRow, totalValorSomado, uniqueUserIds } = group

      // Validar ISSUE
      const issueTrimmed = String(issue || "").trim()
      if (!issueTrimmed || 
          issueTrimmed === "" || 
          issueTrimmed === "undefined" || 
          issueTrimmed === "null") {
        Logger.log(`PULADO | ISSUE vazia ou inválida: "${issue}"`)
        return
      }

      // Determinar qual template e pasta usar baseado no amount_available
      const amountAvailable = firstRow.amount_available || 0
      let templateId
      let outputFolder
      let regra

      if (amountAvailable > 0) {
        // Saldo positivo: usar template "com saldo"
        templateId = CONFIG.TEMPLATE_COM_SALDO_ID
        outputFolder = folderComSaldo
        regra = "COM_SALDO"
      } else if (amountAvailable < 0) {
        // Saldo negativo: usar template "market fond"
        templateId = CONFIG.TEMPLATE_MARKET_FOND_ID
        outputFolder = folderMarketFond
        regra = "MARKET_FOND"
      } else {
        // Saldo zero: usar template "sem saldo"
        templateId = CONFIG.TEMPLATE_SALDO_ZERO_ID
        outputFolder = folderSemSaldo
        regra = "SEM_SALDO"
      }

      const pdfName = `${issueTrimmed}.pdf`

      Logger.log(
        `ISSUE=${issueTrimmed} | total=${totalValorSomado} | amount_available=${amountAvailable} | ` +
        `regra=${regra} | pasta=${outputFolder.getId()} | arquivo=${pdfName} | users=${uniqueUserIds.size}`
      )

      // Preparar substituições de texto no template
      const replacements = {
        "[hoje]": today,
        "[seizing_entity]": firstRow.seizing_entity,
        "[cause]": firstRow.cause,
        "[case_number]": firstRow.case_number,
        "[tax_id]": firstRow.tax_id,
        "[Count_user_ID]": String(uniqueUserIds.size),
        "[valor_somado]": formatCurrency(totalValorSomado),
      }

      try {
        // 1. Remover PDFs existentes com o mesmo nome na pasta (evita duplicados (1), (2))
        removeExistingFilesByName(outputFolder, pdfName)

        // 2. Obter o template
        const template = DriveApp.getFileById(templateId)
        
        // 3. Criar uma cópia temporária do template
        const tempDoc = template.makeCopy(`TEMP_${issueTrimmed}_${Date.now()}`, outputFolder)
        const doc = DocumentApp.openById(tempDoc.getId())

        // 4. Substituir os placeholders no documento
        replaceTextInDocument(doc, replacements)
        doc.saveAndClose()
        
        // 5. Aguardar um pouco para garantir que o documento foi salvo
        Utilities.sleep(800)

        // 6. Converter para PDF
        const pdf = tempDoc.getAs(MimeType.PDF)
        pdf.setName(pdfName)
        
        // 7. Salvar o PDF na pasta de destino (substitui o anterior se existia)
        outputFolder.createFile(pdf)

        // 8. Excluir o documento temporário
        tempDoc.setTrashed(true)

        Logger.log(`GERADO_COM_SUCESSO | ISSUE=${issueTrimmed} | arquivo=${pdfName}`)
      } catch (error) {
        Logger.log(`ERRO_GERACAO | ISSUE=${issueTrimmed} | erro=${error.message}`)
      }
    })
  }

  /**
   * Substitui placeholders no documento do Google Docs
   * Procura no corpo do documento e em todas as tabelas
   * @param {Document} doc - Documento do Google Docs
   * @param {Object} replacements - Objeto com chave-valor dos placeholders e valores
   */
  function replaceTextInDocument(doc, replacements) {
    const body = doc.getBody()

    // Substituir no corpo do documento
    Object.keys(replacements).forEach(placeholder => {
      const escapedPlaceholder = escapeRegex(placeholder)
      const replacementValue = String(replacements[placeholder] ?? "")
      body.replaceText(escapedPlaceholder, replacementValue)
    })

    // Substituir em todas as tabelas
    const tables = body.getTables()
    for (let tableIndex = 0; tableIndex < tables.length; tableIndex++) {
      const table = tables[tableIndex]
      
      for (let rowIndex = 0; rowIndex < table.getNumRows(); rowIndex++) {
        const row = table.getRow(rowIndex)
        
        for (let cellIndex = 0; cellIndex < row.getNumCells(); cellIndex++) {
          const cell = row.getCell(cellIndex)
          
          Object.keys(replacements).forEach(placeholder => {
            const escapedPlaceholder = escapeRegex(placeholder)
            const replacementValue = String(replacements[placeholder] ?? "")
            cell.replaceText(escapedPlaceholder, replacementValue)
          })
        }
      }
    }
  }

  /**
   * Escapa caracteres especiais para uso em expressões regulares
   * @param {string} str - String a ser escapada
   * @returns {string} String com caracteres especiais escapados
   */
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  }

  // ====================================================================
  // WEBHOOK VERDI
  // ====================================================================

  const WEBHOOK_VERDI_URL = "http://verdi-flows.melisystems.com/webhook/32314d9b-064d-42c2-91b7-5f8a2dfb1a17"

  /**
   * Chama o webhook Verdi após a conclusão da geração de PDFs
   * @param {number} pdfCount - Quantidade de PDFs gerados
   */
  function callVerdiWebhook(pdfCount) {
    try {
      const payload = JSON.stringify({
        source: "MeliTRigger_PDF_Generator",
        status: "completed",
        pdf_count: pdfCount,
        timestamp: new Date().toISOString(),
      })

      const options = {
        method: "post",
        contentType: "application/json",
        payload: payload,
        muteHttpExceptions: true,
      }

      const response = UrlFetchApp.fetch(WEBHOOK_VERDI_URL, options)
      Logger.log(`Webhook Verdi chamado | status=${response.getResponseCode()} | PDFs gerados=${pdfCount}`)
    } catch (e) {
      Logger.log(`ERRO ao chamar webhook Verdi: ${e.message}`)
      // Não interrompe o fluxo - o processo de PDF já foi concluído
    }
  }

  // ====================================================================
  // UTILITÁRIOS
  // ====================================================================

  /**
   * Formata um número como moeda brasileira (R$ X.XXX,XX)
   * @param {number} num - Número a ser formatado
   * @returns {string} Número formatado como moeda
   */
  function formatCurrency(num) {
    const number = Number(num)
    
    if (!isFinite(number)) {
      return "0,00"
    }
    
    // Converter para string com 2 casas decimais
    const [integerPart, decimalPart] = number.toFixed(2).split(".")
    
    // Adicionar separadores de milhar (pontos) e vírgula para decimais
    return `${integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".")},${decimalPart}`
  }

  // ====================================================================
  // EXPOSIÇÃO DA API PÚBLICA
  // ====================================================================

  return { run }
})()
