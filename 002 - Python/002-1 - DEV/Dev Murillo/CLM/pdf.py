import os
import re
from PyPDF2 import PdfReader

# Caminho da pasta com os PDFs
base_path = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Matriz de arquivos"

# Lista de nomes (ou palavras) que você quer procurar
nomes_procurados = ["Ronaldo Luís Nazário de Lima","Larissa de Macedo Machado","Anitta"]  # exemplo

# Quantidade de caracteres de contexto ao redor da ocorrência
contexto = 60

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    try:
        reader = PdfReader(caminho_pdf)
        for page in reader.pages:
            texto += page.extract_text() or ""
    except Exception as e:
        print(f"⚠️ Erro ao ler {caminho_pdf}: {e}")
    return texto

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.lower().endswith(".pdf"):
            caminho_arquivo = os.path.join(root, file)
            texto = extrair_texto_pdf(caminho_arquivo)
            texto_lower = texto.lower()
            for nome in nomes_procurados:
                nome_lower = nome.lower()
                for match in re.finditer(nome_lower, texto_lower):
                    inicio = max(match.start() - contexto, 0)
                    fim = min(match.end() + contexto, len(texto))
                    trecho = texto[inicio:fim].replace("\n", " ")
                    print(f"\n📄 {file}")
                    print(f"➡️ Nome encontrado: '{nome}'")
                    print(f"...{trecho}...")
