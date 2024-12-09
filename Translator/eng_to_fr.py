import json
from transformers import pipeline  # type: ignore

# Load the translation model
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")

# Read the JSON file
input_file = 'output.json'
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Translate and populate values
for key, value in data.items():
    if not value:  # Check if value is blank
        translated_text = translator(key)[0]['translation_text']
        data[key] = translated_text

# Write back to the JSON file
with open('file.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Translation completed offline and updated in the JSON file.")
