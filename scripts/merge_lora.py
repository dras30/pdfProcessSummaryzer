# Parte de merge da LoRA
import torch
from transformers import LoraConfig, get_peft_model, PeftModel

def merge_lora_model(base_model_path, lora_model_path, output_model_path):
    # Carregar o modelo base
    base_model = torch.load(base_model_path)

    # Configuração LoRA (ajuste conforme necessário)
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # Aplicar LoRA ao modelo base
    peft_model = get_peft_model(base_model, lora_config)

    # Carregar pesos LoRA
    peft_model.load_state_dict(torch.load(lora_model_path), strict=False)

    # Mesclar os pesos LoRA no modelo base
    merged_model = peft_model.merge_and_unload()

    # Salvar o modelo mesclado
    torch.save(merged_model, output_model_path)
    print(f"Modelo mesclado salvo em: {output_model_path}")

# Exemplo de uso
if __name__ == "__main__":
    base_model_path = "caminho/para/o/modelo/base.pt"
    lora_model_path = "caminho/para/o/modelo/lora.pt"
    output_model_path = "caminho/para/salvar/o/modelo/mesclado.pt"

    merge_lora_model(base_model_path, lora_model_path, output_model_path)
    