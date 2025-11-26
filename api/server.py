from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("model/final")
model = AutoModelForCausalLM.from_pretrained("model/final", device_map="auto")

class Processo(BaseModel):
    textoProcesso: str
    causaRaiz: str
    produto: str

@app.post("/gerar")
def gerar(p: Processo):
    prompt = f"""
Importante:
- NÃO ALTERE os valores de causaRaiz e produto.
- Somente copie esses valores para a resposta.
- Gere os demais campos corretamente.

Texto:
{p.textoProcesso}

Causa raiz: {p.causaRaiz}
Produto: {p.produto}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=1800)
    texto = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"json": texto}
