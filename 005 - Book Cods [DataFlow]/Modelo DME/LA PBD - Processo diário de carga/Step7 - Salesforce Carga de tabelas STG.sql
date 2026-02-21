LOAD DATA OVERWRITE STG.SALESFORCE_INCOMING_EMBARGOS  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Incoming_Embargos.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_INCOMING_OFICIOS  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Incoming_Oficios.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_OUTCOMING_OFICIOS  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Outcoming_Oficios.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_OUTGOING_EMBARGOS  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Outgoing_Embargos.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_PENDING_EMBARGOS_BCRA_E_NAO_BCRA  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Pending_Embargos_BCRA_e_nao_BCRA.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_PENDING_INFORMATIVOS  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Pending_Informativos.parquet']
);

LOAD DATA OVERWRITE STG.SALESFORCE_BCRA_OE_ISSUE  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_BCRA_OE_ISSUE.parquet']
);


LOAD DATA OVERWRITE STG.SALESFORCE_EMBARGOS_REVISAO_MANUAL  
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://<Bucket>/Projeto banco de dados/Salesforce_Databases/Salesforce_Report_Embargos_Revisao.parquet']
);




LOAD DATA OVERWRITE STG.PAGAMENTOS_FINAL_BRASIL
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Final_Brasil.parquet']
  );

LOAD DATA OVERWRITE STG.PAGAMENTOS_FINAL_HISPANOS
FROM
  FILES (
    format = 'PARQUET',
    uris = ['gs://<Bucket>/Projeto banco de dados/Diversas/Final_Hispanos.parquet']
  );
