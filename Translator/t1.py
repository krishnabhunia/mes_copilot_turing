from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the mT5 model and tokenizer
model_name = "google/mt5-small"  # Use other variants like 'mt5-base' or 'mt5-large' if needed
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Define the source and target languages
source_language = "en"  # English
target_language = "fr"  # French
text_to_translate = "Good morning"

# Prepare the input text in the T5 format
input_text = f"translate {source_language} to {target_language}: {text_to_translate}"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate translation
outputs = model.generate(**inputs)
translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Original Text:", text_to_translate)
print("Translated Text:", translated_text)