import os
from transformers import MarianMTModel, MarianTokenizer  # type: ignore

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Define paths
input_folder = 'input'
output_folder = 'translated_document'
os.environ["HF_HOME"] = "cache"
os.makedirs(output_folder, exist_ok=True)

# Load MarianMT model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-fr'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Translate function
def translate_text(text, tokenizer, model):
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    translated_tokens = model.generate(tokens, max_length=512, num_beams=5, early_stopping=True)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# Translation process
input_file_name = 'krishna.txt'
input_file_path = f'{input_folder}/{input_file_name}'
if os.path.isfile(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    translated_content = translate_text(content, tokenizer, model)
    output_file_name = f'translated_{input_file_name}'
    output_file_path = f'{output_folder}/{output_file_name}'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
