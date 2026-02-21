import pdfplumber
import re
import unicodedata
from difflib import SequenceMatcher
from collections import defaultdict
import os
import pandas as pd

# ===== Base de Categorias =====
CATEGORIAS = {
    "COMPRAS": {
        "Realização de obra": [
            "obra", "construção", "reforma", "ampliação", "engenharia", "execução de obra", "edificação",
            "obra civil", "construccion", "remodelacion", "ampliacion", "ejecucion de obra",
            "mantenimiento de infraestructura", "construction", "building", "civil work", "renovation",
            "remodeling", "infrastructure project", "engineering work", "structural repair", "site works"
        ],
        "Prestação de serviço": [
            "prestação de serviço", "serviço", "serviços técnicos", "manutenção", "consultoria",
            "limpeza", "assistência técnica", "fornecimento de mão de obra", "gestão de serviços",
            "manutenção preventiva", "terceirização", "suporte técnico", "auditoria", "servicios profesionales",
            "prestacion de servicios", "mantenimiento", "limpieza", "asistencia técnica", "soporte tecnico",
            "services", "technical service", "outsourcing", "cleaning services", "advisory"
        ],
        "Compra de equipamentos": [
            "equipamento", "equipamentos", "máquina", "maquinário", "hardware", "instrumento",
            "ferramenta industrial", "equipamentos eletrônicos", "equipment", "machinery", "devices",
            "industrial tool", "electronic equipment"
        ],
        "Compra de produtos": [
            "produto", "insumo", "material", "materiais", "mercadoria", "fornecimento de materiais",
            "bens de consumo", "materiais de escritório", "materiais de construção", "materiais elétricos",
            "producto", "productos", "materiales", "goods", "supplies", "procurement"
        ],
        "Aluguel de bens": [
            "aluguel", "arrendamento", "comodato", "locação de equipamentos", "leasing", "equipment rental"
        ],
        "Aluguel de imóveis": [
            "imóvel", "imóveis", "locação", "locacao","locataria","locadora",
            "contrato de locação", "aluguel de imóvel", "propriedade",
            "edifício", "galpão", "armazém", "oficina", "terreno", "sala comercial",
            "local comercial", "escritório", "prédio", "inmueble", "arrendamiento",
            "property", "real estate", "lease", "rental property"
        ],
        "Transporte": [
            "transporte", "frete", "envio", "logística", "entrega", "remessa", "coleta",
            "distribution", "shipping", "delivery", "logistics", "freight"
        ],
        "Publicidade e marketing": [
            "marketing", "publicidade", "propaganda", "campanha", "promoção", "branding",
            "divulgação", "mídia", "influenciador", "advertising", "promotion"
        ],
        "Operação logística": [
            "centro de distribuição", "armazém", "logística", "armazenagem",
            "rede de transporte", "operação logística", "warehouse", "supply chain"
        ],
        "Licenças e software": [
            "licença", "software", "assinatura", "plataforma", "sistema", "programa",
            "aplicativo", "tecnologia", "saas", "nuvem", "license", "subscription", "cloud"
        ],
        "Outros": [
            "outros", "contratação", "contrato diverso", "fornecedor", "supplier", "provider"
        ]
    },
    "VENDAS": {
        "Acordos T&C": [
            "termos e condições", "agreement", "appendix", "addendum",
            "contrato complementar", "terms of service"
        ],
        "Outros acordos": [
            "colaboração", "cooperação", "acordo comercial", "aliança",
            "parceria", "clientes", "joint venture", "associação"
        ],
        "Intercompany": [
            "mercadolibre", "grupo", "subsidiária", "empresa relacionada",
            "filial", "companhia do grupo", "intercompany", "intragroup"
        ],
        "Fondeo": [
            "empréstimo", "financiamento", "crédito", "funding", "loan",
            "financing", "credit facility"
        ],
        "Investimento": [
            "investimento", "investment", "participação", "acciones",
            "equity", "fundo", "capital", "aporte"
        ],
        "Cobertura / Hedge": [
            "hedge", "cobertura", "proteção financeira", "derivativo",
            "swap", "financial coverage", "hedging"
        ],
        "Garantias": [
            "garantia", "fiança", "aval", "guarantee", "bond", "collateral"
        ],
        "Outros": [
            "venda", "sales", "contrato comercial", "parceria comercial"
        ]
    }
}

