import os
import re
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd

# ====== Caminhos ======
input_dir = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Matriz de arquivos"
output_xlsx = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Resultado\Resultado2.xlsx"

# ====== Quantos arquivos ler (0 = todos) ======
NUM_ARQUIVOS = 5  # altere aqui se quiser limitar

# ====== Regex ======
GUID_RE = re.compile(r"\b[0-9A-Fa-f]{8}-(?:[0-9A-Fa-f]{4}-){3}[0-9A-Fa-f]{12}\b")
DOCUSIGN_RE = re.compile(r"DocuSign\s*Envelope\s*ID\s*[:\-–]?\s*([^\n]+)", flags=re.IGNORECASE)
PAT = re.compile(r"(CPF|CNPJ|Multa)[^\d]{0,40}([\d\.\-\/,\s]{3,60})", flags=re.IGNORECASE | re.DOTALL)

# ====== Normalizador ======
def normalize_id(term: str, raw_number: str) -> str:
    term_up = term.upper()
    digits = re.sub(r"\D", "", raw_number)

    if term_up == "CPF":
        m = re.search(r"\d{11}", digits)
        return m.group(0) if m else digits

    if term_up == "CNPJ":
        m = re.search(r"\d{14}", digits)
        return m.group(0) if m else digits

    # Multa (12.345,67 -> 12345.67)
    m = re.search(r"\d[\d\.\s]{0,15},\d{2}", raw_number) or re.search(r"\d[\d\.\s]{3,}", raw_number)
    if m:
        val = m.group(0)
        val = re.sub(r"\s", "", val).replace(".", "").replace(",", ".")
        return val
    return re.sub(r"[^\d,\.]", "", raw_number)

# ====== Arquivos a processar ======
arquivos_pdf = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
arquivos_pdf.sort()
if NUM_ARQUIVOS > 0:
    arquivos_pdf = arquivos_pdf[:NUM_ARQUIVOS]

print(f"🔍 Processando {len(arquivos_pdf)} arquivo(s)...")

todos_resultados = []

for idx, arquivo in enumerate(arquivos_pdf, start=1):
    pdf_path = os.path.join(input_dir, arquivo)
    doc_id = os.path.splitext(arquivo)[0]

    print(f"📄 [{idx}/{len(arquivos_pdf)}] {arquivo}")

    try:
        # === 1) Metadados ===
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        file_size_kb = round(doc.tobytes().__sizeof__() / 1024, 2)
        doc.close()

        # === 2) Conteúdo (pode falhar em PDFs imagem) ===
        pages_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages_data.append({"pagina": i, "conteudo": text.strip()})

        df = pd.DataFrame([p for p in pages_data if p["conteudo"]])

        # Se não houver texto legível:
        if df.empty or "conteudo" not in df.columns:
            todos_resultados.append({
                "DOC_ID": doc_id,
                "DocuSign Envelope ID": "",
                "CHAVE": "Não lido",
                "CHAVE_ID": "",
                "PAGINAS": page_count,
                "TAMANHO_KB": file_size_kb
            })
            print(f"⚠️  Arquivo ignorado (sem texto legível)")
            continue

        # === 3) Envelope ID ===
        full_text = "\n".join(df["conteudo"].tolist())
        envelope_id = ""
        m_env = DOCUSIGN_RE.search(full_text)
        if m_env:
            g = GUID_RE.search(m_env.group(0))
            if g:
                envelope_id = g.group(0).upper()

        # === 4) Extração de chaves ===
        matches_total = []
        for _, row in df.iterrows():
            t = row["conteudo"]
            for m in PAT.finditer(t):
                term = m.group(1)
                raw_num = m.group(2)
                clean = normalize_id(term, raw_num)
                matches_total.append({
                    "pagina": row["pagina"],
                    "termo": term.upper(),
                    "numero_encontrado": clean
                })

        # === 5) Resultados do arquivo ===
        if matches_total:
            for m in matches_total:
                todos_resultados.append({
                    "DOC_ID": doc_id,
                    "DocuSign Envelope ID": envelope_id,
                    "CHAVE": m["termo"],
                    "CHAVE_ID": m["numero_encontrado"],
                    "PAGINAS": page_count,
                    "TAMANHO_KB": file_size_kb
                })
        else:
            todos_resultados.append({
                "DOC_ID": doc_id,
                "DocuSign Envelope ID": envelope_id,
                "CHAVE": "Sem correspondências",
                "CHAVE_ID": "",
                "PAGINAS": page_count,
                "TAMANHO_KB": file_size_kb
            })

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")
        todos_resultados.append({
            "DOC_ID": doc_id,
            "DocuSign Envelope ID": "",
            "CHAVE": "Não lido",
            "CHAVE_ID": "",
            "PAGINAS": "",
            "TAMANHO_KB": ""
        })

# ====== Consolidar ======
out_df = pd.DataFrame(todos_resultados, columns=["DOC_ID", "DocuSign Envelope ID", "CHAVE", "CHAVE_ID", "PAGINAS", "TAMANHO_KB"])

if os.path.exists(output_xlsx):
    os.remove(output_xlsx)

with pd.ExcelWriter(output_xlsx, engine="openpyxl") as writer:
    out_df.to_excel(writer, index=False, sheet_name="Resultado2")

print(f"\n✅ Resultado salvo em: {output_xlsx}")
print(f"📊 Linhas totais: {len(out_df)} em {len(arquivos_pdf)} arquivo(s)")
