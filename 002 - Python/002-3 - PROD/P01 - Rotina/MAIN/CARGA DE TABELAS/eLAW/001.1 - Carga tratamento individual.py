import pandas as pd
import re
import os
import unicodedata

# --- Funções de Normalização ---

def normalizar_coluna(nome):
    """
    Normaliza o nome de uma coluna:
    1. Remove acentos e caracteres especiais (mantém apenas ASCII).
    2. Converte para minúsculas.
    3. Substitui sequências de caracteres não alfanuméricos (incluindo espaços)
       por um único underscore (_).
    4. Remove underscores do início ou fim.
    """
    # 1. Normaliza para remover acentos
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    
    # 2. Converte para minúsculas
    nome = nome.lower()
    
    # 3. Substitui caracteres não alfanuméricos (exceto a-z e 0-9) por underscore
    # O '+' garante que múltiplos caracteres especiais/espaços seguidos sejam substituídos por UM SÓ '_'
    nome = re.sub(r'[^a-z0-9]+', '_', nome)
    
    # 4. Remove o '_' se for o primeiro ou o último caractere
    nome = nome.strip('_')
    
    return nome

# Função para extrair os valores desejados (mantida com pequenas melhorias)
def extrair_campos(texto, padroes):
    """Extrai campos de texto semi-estruturado usando padrões regex."""
    if pd.isna(texto):
        return {}
        
    resultado = {}
    
    for nome, regex in padroes.items():
        m = regex.search(str(texto))
        if m:
            # Captura, limpa espaços em branco e salva
            valor = m.group(1).strip()
            resultado[nome] = valor
        else:
            resultado[nome] = None
            
    return resultado

# --- Configurações e Caminhos ---

# Caminho do arquivo parquet original
# ATENÇÃO: Verifique se este caminho existe e se você tem permissão
arquivo = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW\Database_eLAW_Obrigacoes_de_Fazer.parquet"

# Caminho do arquivo de saída
# ATENÇÃO: Verifique se este caminho é válido
saida = r"G:\Drives compartilhados\Legales_Analytics\001 - Base\001-01 - eLAW\Database_eLAW_Obrigacoes_de_Fazer_Com_Multas.parquet"

# Coluna com texto semi-estruturado
coluna = "descricao_evento_concluido"

# Campos que queremos extrair (nomes originais, que serão normalizados depois)
campos = [
    "Tem multa fixada?",
    "Prazo para Cumprimento",
    "Valor da Multa (R$?)",
    "Periodicidade da Multa",
    "Teto Multa"
]

# Regex para capturar cada campo com segurança
# Usamos re.escape(campo) para tratar caracteres especiais nos nomes dos campos
# Regex mais robusto (captura valores com R$, pontos e vírgulas)
padroes = {
    "Tem multa fixada?": re.compile(r"Tem multa fixada\?\s*:\s*([^;]*?)(?=;|$)", re.IGNORECASE),
    "Prazo para Cumprimento": re.compile(r"Prazo para Cumprimento\s*:\s*([^;]*?)(?=;|$)", re.IGNORECASE),
    "Valor da Multa (R\$?)": re.compile(r"Valor da Multa\s*\(R\$?\)\s*:\s*([^;]*?)(?=;|$)", re.IGNORECASE),
    "Periodicidade da Multa": re.compile(r"Periodicidade da Multa\s*:\s*([^;]*?)(?=;|$)", re.IGNORECASE),
    "Teto Multa": re.compile(r"Teto Multa\s*:\s*([^;]*?)(?=;|$)", re.IGNORECASE)
}

def limpar_valor_monetario(valor):
    """Converte valores como 'R$ 1.234,56' para '1234.56'."""
    if pd.isna(valor):
        return None
    texto = str(valor)
    texto = re.sub(r'[^\d,.-]', '', texto)     # remove R$, espaços etc
    texto = texto.replace('.', '').replace(',', '.')
    try:
        return float(texto)
    except ValueError:
        return None

print(f"Iniciando leitura do arquivo: {arquivo}")

df = pd.read_parquet(arquivo)
print(f"Base lida com {len(df)} linhas.")

df_extraido = df[coluna].apply(lambda x: extrair_campos(x, padroes)).apply(pd.Series)

# Limpeza pós-extração
if "Valor da Multa (R$?)" in df_extraido.columns:
    df_extraido["Valor da Multa (R$?)"] = df_extraido["Valor da Multa (R$?)"].apply(limpar_valor_monetario)

# Junta com o DataFrame original
df_final = pd.concat([df, df_extraido], axis=1)

# Normaliza os nomes
df_final.columns = [normalizar_coluna(c) for c in df_final.columns]

# Verifica o resultado antes de salvar
print(df_final[["valor_da_multa_r", "descricao_evento_concluido"]].head(10))

# Exporta o parquet final
df_final.to_parquet(saida, index=False)
print(f"\n✅ Arquivo final salvo com sucesso em: {saida}")
