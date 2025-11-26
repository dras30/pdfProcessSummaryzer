from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import transformers

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

dataset = load_dataset("json", data_files="dataset/dataset.jsonl")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True,
)

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    dataset_text_field="output",
    max_seq_length=4096,
    args=transformers.TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        warmup_steps=10,
        max_steps=1500,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        output_dir="model/",
        save_strategy="epoch"
    ),
)

trainer.train()

model.save_pretrained("model/final")
tokenizer.save_pretrained("model/final")

print("Treinamento concluído!")
