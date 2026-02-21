/**
 * Endpoint HTTP para chamada externa (n8n)
 * Aceita POST ou GET
 */
function doPost(e) {
  return handleRequest(e);
}

function doGet(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  try {
    exportSheetsAndClearFolder();
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "ok",
        message: "Processo executado com sucesso"
      }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: "error",
        message: err.message
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Baixa as planilhas e exporta para a pasta de Controle de Pagamentos.
 * Planilhas que não existirem mais são ignoradas (não interrompem o processo).
 */
function exportSheetsAndClearFolder() {

  // Pasta destino: https://drive.google.com/drive/u/0/folders/17RnK9Gigc2T_mElRNuem3-Ej1Pa9CeI7
  const ID_PASTA_DESTINO = "17RnK9Gigc2T_mElRNuem3-Ej1Pa9CeI7";

  const FILES_TO_EXPORT = [
    { nome: "pagamentos_2025_Hisp.xlsx", id: "1DF2YEl4bDkHBi3QkEwHr1ryi9dyTeGlQGSnD7YrhwjE" },
    { nome: "pagamentos_2026_Hisp.xlsx", id: "1QROwrnsCdoJ4iomb6SHjyr4Q7Ujl2rfwklCzn0lu0CY" },
    { nome: "pagamentos_2025_BR.xlsx",   id: "1sM1ZR3J-7RU6gcApjwZKDJjRNsRALwpI9VHDG532rDs" },
    { nome: "pagamentos_2026_BR.xlsx",   id: "1dgZ-crXBkjCC8Or95sJjZ-jvgqOG4NgXj_2aK9CXtH4" },
    { nome: "valores.xlsx",              id: "1FsXvhVSUpCc601IohIv3VukHRbnDV4SV8YidyPjiE9s" },
    { nome: "honorarios_brasil.xlsx",    id: "1XV3PniKJUftYcWnPgFqjjTmGNWMzVflBuW1sOUVvKog" },
    { nome: "contingencias_brasil.xlsx", id: "1a6YkqfXZSjKzrM6Plujga2X2HjwscCld6weOQbOjR9Y" },
    { nome: "contingencias_hisp.xlsx",   id: "1FW1DxXoUxlKsvaMs4_VsnQRTStDSgYCPj1fJcKAfCIw" }
  ];

  const token = ScriptApp.getOAuthToken();
  const folder = DriveApp.getFolderById(ID_PASTA_DESTINO);

  // Limpa apenas a pasta destino
  const files = folder.getFiles();
  while (files.hasNext()) {
    try {
      const file = files.next();
      file.setTrashed(true);
    } catch (fileErr) {
      Logger.log("Arquivo ignorado ao limpar: " + (fileErr && fileErr.message));
    }
  }

  // Exporta cada planilha; se não existir mais, ignora e continua
  FILES_TO_EXPORT.forEach(file => {
    try {
      const url = `https://docs.google.com/spreadsheets/d/${file.id}/export?exportFormat=xlsx`;
      const response = UrlFetchApp.fetch(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      folder.createFile(response.getBlob().setName(file.nome));
    } catch (err) {
      Logger.log("Planilha não encontrada ou sem permissão (" + file.nome + ", id: " + file.id + "): " + (err && err.message));
    }
  });
}
