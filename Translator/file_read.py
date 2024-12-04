from transformers import MarianMTModel, MarianTokenizer


# Load MarianMT model and tokenizer for English to French translation
model_name = 'Helsinki-NLP/opus-mt-en-fr'
# model_name = 'google-t5/t5-small'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


# Function to translate text
def translate_text(text, tokenizer, model):
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    translated_tokens = model.generate(tokens, max_length=512, num_beams=5, early_stopping=True)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)


file_path = 'input/file_text.txt'
with open(file_path, 'r') as f:
    print('File Reading ... ')
    content = f.read()
    print('File Reading Completed')

# Translate content
print('Trying to translate ... ')
translated_content = translate_text(content, tokenizer, model)
print('Translate complete')
print(translate_text)
