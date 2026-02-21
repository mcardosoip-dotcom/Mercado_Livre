function doPost(e) {
return handleRequest(e);
}

function doGet(e) {
return handleRequest(e);
}

function handleRequest(e) {
try {
main(e);
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

function main(e) {
cruzarDadosFinal();
}

function cruzarDadosFinal() {
const folderIdInput = '1-MTlq_7QLdTrA2ivk1fT4BJ198D_-wRJ';
const folderIdOutput = '1uJJqqb5Ot9Mn7z4jNuFMdY4DyQIxrfOt';
const destId = '1zyhXcYfi7epUOjEyzeHA-nTYTAZryh74LArP39HzPN4';

const tabNameResultado = 'Resultado';
const tabNameSemMatch = '(Sem Match)';
const tabNameInput = 'Input';
const tabNameOutput = 'Output';

let tempOutputData = [];
let tempInputData = [];
let tempResultadoData = [];

let headerOutput = null;
let headerInput = null;

const outputMap = new Map();
const validUsersSet = new Set();

const matchConfigOutput = {
user: ['user_account'],
amount: ['amount'],
target: ['debt_id'],
filterCol: ['execution_status']
};

processarPastaCompleta(folderIdOutput, matchConfigOutput, headerOutput, (info) => {
if (!headerOutput) headerOutput = info.headers;

const status = String(info.matchedValues[3] || '').toLowerCase();
if (status.includes('error')) return;

const user = String(info.matchedValues[0]).trim();
const amountText = String(info.matchedValues[1]);
const amountClean = amountText.split('.')[0].trim();
const debtId = info.matchedValues[2];

if (user && amountClean) {
outputMap.set(user + '|' + amountClean, debtId);
}

if (user) {
validUsersSet.add(user);
}

tempOutputData.push({
user: user,
amountClean: amountClean,
fullRow: info.fullRow
});
});

const matchConfigInput = {
user: ['user_from'],
amount: ['amount'],
extras: ['case_file', 'court', 'cover_sheet']
};

processarPastaCompleta(folderIdInput, matchConfigInput, headerInput, (info) => {
if (!headerInput) headerInput = info.headers;

const user = String(info.matchedValues[0]).trim();
const amountText = String(info.matchedValues[1]);
const amountClean = amountText.split('.')[0].trim();

let foundDebtId = '';
const result = outputMap.get(user + '|' + amountClean);
if (result) foundDebtId = result;

let obsCruzamento = "Sem Match";
if (foundDebtId !== '') {
obsCruzamento = "Match ID e Valor";
} else if (validUsersSet.has(user)) {
obsCruzamento = "Match ID apenas";
}

tempInputData.push({
user: user,
amountClean: amountClean,
fullRow: info.fullRow,
foundId: foundDebtId
});

tempResultadoData.push({
user: user,
amount: amountClean,
case_file: info.matchedValues[2],
court: info.matchedValues[3],
cover_sheet: info.matchedValues[4],
debt_id: foundDebtId,
obs: obsCruzamento
});
});

const headerResultado = ['user_from', 'amount', 'case_file', 'court', 'cover_sheet', 'debt_id', 'OBS_Cruzamento', 'CHAVE_CONSOLIDADA'];

const finalResultadoTable = [headerResultado];
const finalSemMatchTable = [headerResultado];

tempResultadoData.forEach(item => {
const chave = item.user + item.amount;
const linha = [
item.user,
item.amount,
item.case_file,
item.court,
item.cover_sheet,
item.debt_id,
item.obs,
chave
];

if (item.obs === "Sem Match") {
finalSemMatchTable.push(linha);
} else {
finalResultadoTable.push(linha);
}
});

const finalInputTable = [];
if (headerInput) {
finalInputTable.push([...headerInput, 'MATCH_DEBT_ID', 'CHAVE_CONSOLIDADA']);
tempInputData.forEach(item => {
const chave = item.user + item.amountClean;
finalInputTable.push([...item.fullRow, item.foundId, chave]);
});
}

const finalOutputTable = [];
if (headerOutput) {
finalOutputTable.push([...headerOutput, 'CHAVE_CONSOLIDADA']);
tempOutputData.forEach(item => {
const chave = item.user + item.amountClean;
finalOutputTable.push([...item.fullRow, chave]);
});
}

const spreadsheet = SpreadsheetApp.openById(destId);

salvarEFormatar(spreadsheet, tabNameResultado, finalResultadoTable, true);
salvarEFormatar(spreadsheet, tabNameSemMatch, finalSemMatchTable, true);
salvarEFormatar(spreadsheet, tabNameInput, finalInputTable, true);
salvarEFormatar(spreadsheet, tabNameOutput, finalOutputTable, true);
}

function salvarEFormatar(spreadsheet, tabName, dados, pintarUltimaColuna) {
if (!dados || dados.length <= 1) {
let sheet = spreadsheet.getSheetByName(tabName);
if (sheet) sheet.clear();
return;
}

let sheet = spreadsheet.getSheetByName(tabName);
if (!sheet) {
sheet = spreadsheet.insertSheet(tabName);
} else {
sheet.clear();
}

const rows = dados.length;
const cols = dados[0].length;

sheet.getRange(1, 1, rows, cols).setValues(dados);
sheet.setFrozenRows(1);
sheet.getRange(1, 1, 1, cols).setFontWeight('bold');

if (pintarUltimaColuna && rows > 1) {
sheet.getRange(2, cols, rows - 1, 1).setBackground('#cfe2f3');
}
}

function processarPastaCompleta(folderId, configMatch, masterHeadersRef, callback) {
try {
const folder = DriveApp.getFolderById(folderId);
const files = folder.getFiles();
let localMasterHeaders = masterHeadersRef || null;

while (files.hasNext()) {
let file = files.next();
let mimeType = file.getMimeType();

if (mimeType === 'application/vnd.google-apps.shortcut') {
try {
file = DriveApp.getFileById(file.getTargetId());
mimeType = file.getMimeType();
} catch (e) {
continue;
}
}

let rawData = [];
if (file.getName().toLowerCase().endsWith('.csv') || mimeType === MimeType.CSV || mimeType === 'text/csv') {
const text = file.getBlob().getDataAsString();
try {
rawData = Utilities.parseCsv(text, ';');
} catch (e) {
rawData = [];
}
if (rawData.length > 0 && rawData[0].length < 2) {
try {
rawData = Utilities.parseCsv(text, ',');
} catch (e) {}
}
} else {
continue;
}

if (rawData.length < 2) continue;

const fileHeaders = rawData[0].map(h => String(h).trim());
const fileHeadersLower = fileHeaders.map(h => h.toLowerCase());

if (!localMasterHeaders) localMasterHeaders = fileHeaders;

const indicesMatch = {};
let hasRequiredKeys = true;

for (let key in configMatch) {
const possibleNames = configMatch[key];
let idx = -1;
for (let name of possibleNames) {
idx = fileHeadersLower.indexOf(name.toLowerCase());
if (idx > -1) break;
}
if (idx === -1 && (key === 'user' || key === 'amount')) hasRequiredKeys = false;
indicesMatch[key] = idx;
}

if (!hasRequiredKeys) continue;

for (let i = 1; i < rawData.length; i++) {
const row = rawData[i];

const userVal = indicesMatch['user'] > -1 ? row[indicesMatch['user']] : '';
const amountVal = indicesMatch['amount'] > -1 ? row[indicesMatch['amount']] : '';

const matchedValues = [userVal, amountVal];

if (configMatch.target) matchedValues.push(indicesMatch['target'] > -1 ? row[indicesMatch['target']] : '');
if (configMatch.filterCol) matchedValues.push(indicesMatch['filterCol'] > -1 ? row[indicesMatch['filterCol']] : '');
if (configMatch.extras) {
configMatch.extras.forEach(extraName => {
const idx = fileHeadersLower.indexOf(extraName.toLowerCase());
matchedValues.push(idx > -1 ? row[idx] : '');
});
}

const fullRowAligned = localMasterHeaders.map(masterColName => {
const idx = fileHeadersLower.indexOf(masterColName.toLowerCase());
return idx > -1 ? (row[idx] || '') : '';
});

callback({
matchedValues: matchedValues,
fullRow: fullRowAligned,
headers: localMasterHeaders
});
}
}
} catch (e) {
Logger.log('Erro ao processar pasta ' + folderId + ': ' + e.message);
}
}
