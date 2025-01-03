from transformers import MarianMTModel, MarianTokenizer

# Load the model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-mul"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate English to Portuguese
def translate_english_to_portuguese(text):
    # Add the target language tag (>>por<< for Portuguese)
    text_with_tag = f">>swe<< {text}"
    # Tokenize the input text
    inputs = tokenizer(text_with_tag, return_tensors="pt", padding=True)
    # Generate translation
    translated = model.generate(**inputs)
    # Decode the generated translation
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Example usage
english_text = "How are you?, I am Krishna Bhunia, I am Generative AI Engineer"
portuguese_translation = translate_english_to_portuguese(english_text)
print(f"Original: {english_text}")
print(f"Translation: {portuguese_translation}")