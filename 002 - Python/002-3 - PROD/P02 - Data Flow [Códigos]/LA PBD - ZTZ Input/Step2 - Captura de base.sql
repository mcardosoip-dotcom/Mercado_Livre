CREATE
OR REPLACE EXTERNAL TABLE `<ENV>.STG.LK_PBD_LA_BACKLOG_PARCEIROS_ENLIGHTEN` (
  documents STRING
) OPTIONS (
  format = 'GOOGLE_SHEETS',
  skip_leading_rows = 1,
  sheet_range = 'Input!A:A',
  uris = ['https://docs.google.com/spreadsheets/d/1AZDxKWeSz4vSZvc7DT47v9viLWKVaSdVteCNssIvzss']
);

