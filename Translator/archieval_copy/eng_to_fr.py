import json
from transformers import MarianMTModel, MarianTokenizer  # type: ignore

# Load MarianMT model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-fr'
print("tokenizer intializing ...")
tokenizer = MarianTokenizer.from_pretrained(model_name)
print("tokenizer initialized, model initializing ...")
model = MarianMTModel.from_pretrained(model_name)
print("model initialized")


# Translate function
def translate_text(text, tokenizer, model):
    print('token encoding ...')
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    print('token encoded, model generating tokens ...')
    translated_tokens = model.generate(tokens, max_length=512, num_beams=5, early_stopping=True)
    print('translated token generated, returning tokens')
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)


# Read the JSON file
input_file = 'output.json'
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)


# Translate and populate values
for da in data:
    for d in da.items():
        da[d[0]] = translate_text(d[0], tokenizer, model)

# Write back to the JSON file
with open(input_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Translation completed offline and updated in the JSON file.")