# ===== Termos-chave com pesos diferenciados =====

TERMOS_CHAVE = {
    # ===================== COMPRAS =====================
    "Realização de obra": {
        "obra": 3.0,
        "construção": 3.0,
        "construction": 3.0,
        "reforma": 2.5,
        "renovation": 2.5,
        "obra civil": 2.5,
        "civil work": 2.5,
        "execução de obra": 2.5
    },

    "Prestação de serviço": {
        "prestação de serviço": 3.0,
        "prestação de serviços": 3.0,
        "serviço": 2.5,
        "servicio": 2.5,
        "service": 2.5,
        "serviços técnicos": 2.0,
        "maintenance": 2.0,
        "outsourcing": 2.0,
        "consultoria": 2.0
    },

    "Compra de equipamentos": {
        "equipamento": 3.0,
        "equipamentos": 3.0,
        "equipment": 3.0,
        "maquinário": 2.5,
        "maquinaria": 2.5,
        "machinery": 2.5,
        "hardware": 2.0,
        "electronic equipment": 2.0
    },

    "Compra de produtos": {
        "fornecimento de materiais": 3.0,
        "suministros": 2.5,
        "supplies": 2.5,
        "goods": 2.5,
        "insumo": 2.0,
        "procurement": 2.0,
        "mercadoria": 2.0
    },

    "Aluguel de bens": {
        "locação de equipamentos": 3.0,
        "equipment rental": 3.0,
        "leasing": 2.5,
        "arrendamento": 2.0,
        "comodato": 2.0
    },

    "Aluguel de imóveis": {
        "imóvel": 3.0,
        "imóveis": 3.0,
        "locação": 2.5,
        "locacao": 2.5,
        "contrato de locação": 3.0,
        "aluguel de imóvel": 3.0,
        "locataria": 2.0,
        "locadora": 2.0,
        "real estate": 2.0,
        "lease": 2.0
    },

    "Transporte": {
        "transporte": 3.0,
        "logística": 2.5,
        "logistics": 2.5,
        "frete": 2.5,
        "shipping": 2.5,
        "delivery": 2.0,
        "courier": 2.0
    },

    "Publicidade e marketing": {
        "marketing": 3.0,
        "publicidade": 3.0,
        "advertising": 3.0,
        "campanha": 2.5,
        "promotion": 2.5,
        "branding": 2.0,
        "sponsorship": 2.0
    },

    "Operação logística": {
        "centro de distribuição": 3.0,
        "warehouse": 3.0,
        "fulfillment center": 2.5,
        "supply chain": 2.5,
        "operação logística": 2.5,
        "armazenagem": 2.0
    },

    "Licenças e software": {
        "software": 3.0,
        "licença": 2.5,
        "license": 2.5,
        "assinatura": 2.5,
        "subscription": 2.5,
        "saas": 2.0,
        "cloud": 2.0
    },

    "Outros": {
        "fornecedor": 2.0,
        "supplier": 2.0,
        "provider": 2.0
    },

    # ===================== VENDAS =====================
    "Acordos T&C": {
        "termos e condições": 3.0,
        "terms and conditions": 3.0,
        "termos de uso": 2.5,
        "addendum": 2.0,
        "appendix": 2.0,
        "terms of service": 2.0
    },

    "Outros acordos": {
        "acordo comercial": 3.0,
        "parceria": 2.5,
        "aliança": 2.5,
        "joint venture": 2.5,
        "colaboração": 2.0,
        "mou": 2.0,
        "loi": 2.0,
        "memorando de entendimento": 2.0
    },

    "Intercompany": {
        "intercompany": 3.0,
        "intragroup": 2.5,
        "grupo": 2.5,
        "empresa relacionada": 2.5,
        "filial": 2.0,
        "companhia do grupo": 2.0
    },

    "Fondeo": {
        "empréstimo": 3.0,
        "loan": 3.0,
        "financiamento": 2.5,
        "crédito": 2.5,
        "credit facility": 2.5,
        "funding": 2.0,
        "financing": 2.0
    },

    "Investimento": {
        "investimento": 3.0,
        "investment": 3.0,
        "equity": 2.5,
        "participação": 2.5,
        "capital": 2.5,
        "share purchase": 2.0,
        "aporte": 2.0
    },

    "Cobertura / Hedge": {
        "hedge": 3.0,
        "hedging": 2.5,
        "cobertura": 2.5,
        "derivativo": 2.5,
        "derivative": 2.5,
        "swap": 2.0
    },

    "Garantias": {
        "garantia": 3.0,
        "guarantee": 3.0,
        "fiança": 2.5,
        "aval": 2.5,
        "bond": 2.5,
        "collateral": 2.0
    },

    "Outros": {
        "venda": 3.0,
        "sales": 3.0,
        "contrato comercial": 2.5,
        "parceria comercial": 2.0
    }
}


