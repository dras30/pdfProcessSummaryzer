import fitz
import json
import os

# 🔥 VOCÊ ALTERA AQUI DEPENDENDO DO LOTE!
CAUSA_RAIZ = "ALEGAÇÃO DE FRAUDE"
PRODUTO = "CONTA CORRENT"

def extrair_texto(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([p.get_text() for p in doc])

dataset = []

for arquivo in os.listdir("./pdfs"):
    if arquivo.lower().endswith(".pdf"):
        texto = extrair_texto(f"./pdfs/{arquivo}")

        entry = {
            "instruction": "Gerar JSON completo do processo.",
            "input": {
                "textoProcesso": texto,
                "causaRaiz": CAUSA_RAIZ,
                "produto": PRODUTO
            },
            "output": {
                "content": texto,
                "causaRaiz": CAUSA_RAIZ,
                "produto": PRODUTO,
                "sinonimosCausaRaiz": [
                 "sinonimo1",
                 "sinonimo2",
                 "sinonimo2"
                 ],
                "sinonimosProduto": [
                 "sinonimoproduto1", 
                 "sinonimoproduto2",
                 "sinonimoproduto2"
                 ],
                "mustTerms": [
                 "term1", 
                 "term2", 
                 "term3"
                ], 
                "antiTerms": [
                "term1", 
                "term2", 
                "term3"
                ]
            }
        }

        dataset.append(entry)

with open("dataset/dataset.jsonl", "w", encoding="utf-8") as f:
    for d in dataset:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

print("dataset.jsonl gerado com sucesso!")
