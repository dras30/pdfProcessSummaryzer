import streamlit as st
import fitz  # PyMuPDF
import json
import base64
from io import BytesIO

st.set_page_config(page_title="Processador de Processos", layout="wide")

# -----------------------------
# Função para extrair texto do PDF
# -----------------------------
def extract_text(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = [page.get_text() for page in doc]
    return "\n".join(pages)

# -----------------------------
# Função para gerar JSON final
# -----------------------------
def gerar_json(texto, causaRaiz, produto, sinonimosCausaRaiz, sinonimosProduto, mustTerms, antiTerms):
    return {
        "content": texto,
        "causaRaiz": causaRaiz,
        "produto": produto,
        "sinonimosCausaRaiz": sinonimosCausaRaiz,          
        
        "sinonimosProduto": sinonimosProduto,
        
        "mustTerms": mustTerms,
        "antiTerms": antiTerms
    }

# -----------------------------
# Função para baixar JSON
# -----------------------------
def download_json(data, filename):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">📄 Baixar JSON</a>'
    return href

# -----------------------------
# INTERFACE
# -----------------------------
st.title("📄 Processador de PDFs → JSON Treinável")
st.write("Interface simples para gerar datasets locais.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    causa_raiz = st.text_input("Causa Raiz (forçada)", "")
    produto = st.text_input("Produto (forçado)", "")

with col2:
    uploaded_files = st.file_uploader(
        "Selecione um ou mais PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

process_btn = st.button("🚀 Processar PDFs")

st.divider()

# -----------------------------
# Execução
# -----------------------------
if process_btn:
    if not uploaded_files:
        st.error("Selecione ao menos um PDF.")
    elif not causa_raiz or not produto:
        st.error("Informe causaRaiz e produto.")
    else:
        st.success("Processando arquivos...")

        resultados = []

        for pdf in uploaded_files:
            pdf_bytes = pdf.read()
            texto = extract_text(pdf_bytes)

            json_saida = gerar_json(
                texto=texto,
                causaRaiz=causa_raiz,
                produto=produto,
                sinonimosCausaRaiz=[
                  "sinonimo1", 
                  "sinonimo2",
                  "sinonimo3",
                  ],
                sinonimosProduto=[
                  "sinonimoproduto1",
                  "sinonimoproduto2",
                  "sinonimoproduto3",
                  ],
                mustTerms=[
                  "term1",
                  "term2",
                  "term3"
                  ],
                antiTerms=[
                  "term1",
                  "term2",
                  "term3"
                  ]
            )

            resultados.append({
                "filename": pdf.name,
                "json": json_saida
            })

        st.subheader("Resultados")

        for item in resultados:
            st.write(f"### 📌 {item['filename']}")

            st.json(item["json"])

            st.markdown(download_json(item["json"], item["filename"] + ".json"), unsafe_allow_html=True)

        st.divider()

        # Download do dataset.jsonl para fine-tuning
        dataset_jsonl = "\n".join([
            json.dumps({
                "instruction": "Gerar JSON completo do processo.",
                "input": {
                    "textoProcesso": r["json"]["content"],
                    "causaRaiz": causa_raiz,
                    "produto": produto
                },
                "output": r["json"]
            }, ensure_ascii=False)
            for r in resultados
        ])

        b64_dataset = base64.b64encode(dataset_jsonl.encode()).decode()
        href_dataset = f'<a href="data:text/plain;base64,{b64_dataset}" download="dataset.jsonl">📥 Baixar dataset.jsonl</a>'

        st.markdown("### 📘 Dataset para Fine-Tuning")
        st.markdown(href_dataset, unsafe_allow_html=True)

        st.success("Processamento concluído!")