import pdfplumber
import re
import unicodedata
from difflib import SequenceMatcher
from collections import defaultdict
import os
import pandas as pd

# ===== Caminhos =====
input_dir = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Matriz de arquivos"
output_dir = r"G:\Drives compartilhados\Legales_Analytics\002 - Python\002-1 - DEV\Dev - CLM Ma e Mu\Resultado"
output_final = os.path.join(output_dir, "Analise contextual.xlsx")
consolidado_path = os.path.join(output_dir, "Analise_contextual_CONSOLIDADO.xlsx")

# ====== Carregar consolidado existente (para ignorar duplicados) ======
if os.path.exists(consolidado_path):
    consolidado_df = pd.read_excel(consolidado_path)
    arquivos_consolidados = set(consolidado_df["Arquivo"].astype(str).str.lower().tolist())
    print(f"📚 Consolidado encontrado ({len(arquivos_consolidados)} arquivos já processados).")
else:
    arquivos_consolidados = set()
    print("⚠️ Nenhum consolidado encontrado — todos os PDFs serão analisados.")

# ===== Funções utilitárias =====
def normalize_text(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9\s]", " ", txt.lower())

def limpar_emails(texto):
    return re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", texto)

# ===== Classificação contextual =====
def classificar_contexto(texto):
    texto = limpar_emails(texto)
    texto_norm = normalize_text(texto)
    scores = defaultdict(float)

    for cat, subs in CATEGORIAS.items():
        for sub, termos in subs.items():
            for termo in termos:
                termo_norm = termo.lower().strip()
                if not termo_norm:
                    continue
                count = texto_norm.count(termo_norm)
                if count == 0:
                    continue
                peso = TERMOS_CHAVE.get(sub, {}).get(termo_norm, 1.0)
                sim = SequenceMatcher(None, termo_norm, texto_norm).ratio()
                score = (0.5 + sim) * count * peso
                scores[(cat, sub)] += score

    if not scores:
        return "—", "—", 0, "—", 0, "—"

    categoria_scores = defaultdict(float)
    for (cat, _), valor in scores.items():
        categoria_scores[cat] += valor

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    (cat_melhor, sub_melhor), _ = ranking[0]

    ranking_cat = sorted(categoria_scores.items(), key=lambda x: x[1], reverse=True)
    cat_top, score_cat_top = ranking_cat[0]
    score_cat_seg = ranking_cat[1][1] if len(ranking_cat) > 1 else 0
    dominancia_cat = (score_cat_top - score_cat_seg) / (score_cat_seg + 1e-6)
    proporcao_cat = score_cat_top / (sum(categoria_scores.values()) + 1e-6)
    conf_cat = (0.7 * dominancia_cat + 0.3 * proporcao_cat) * 100
    conf_cat = min(100, max(1, conf_cat))

    subs_dessa_cat = {k[1]: v for k, v in scores.items() if k[0] == cat_top}
    ranking_subs = sorted(subs_dessa_cat.items(), key=lambda x: x[1], reverse=True)
    sub_top, score_sub_top = ranking_subs[0]
    score_sub_seg = ranking_subs[1][1] if len(ranking_subs) > 1 else 0
    dominancia_sub = (score_sub_top - score_sub_seg) / (score_sub_seg + 1e-6)
    proporcao_sub = score_sub_top / (sum(subs_dessa_cat.values()) + 1e-6)
    conf_sub = (0.7 * dominancia_sub + 0.3 * proporcao_sub) * 100
    conf_sub = min(100, max(1, conf_sub))

    def nivel_conf(c):
        if c >= 85: return "Alta"
        if c >= 70: return "Média-Alta"
        if c >= 55: return "Média"
        if c >= 40: return "Média-Baixa"
        return "Baixa"

    return cat_melhor, sub_melhor, round(conf_cat, 2), nivel_conf(conf_cat), round(conf_sub, 2), nivel_conf(conf_sub)

# ===== Processamento em massa =====
resultados = []
arquivos_pdf = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
os.makedirs(output_dir, exist_ok=True)

print(f"🔍 Encontrados {len(arquivos_pdf)} PDFs no diretório.\n")

for i, nome_arquivo in enumerate(arquivos_pdf, start=1):
    nome_lower = nome_arquivo.lower()
    if nome_lower in arquivos_consolidados:
        print(f"[{i}/{len(arquivos_pdf)}] ⏭️ {nome_arquivo} já presente no consolidado. Pulando.")
        continue

    caminho = os.path.join(input_dir, nome_arquivo)
    try:
        with pdfplumber.open(caminho) as pdf:
            texto_total = "\n".join((page.extract_text() or "") for page in pdf.pages)

        categoria, subcategoria, conf_cat, nivel_cat, conf_sub, nivel_sub = classificar_contexto(texto_total)
        resultados.append({
            "Arquivo": nome_arquivo,
            "Categoria": categoria,
            "Confiança Categoria (%)": conf_cat,
            "Nível Categoria": nivel_cat,
            "Subcategoria": subcategoria,
            "Confiança Subcategoria (%)": conf_sub,
            "Nível Subcategoria": nivel_sub
        })

        print(f"[{i}/{len(arquivos_pdf)}] ✅ {nome_arquivo} → {categoria} / {subcategoria}")

        # === Checkpoint automático a cada 100 PDFs ===
        if i % 100 == 0:
            temp_path = os.path.join(output_dir, f"Analise contextual_temp_{i}.xlsx")
            pd.DataFrame(resultados).to_excel(temp_path, index=False)
            print(f"💾 Checkpoint salvo ({i} PDFs): {temp_path}")

    except Exception as e:
        print(f"[{i}/{len(arquivos_pdf)}] ⚠️ Erro ao processar {nome_arquivo}: {e}")
        resultados.append({
            "Arquivo": nome_arquivo,
            "Categoria": "Erro",
            "Confiança Categoria (%)": 0,
            "Nível Categoria": "—",
            "Subcategoria": "Erro",
            "Confiança Subcategoria (%)": 0,
            "Nível Subcategoria": str(e)
        })

# ===== Salvar resultado final =====
if resultados:
    df = pd.DataFrame(resultados)
    df.to_excel(output_final, index=False)
    print(f"\n✅ Análise concluída! Resultado salvo em:\n{output_final}")
else:
    print("\nℹ️ Nenhum novo arquivo foi processado (todos já estavam no consolidado).")
