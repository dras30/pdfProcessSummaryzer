processos-ia/
│
├── dataset/
│   ├── dataset.jsonl
│   ├── exemplos/
│   │   ├── exemplo1.json
│   │   ├── exemplo2.json
│   │   ├── exemplo3.json
│
├── pdfs/
│   ├── (seus PDFs aqui)
│
├── scripts/
│   ├── preprocess.py
│   ├── generate_outputs.py
│   ├── train.py
│   ├── merge_lora.py
│
├── model/
│   ├── (modelo final após treinamento)
│
├── api/
│   ├── server.py
│
├── requirements.txt
└── README.md

# Sistema de Extração Estruturada de Processos

Este projeto treina um modelo local (LLaMA/Mistral/Gemma) para gerar JSON completo
de processos extraídos de PDFs.

## Fluxo completo

1. Coloque PDFs em `/pdfs/`
2. Defina causaRaiz e produto em `scripts/preprocess.py`
3. Rode:
