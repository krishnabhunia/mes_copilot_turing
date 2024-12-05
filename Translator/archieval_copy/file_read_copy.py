from transformers import MarianMTModel, MarianTokenizer


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


file_path = 'input/file_text.txt'
with open(file_path, 'r') as f:
    content = f.read()
    # Translate content
    translated_content = translate_text(content, tokenizer, model)
    print(translate_text)


print(content)
words = content.split()
# print(words)

count_word = {}
for word in words:
    if word in count_word:
        count_word[word] += 1
    else:
        count_word[word] = 1

# print(count_word)

for word, count in count_word.items():
    if count > 9:
        print(f"{word}: {count}")


# Save to output folder
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(translated_content)

print(f"Translated {file_name} and saved to {output_file_path}")

print("Translation completed.")
