import os
# Configuración de entorno
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["UNSLOTH_OFFLOAD_GRADIENTS"] = "0" 

from unsloth import FastLanguageModel, get_chat_template
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. Cargar Modelo Llama 3.2 1B
max_seq_length = 2048
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length = max_seq_length,
    load_in_4bit = True,
)

# 2. Configurar adaptadores LoRA (MÁS FUERTES)
# Aumentamos r a 32 y alpha a 64 para que el entrenamiento "pese" más que el modelo base
model = FastLanguageModel.get_peft_model(
    model,
    r = 32, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 64, 
    lora_dropout = 0,
    bias = "none",    
    use_gradient_checkpointing = "unsloth",
)

# 3. Formato de Chat
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3.2",
)

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

# 4. Cargar Dataset
dataset = load_dataset("json", data_files=r"C:\Users\rival\Documents\IA\Inteligencia-Artificial\Proyectos\TutorCoding\tutor_dataset.jsonl", split="train")
dataset = dataset.map(formatting_prompts_func, batched = True)

# 5. Entrenador optimizado
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, 
    args = TrainingArguments(
        per_device_train_batch_size = 4,
        gradient_accumulation_steps = 4,
        # Cambiamos max_steps por num_train_epochs para dar vueltas completas al dataset
        num_train_epochs = 3, 
        learning_rate = 1e-4, # Un poco más bajo para mayor precisión
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "cosine", # Mejora la convergencia al final
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
    ),
)

# 6. Entrenar
trainer.train()

# 7. Guardar de forma SEGURA para mover a otra PC
# Primero guardamos los adaptadores (pequeños)
model.save_pretrained("tutor_llama_1b_adapters")
tokenizer.save_pretrained("tutor_llama_1b_adapters")

# Segundo, hacemos el MERGE para tener el modelo de 2.3GB listo para Windows
print("Iniciando fusión de pesos (Merge)...")
model.save_pretrained_merged(
    "my_final_model", 
    tokenizer, 
    save_method = "merged_16bit"
)