# Configuração de acesso ao Bucket GCP (Google Cloud Storage)

Este guia ajuda a configurar o acesso para o script `002 - Carga_em_Bucket.py` subir arquivos nos buckets **pdme000426** (prod) e **ddme000426** (dev).

---

## Opção A: Usar sua conta com gcloud (desenvolvimento/local)

1. **Instale o Google Cloud SDK** (se ainda não tiver):
   - https://cloud.google.com/sdk/docs/install

2. **Faça login e defina as credenciais padrão para aplicação:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
   - O primeiro comando abre o navegador para login na sua conta Google.
   - O segundo grava credenciais que o Python usa automaticamente.

3. **Defina o projeto** (substitua pelo ID do seu projeto):
   ```bash
   gcloud config set project SEU_PROJECT_ID
   ```

4. **Permissões:** sua conta precisa ter permissão nos buckets (ex.: *Storage Object Creator* ou *Storage Admin*). Quem administra o projeto GCP pode conceder isso no Console.

Depois disso, execute o script sem alterar `CAMINHO_CREDENCIAIS_JSON` (deixe `None`).

---

## Opção B: Service Account (recomendado para rotinas/automação)

1. **No Console GCP** (https://console.cloud.google.com):
   - **IAM e administração** → **Contas de serviço** → **Criar conta de serviço**
   - Nome sugerido: ex. `carga-bucket-legales`
   - Clique em **Criar e continuar**

2. **Conceda permissão à conta:**
   - Adicione o papel **Storage Object Creator** (ou **Storage Admin** se precisar de mais que upload).
   - Avançar → Concluir.

3. **Crie uma chave JSON:**
   - Na lista de contas de serviço, clique na que você criou
   - Aba **Chaves** → **Adicionar chave** → **Criar nova chave** → **JSON**
   - O arquivo será baixado. **Guarde em local seguro e não suba no Git.**

4. **Dê acesso aos buckets para essa service account:**
   - No **Cloud Storage** → selecione o bucket (ex.: `pdme000426`)
   - Aba **Permissões** → **Conceder acesso**
   - Novo principal: e-mail da service account (ex. `carga-bucket-legales@seu-projeto.iam.gserviceaccount.com`)
   - Papel: **Storage Object Creator** (ou **Storage Admin**)
   - Repita para o bucket `ddme000426` se for usar os dois.

5. **Configure o script** de uma das formas:

   **5.1 Variável de ambiente (recomendado)**  
   No Windows (PowerShell, uma vez por sessão):
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\caminho\para\sua-chave-service-account.json"
   ```
   No Windows (definir permanentemente):
   - Painel de Controle → Sistema → Configurações avançadas → Variáveis de ambiente
   - Em "Variáveis do usuário", Nova → Nome: `GOOGLE_APPLICATION_CREDENTIALS`, Valor: caminho completo do arquivo `.json`

   **5.2 Direto no script**  
   No arquivo `002 - Carga_em_Bucket.py`, na linha de configuração:
   ```python
   CAMINHO_CREDENCIAIS_JSON = r"C:\caminho\para\sua-chave-service-account.json"
   ```
   Use o caminho real onde você salvou o JSON.

---

## Erros comuns

| Erro | O que fazer |
|------|-------------|
| `Could not automatically determine credentials` | Use Opção A (`gcloud auth application-default login`) ou Opção B (service account + variável ou `CAMINHO_CREDENCIAIS_JSON`). |
| `403 Forbidden` / `Permission denied` | A conta ou service account não tem permissão no bucket. Adicione **Storage Object Creator** (ou **Storage Admin**) no bucket. |
| `404 Not Found` no bucket | Nome do bucket errado ou bucket em outro projeto. Confirme os nomes `pdme000426` e `ddme000426` no Console GCP. |
| `File not found` no JSON | O caminho em `GOOGLE_APPLICATION_CREDENTIALS` ou em `CAMINHO_CREDENCIAIS_JSON` está errado ou o arquivo foi movido. |

---

## Teste rápido

Depois de configurar:

```bash
cd "G:\Drives compartilhados\Legales_Analytics\002 - Python\002-3 - PROD\P01 - Rotina\DIM"
python "002 - Carga_em_Bucket.py"
```

O script mostra qual tipo de credencial está usando e, em caso de falha, exibe mensagens objetivas para ajustar acesso ou caminho do JSON.
