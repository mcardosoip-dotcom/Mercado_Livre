import re
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd

pdf_path = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Matriz de arquivos\1dX1DC-vrs7w8rk_U2xUil3aPi8S_rNZF.pdf"

# ==============================
# 1) Metadados
# ==============================
doc = fitz.open(pdf_path)
metadata = doc.metadata
page_count = doc.page_count
file_size_kb = round(doc.tobytes().__sizeof__() / 1024, 2)
doc.close()

# ==============================
# 2) Conteúdo (pdfplumber)
# ==============================
pages_data = []
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        pages_data.append({"pagina": i, "conteudo": text.strip()})

df = pd.DataFrame([p for p in pages_data if p["conteudo"]])

# ==============================
# 3) Busca robusta (atravessa quebras de linha)
# ==============================
KEYWORDS = ["CPF", "CNPJ", "Multa"]

# Permite até 40 chars não-numéricos entre termo e número e aceita separadores + espaços/linhas
PAT = re.compile(r"(CPF|CNPJ|Multa)[^\d]{0,40}([\d\.\-\/,\s]{3,60})",
                 flags=re.IGNORECASE | re.DOTALL)

def normalize_id(term: str, raw_number: str) -> str:
    digits = re.sub(r"\D", "", raw_number)  # remove tudo que não for dígito
    if term.upper() == "CPF":
        # pega o primeiro bloco de 11 dígitos contínuos
        m = re.search(r"\d{11}", digits)
        return m.group(0) if m else digits
    if term.upper() == "CNPJ":
        # pega o primeiro bloco de 14 dígitos contínuos
        m = re.search(r"\d{14}", digits)
        return m.group(0) if m else digits
    # Multa: extrai o primeiro número "humano" (com milhar/decimal)
    #  - prioriza algo como 12.345,67 ou 12345,67; se não houver vírgula decimal, pega inteiro
    m = re.search(r"\d[\d\.\s]{0,15},\d{2}", raw_number) or re.search(r"\d[\d\.\s]{3,}", raw_number)
    if m:
        val = m.group(0)
        val = re.sub(r"\s", "", val)      # tira espaços
        val = val.replace(".", "")        # remove milhar
        val = val.replace(",", ".")       # vírgula -> ponto decimal
        return val
    return re.sub(r"[^\d,\.]", "", raw_number)

def highlight_context(text: str, start: int, end: int, ctx: int = 60) -> str:
    s = max(0, start - ctx)
    e = min(len(text), end + ctx)
    snippet = text[s:e].replace("\n", " ")
    return snippet

matches_total = []
for _, row in df.iterrows():
    t = row["conteudo"]
    for m in PAT.finditer(t):
        term = m.group(1)
        raw_num = m.group(2)
        clean = normalize_id(term, raw_num)

        # Para o contexto, uso as posições do match completo (termo + sequência)
        ctx = highlight_context(t, m.start(), m.end())
        matches_total.append({
            "pagina": row["pagina"],
            "termo": term.upper(),
            "numero_encontrado": clean,
            "contexto": ctx
        })

# ==============================
# 4) Print estruturado
# ==============================
print("\n" + "="*100)
print("📄 INFORMAÇÕES GERAIS DO DOCUMENTO")
print("="*100)
print(f"📁 Caminho: {pdf_path}")
print(f"📚 Número de páginas: {page_count}")
print(f"💾 Tamanho do arquivo: {file_size_kb} KB\n")

print("🧾 Metadados:")
for k, v in metadata.items():
    print(f"  • {k}: {v if v else '—'}")

print("\n" + "="*100)
print("🔍 PALAVRAS-CHAVE  ENCONTRADAS")
print("="*100)
if matches_total:
    for m in matches_total:
        print(f"📎 Página {m['pagina']:>2} | {m['termo']:<5} → {m['numero_encontrado']}")
 #       print(f"    … {m['contexto']} …")
else:
    print("⚠️ Nenhuma ocorrência de CPF, CNPJ ou Multa encontrada.")

print("\n" + "="*100)
print("🧠 CONTEÚDO (PRÉVIA)")
print("="*100)
for _, row in df.iterrows():
    print(f"\n--- Página {row['pagina']} ---")
    print((row['conteudo'][:1000]).strip())
    if len(row['conteudo']) > 1000:
        print("... [conteúdo truncado]")
    print("-" * 80)
