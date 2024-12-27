from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the T5 tokenizer and model
model_name = "t5-large"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Input text and task prefix
source_text = "Translate English to French: Hello, how are you?"
inputs = tokenizer(source_text, return_tensors="pt", max_length=512, truncation=True)

# Generate translation
outputs = model.generate(inputs.input_ids, max_length=512, num_beams=5, early_stopping=True)

# Decode and print the translated text
translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Translated Text:", translated_text)
