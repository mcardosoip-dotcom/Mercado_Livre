function onOpen() {
SpreadsheetApp.getUi()
.createMenu('Legal Analytics')
.addItem('Mover para Concluído', 'moverParaConcluidos')
.addToUi();
}