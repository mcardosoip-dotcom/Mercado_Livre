function gerarRelatorioCorrigido() {
  // ==========================================
  // 1. CONFIGURAÇÕES
  // ==========================================
  const idPlanilha = '1zo6019x58F7YiTbijqpawmbFVWhBs8nhZEjYXyEjqxU';
  const idDoc = '1Shqv6PC8txxaNyQXdCmK16VPYxvNYKEeUA1eXoZ9Qcw';
  const nomeAba = 'Tabela_Final';

  // Larguras das colunas
  const largNome = 110;    
  const largCPF = 80;      
  const largClasse = 65;   
  const largEspaco = 10;   

  const titulos = ["Nome", "CPF", "Classe"];

  // ==========================================
  // 2. LER E PROCESSAR DADOS
  // ==========================================
  const ss = SpreadsheetApp.openById(idPlanilha);
  const aba = ss.getSheetByName(nomeAba);
  
  if (!aba) { Logger.log("ERRO: Aba não encontrada!"); return; }
  
  const ultimaLinha = aba.getLastRow();
  
  // >>> ALTERAÇÃO 1: Lendo 4 colunas para incluir a Coluna D (Origem/Tipo) <<<
  // Índices: 0=Classe, 1=Nome, 2=CPF, 3=Origem(Coluna D)
  const dados = aba.getRange(2, 1, ultimaLinha - 1, 4).getValues();
  
  // Filtra linhas onde o Nome (índice 1) não está vazio
  const listaLimpa = dados.filter(linha => linha[1] !== "" && linha[1] != null);
  
  const metade = Math.ceil(listaLimpa.length / 2);
  const blocoEsquerda = listaLimpa.slice(0, metade);
  const blocoDireita = listaLimpa.slice(metade, listaLimpa.length);

  // ==========================================
  // 3. PREPARAR O DOCUMENTO
  // ==========================================
  let doc = DocumentApp.openById(idDoc); 
  let body = doc.getBody();
  body.clear(); 
  
  body.setMarginLeft(36);
  body.setMarginRight(36);
  body.setMarginTop(36);
  body.setMarginBottom(36);

  const tituloDoc = body.appendParagraph("Relatório Final de Classificação");
  tituloDoc.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  tituloDoc.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  body.appendParagraph(""); 

  // ==========================================
  // 4. ESTILOS
  // ==========================================
  const estiloBase = {};
  estiloBase[DocumentApp.Attribute.FONT_SIZE] = 9;
  estiloBase[DocumentApp.Attribute.FONT_FAMILY] = 'Arial';
  estiloBase[DocumentApp.Attribute.VERTICAL_ALIGNMENT] = DocumentApp.VerticalAlignment.CENTER;

  const estiloHeader = {};
  Object.assign(estiloHeader, estiloBase);
  estiloHeader[DocumentApp.Attribute.BOLD] = true;
  estiloHeader[DocumentApp.Attribute.BACKGROUND_COLOR] = '#444444';
  estiloHeader[DocumentApp.Attribute.FOREGROUND_COLOR] = '#FFFFFF';
  estiloHeader[DocumentApp.Attribute.BORDER_WIDTH] = 1;
  estiloHeader[DocumentApp.Attribute.BORDER_COLOR] = '#000000';
  estiloHeader[DocumentApp.Attribute.PADDING_TOP] = 3;
  estiloHeader[DocumentApp.Attribute.PADDING_BOTTOM] = 3;

  const estiloCel = {};
  Object.assign(estiloCel, estiloBase);
  estiloCel[DocumentApp.Attribute.FOREGROUND_COLOR] = '#000000';
  estiloCel[DocumentApp.Attribute.BORDER_WIDTH] = 1;
  estiloCel[DocumentApp.Attribute.BORDER_COLOR] = '#000000';
  estiloCel[DocumentApp.Attribute.PADDING_TOP] = 2;
  estiloCel[DocumentApp.Attribute.PADDING_BOTTOM] = 2;

  const estiloEspaco = {};
  estiloEspaco[DocumentApp.Attribute.BORDER_WIDTH] = 0;
  estiloEspaco[DocumentApp.Attribute.BACKGROUND_COLOR] = '#FFFFFF';

  // ==========================================
  // 5. CONSTRUIR TABELA
  // ==========================================
  let tabela = body.appendTable();
  tabela.setBorderWidth(0); 

  function addCell(row, text, width, style, align, bgColor) {
    let conteudo = (text !== null && text !== undefined) ? text.toString() : "";
    const cell = row.appendTableCell(conteudo);
    cell.setAttributes(style);
    cell.setWidth(width);
    if (align) cell.getChild(0).asParagraph().setAlignment(align);
    if (bgColor) cell.setBackgroundColor(bgColor);
  }

  // >>> ALTERAÇÃO 2: Função Helper para formatar CPF <<<
  function processarCPF(valorBruto, origem) {
    if (!valorBruto) return "";
    
    let texto = valorBruto.toString();

    // Se a coluna D for "Base de estrangeiros", retorna original sem mexer
    if (origem === "Base de estrangeiros") {
      return texto; 
    }

    // Lógica para CPF brasileiro: remove não-números e formata
    let apenasNumeros = texto.replace(/\D/g, "");
    
    // Adiciona zeros à esquerda até completar 11 dígitos
    apenasNumeros = apenasNumeros.padStart(11, '0');

    // Aplica a máscara 000.000.000-00
    return apenasNumeros.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
  }

  // --- CABEÇALHO ---
  const rowHeader = tabela.appendTableRow();
  addCell(rowHeader, titulos[0], largNome, estiloHeader, DocumentApp.HorizontalAlignment.LEFT);
  addCell(rowHeader, titulos[1], largCPF, estiloHeader, DocumentApp.HorizontalAlignment.CENTER);
  addCell(rowHeader, titulos[2], largClasse, estiloHeader, DocumentApp.HorizontalAlignment.CENTER);
  addCell(rowHeader, "", largEspaco, estiloEspaco);
  addCell(rowHeader, titulos[0], largNome, estiloHeader, DocumentApp.HorizontalAlignment.LEFT);
  addCell(rowHeader, titulos[1], largCPF, estiloHeader, DocumentApp.HorizontalAlignment.CENTER);
  addCell(rowHeader, titulos[2], largClasse, estiloHeader, DocumentApp.HorizontalAlignment.CENTER);

  // --- DADOS ---
  for (let i = 0; i < metade; i++) {
    
    if (i > 0 && i % 80 === 0) {
      doc.saveAndClose();
      doc = DocumentApp.openById(idDoc);
      body = doc.getBody();
      tabela = body.getTables()[0]; 
    }

    const row = tabela.appendTableRow();
    const corFundo = (i % 2 === 1) ? '#F3F3F3' : '#FFFFFF';

    // >>> ALTERAÇÃO 3: Aplicação da lógica nos blocos <<<
    
    // --- BLOCO ESQUERDA ---
    if (blocoEsquerda[i]) {
      // Índice 2 = CPF Bruto, Índice 3 = Coluna D (Origem)
      let cpfFormatado = processarCPF(blocoEsquerda[i][2], blocoEsquerda[i][3]);
      
      addCell(row, blocoEsquerda[i][1], largNome, estiloCel, DocumentApp.HorizontalAlignment.LEFT, corFundo);
      addCell(row, cpfFormatado, largCPF, estiloCel, DocumentApp.HorizontalAlignment.CENTER, corFundo);
      addCell(row, blocoEsquerda[i][0], largClasse, estiloCel, DocumentApp.HorizontalAlignment.CENTER, corFundo);
    } else {
      addCell(row, "", largNome, estiloCel, null, corFundo);
      addCell(row, "", largCPF, estiloCel, null, corFundo);
      addCell(row, "", largClasse, estiloCel, null, corFundo);
    }

    // --- ESPAÇADOR ---
    addCell(row, "", largEspaco, estiloEspaco);

    // --- BLOCO DIREITA ---
    if (i < blocoDireita.length) {
      // Índice 2 = CPF Bruto, Índice 3 = Coluna D (Origem)
      let cpfFormatado = processarCPF(blocoDireita[i][2], blocoDireita[i][3]);

      addCell(row, blocoDireita[i][1], largNome, estiloCel, DocumentApp.HorizontalAlignment.LEFT, corFundo);
      addCell(row, cpfFormatado, largCPF, estiloCel, DocumentApp.HorizontalAlignment.CENTER, corFundo);
      addCell(row, blocoDireita[i][0], largClasse, estiloCel, DocumentApp.HorizontalAlignment.CENTER, corFundo);
    } else {
      addCell(row, "", largNome, estiloCel, null, corFundo);
      addCell(row, "", largCPF, estiloCel, null, corFundo);
      addCell(row, "", largClasse, estiloCel, null, corFundo);
    }
  }

  doc.saveAndClose();
  Logger.log("Relatório gerado com lógica condicional de CPF!");
}