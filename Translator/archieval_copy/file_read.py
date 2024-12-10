import os
from transformers import MarianMTModel, MarianTokenizer  # type: ignore


# Define paths
input_folder = 'input'
output_folder = 'translated_document'
custom_cache_directory = 'cache'
os.environ["HF_HOME"] = "cache"
print(os.environ.get("HF_HOME"))

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress TensorFlow logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN optimizations

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)
os.makedirs(custom_cache_directory, exist_ok=True)

# Load MarianMT model and tokenizer for English to French translation
model_name = 'Helsinki-NLP/opus-mt-en-fr'
# model_name = 'google-t5/t5-small'
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=custom_cache_directory)
model = MarianMTModel.from_pretrained(model_name, cache_dir=custom_cache_directory)


# Function to translate text
def translate_text(text, tokenizer, model):
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    translated_tokens = model.generate(tokens, max_length=512, num_beams=5, early_stopping=True)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)


input_file_name = 'krishna.txt'
input_file_path = f'{input_folder}/{input_file_name}'

if os.path.isfile(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        print('File Reading ... ')
        content = f.read()
        print('File Reading Completed')

    # Translate content
    print('Trying to translate ... ')
    translated_content = translate_text(content, tokenizer, model)
    print('Translate complete')
    print(translated_content)

    output_file_name = f'translated_{input_file_name}'
    output_file_path = f'{output_folder}/{output_file_name}'
    # Save to output folder
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
