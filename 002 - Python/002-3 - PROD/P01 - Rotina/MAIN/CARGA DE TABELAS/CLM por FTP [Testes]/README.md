# SFTP CLM (DocuSign / SpringCM)

Conexão SFTP com chave RSA — mesma configuração do FileZilla.

## Arquivos (só o necessário)

| Arquivo | Uso |
|---------|-----|
| **00_Processo_Completo_CLM_FTP.py** | **Matriz:** conecta ao CLM e executa os steps 4, 5 e 6 em sequência. |
| **config_sftp.py** | Configuração: host, porta, usuário, caminho da chave. Ajuste aqui para bater com o FileZilla. |
| **03_Coleta_SFTP.py** | Conexão e uso: listar/baixar arquivos. |
| **04_Baixar_Reports_CLM.py** | Step 4: baixa os 3 reports e salva em STAGE/CLM Database/YYYY-MM-DD. |
| **05_Conversao_em_parquet.py** | Step 5: converte os CSVs da pasta mais recente em Parquet (CLM_DocuSign). |
| **06_Carga_em_Bucket.py** | Step 6: envia os Parquets para o bucket GCS (prod e dev). |
| **02_Testar_Conexao_SFTP.py** | Testar se a conexão está OK (Paramiko, chave, servidor). |
| **01_Gerar_Chaves_e_Configurar.py** | Só quando precisar de chave nova: gera par RSA e atualiza config. |

## Pipeline (processo por FTP)

**Tudo de uma vez:**  
`python 00_Processo_Completo_CLM_FTP.py` → conecta ao CLM e executa os steps 4, 5 e 6.

**Ou passo a passo:**  
4. `python 04_Baixar_Reports_CLM.py` → baixa os 3 CSVs em STAGE/CLM Database/YYYY-MM-DD  
5. `python 05_Conversao_em_parquet.py` → converte para Parquet em 001-99 - Outras Fontes/CLM_DocuSign  
6. `python 06_Carga_em_Bucket.py` → upload dos Parquets para o bucket GCS  

## Uso rápido

1. **Configurar:** edite `config_sftp.py` (host, usuário, `PRIVATE_KEY_PATH`) com os mesmos dados do FileZilla.
2. **Testar:** `python 02_Testar_Conexao_SFTP.py`
3. **Usar:** `python 03_Coleta_SFTP.py` (listar) ou rodar o pipeline 04 → 05 → 06.

Chave nova: `python 01_Gerar_Chaves_e_Configurar.py` → depois envie a chave pública no DocuSign (Manage Profile → Certificates).

## Requisitos

- **SFTP (04):** `pip install paramiko`
- **Step 5 (parquet):** `pandas`, `pyarrow`, `unidecode`
- **Step 6 (bucket):** `google-cloud-storage`  
  Ou: `pip install -r requirements.txt`
