import pandas as pd
import json
import torch
from transformers import pipeline
from tqdm import tqdm
import os

# Configuración de hardware
device = 0 if torch.cuda.is_available() else -1
print(f"Usando dispositivo: {'GPU (CUDA)' if device == 0 else 'CPU'}")

# Cargar el modelo con configuración de longitud extendida
translator = pipeline(
    "translation", 
    model="Helsinki-NLP/opus-mt-en-es", 
    device=device
)

def translate_and_convert(input_csv, output_json, batch_size=32):
    df = pd.read_csv(input_csv)
    df.columns = [c.strip().lower() for c in df.columns]
    
    col_input = 'question' 
    col_output = 'answer'

    final_data = []
    if os.path.exists(output_json):
        with open(output_json, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        print(f"Progreso cargado: {len(final_data)} entradas.")

    start_idx = len(final_data)
    total_rows = len(df)

    # Procesar por lotes
    for i in tqdm(range(start_idx, total_rows, batch_size)):
        batch_df = df.iloc[i:i+batch_size]
        
        # Limitar a 512 caracteres antes de enviar al traductor para ganar velocidad
        # Los textos más largos que eso suelen ser basura o logs en datasets grandes
        inputs_to_translate = [str(x)[:1000] for x in batch_df[col_input].tolist()]
        outputs_to_translate = [str(x)[:1000] for x in batch_df[col_output].tolist()]
        
        try:
            # max_length aumentado para evitar los warnings
            trans_inputs = translator(inputs_to_translate, max_length=512, truncation=True)
            trans_outputs = translator(outputs_to_translate, max_length=512, truncation=True)
            
            for j, (in_res, out_res) in enumerate(zip(trans_inputs, trans_outputs)):
                final_data.append({
                    "input": in_res['translation_text'],
                    "output": out_res['translation_text']
                })
            
            # Guardar cada 200 filas para mayor seguridad
            if i % 200 == 0:
                with open(output_json, 'w', encoding='utf-8') as f:
                    json.dump(final_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"\nError en bloque {i}: {e}")
            continue

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

# Ejecutar
translate_and_convert(r'C:\Users\rival\Downloads\archive(1)\train.csv', 'dataset_traducido.json')