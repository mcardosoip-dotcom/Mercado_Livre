-- Tabela externa para Commerce 2020
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2020` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = '2020!A:O',
    uris = ['https://docs.google.com/spreadsheets/d/1Oz9U17YSW8r74mT_jX1JdeWtA7aHx9r5fWID6JKCZMs/edit?gid=81935643#gid=81935643']
);

-- Tabela externa para Commerce 2021
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2021` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = '2021!A:O',
    uris = ['https://docs.google.com/spreadsheets/d/1Oz9U17YSW8r74mT_jX1JdeWtA7aHx9r5fWID6JKCZMs/edit?gid=81935643#gid=81935643']
);

-- Tabela externa para Commerce 2022
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2022` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = '2022!A:O',
    uris = ['https://docs.google.com/spreadsheets/d/1Oz9U17YSW8r74mT_jX1JdeWtA7aHx9r5fWID6JKCZMs/edit?gid=81935643#gid=81935643']
);

-- Tabela externa para Commerce 2023
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2023` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = '2023!A:O',
    uris = ['https://docs.google.com/spreadsheets/d/1Oz9U17YSW8r74mT_jX1JdeWtA7aHx9r5fWID6JKCZMs/edit?gid=81935643#gid=81935643']
);

-- Tabela externa para Commerce 2024
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2024` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = '2024!A:O',
    uris = ['https://docs.google.com/spreadsheets/d/1Oz9U17YSW8r74mT_jX1JdeWtA7aHx9r5fWID6JKCZMs/edit?gid=81935643#gid=81935643']
);

-- Tabela externa para Commerce 2025 parte 2
CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.COMMERCE_DATABASE_2025` (
    Responsavel STRING,
    Solicitante STRING,
    Data_de_solicitacao DATE,
    Hora_de_solicitacao STRING,
    Ariba_CLM STRING,
    Nome_contraparte STRING,
    Objeto STRING,
    Descricao STRING,
    Valor_global STRING,
    Expectativa_GMV STRING,
    Cost_Avoidance STRING,
    Cost_Saving STRING,
    Data_Entrega DATE,
    Hora_Entrega STRING,
    Area STRING,
    Status_Macro STRING,
    Status_Micro STRING
) OPTIONS (
    format = 'GOOGLE_SHEETS',
    skip_leading_rows = 1,
    sheet_range = 'Database!A:Q',
    uris = ['https://docs.google.com/spreadsheets/d/1BnKT25oRcYOg3UNechKi5v2WfciHzoJcDoGaGVZ5JnI/edit?gid=695733864#gid=695733864']
);