function listarPdfsDeMultiplasPastasNaPlanilhaExterna() {
  // === CONFIGURAÇÕES PRINCIPAIS ===
  const ID_PLANILHA_DESTINO = "1CduJIS32Ua5VTIWyqsQPp2LkthAWDupR75sVitbLEjI";
  const NOME_ABA = "Arquivos_PDFS_gerados";

  // Pasta única de PDFs (Unico - modelo unificado)
  const PASTAS_CONFIG = [
    { id: "1or_byHSfd8-26ghf_g7Opp4hRxLuN59r", label: "Unico" }
  ];

  try {
    const planilha = SpreadsheetApp.openById(ID_PLANILHA_DESTINO);
    const aba = planilha.getSheetByName(NOME_ABA);

    if (!aba) {
      throw new Error(`A aba '${NOME_ABA}' não foi encontrada na planilha externa. Crie-a antes de executar.`);
    }

    // Cabeçalho fixo
    aba.getRange("A1:B1").setValues([["Status", "Nome do Arquivo PDF"]]);

    // Limpa a aba (exceto cabeçalho) para sempre trazer informação atual da pasta de rede
    const lastRowAntes = aba.getLastRow();
    if (lastRowAntes > 1) {
      aba.getRange(2, 1, lastRowAntes, 2).clearContent();
      aba.getRange(2, 1, lastRowAntes, 2).clearFormat();
    }

    Logger.log(`--- Iniciando listagem de PDFs na planilha '${planilha.getName()}' aba '${NOME_ABA}' (lista sempre atual) ---`);

    let totalPdfsEncontrados = 0;

    function processarPasta(folderId, statusLabel) {
      try {
        const pasta = DriveApp.getFolderById(folderId);
        const arquivos = pasta.getFiles();

        Logger.log(`Pasta: ${pasta.getName()} [${statusLabel}]`);

        while (arquivos.hasNext()) {
          const arquivo = arquivos.next();
          if (arquivo.getMimeType() === MimeType.PDF) {
            totalPdfsEncontrados++;
            const nome = arquivo.getName();
            aba.appendRow([statusLabel, nome]);
          }
        }
      } catch (err) {
        Logger.log(`Erro ao acessar pasta [${folderId}]: ${err.message}`);
        aba.appendRow([statusLabel, `ERRO: Não foi possível listar arquivos. (${err.message})`]);
      }
    }

    PASTAS_CONFIG.forEach(cfg => processarPasta(cfg.id, cfg.label));

    if (totalPdfsEncontrados > 0) {
      Logger.log(`${totalPdfsEncontrados} PDFs listados (lista atual das pastas).`);
    } else {
      Logger.log("Nenhum arquivo PDF encontrado nas pastas configuradas.");
    }

    planilha.setActiveSheet(aba);
    aba.activate();

    Logger.log("--- Listagem concluída e aba 'Arquivos_PDFS_gerados' selecionada ---");
  } catch (e) {
    Logger.log(`Erro geral: ${e.message}`);
  }
}
