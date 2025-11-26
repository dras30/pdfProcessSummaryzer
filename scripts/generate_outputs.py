import json
import requests

API_URL = "http://localhost:11434/api/generate"  # Ex. OLLAMA local

def gerar_output(texto, causa, produto, sinonimosCausaRaiz, sinonimosProduto, mustTerms, antiTerms):
    prompt = f"""
Importante:
- NÃO ALTERE os valores de causaRaiz e produto.
- Somente copie esses valores para o JSON final.
- Gere os demais campos com base no texto e nesses valores.

Gerar JSON completo:

Texto:
{texto}

Causa raiz: {causa}
Produto: {produto}
Sinonimos Causa Raiz: {sinonimosCausaRaiz}
Sinonimos Produto: {sinonimosProduto}
Must Terms: {mustTerms}
Anti Terms: {antiTerms}
"""

    response = requests.post(API_URL, json={"model": "llama3", "prompt": prompt})
    return response.json()["response"]

linhas = []
with open("dataset/dataset.jsonl", encoding="utf-8") as f:
    for linha in f:
        item = json.loads(linha)

        out = gerar_output(
            item["input"]["textoProcesso"],
            item["input"]["causaRaiz"],
            item["input"]["produto"],
            item["input"]["sinonimosCausaRaiz"],
            item["input"]["sinonimosProduto"],
            item["input"]["mustTerms"],
            item["input"]["antiTerms"]
        )

        item["output"] = json.loads(out)
        linhas.append(item)

with open("dataset/dataset.jsonl", "w", encoding="utf-8") as f:
    for l in linhas:
        f.write(json.dumps(l, ensure_ascii=False) + "\n")
