import os
from transformers import MarianMTModel, MarianTokenizer

# Define paths
input_folder = 'input'
output_folder = 'translated_document'

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Load MarianMT model and tokenizer for English to French translation
model_name = 'Helsinki-NLP/opus-mt-en-fr'
model_name = 'google-t5/t5-small'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate text
def translate_text(text, tokenizer, model):
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    translated_tokens = model.generate(tokens, max_length=512, num_beams=5, early_stopping=True)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# Iterate through files in the input folder
for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name)
    
    if os.path.isfile(input_file_path):
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Translate content
        translated_content = translate_text(content, tokenizer, model)
        
        # Save to output folder
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"Translated {file_name} and saved to {output_file_path}")

print("Translation completed.")
