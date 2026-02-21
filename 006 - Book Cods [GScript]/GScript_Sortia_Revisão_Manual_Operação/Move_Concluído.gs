function moverParaConcluidos() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  const origem = ss.getSheetByName('Cruzamento');
  const destino = ss.getSheetByName('DataBase_Concluídos');

  if (!origem) throw new Error('Aba origem não encontrada: Cruzamento');
  if (!destino) throw new Error('Aba destino não encontrada: DataBase_Concluídos');

  // 1) Limpar DataBase_Concluídos ANTES de acrescentar (evita estourar limite de 10M células)
  //    Mantém só últimos 7 dias e remove linhas excedentes (deleteRows reduz o total de células)
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  cutoff.setHours(0, 0, 0, 0);

  const dbRange = destino.getDataRange();
  const dbData = dbRange.getValues();
  if (dbData.length > 1) {
    const kept = [dbData[0]]; // cabeçalho
    for (let i = 1; i < dbData.length; i++) {
      const cell = dbData[i][0];
      const dt = cell instanceof Date ? cell : new Date(cell);
      if (!isNaN(dt.getTime()) && dt >= cutoff) kept.push(dbData[i]);
    }
    destino.getRange(1, 1, kept.length, kept[0].length).setValues(kept);
    const lastRow = destino.getLastRow();
    const toDelete = lastRow - kept.length;
    if (toDelete > 0) {
      destino.deleteRows(kept.length + 1, toDelete);
    }
  }

  // 2) Processar Cruzamento: separar concluídos vs manter
  const range = origem.getDataRange();
  const data = range.getValues();

  if (data.length <= 1) {
    Logger.log('Nada para processar (somente cabeçalho ou vazio).');
    return;
  }

  const header = data[0];
  const manter = [header];
  const mover = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const raw = row[15];
    const status = (raw ?? '')
      .toString()
      .trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');

    if (status === 'concluido') mover.push(row);
    else manter.push(row);
  }

  Logger.log('Linhas para mover: ' + mover.length);
  Logger.log('Linhas para manter: ' + (manter.length - 1));

  if (mover.length > 0) {
    const startRow = destino.getLastRow() + 1;
    destino.getRange(startRow, 1, mover.length, mover[0].length).setValues(mover);
  }

  origem.clearContents();
  origem.getRange(1, 1, manter.length, manter[0].length).setValues(manter);
}
