import os
from transformers import MarianMTModel, MarianTokenizer

class OfflineTranslator:
    def __init__(self, model_base_path="./local_models"):
        self.model_base_path = model_base_path

    def load_model(self, source_lang, target_lang):
        """
        Load the translation model and tokenizer from the local directory.

        Args:
            source_lang (str): Source language code (e.g., "en").
            target_lang (str): Target language code (e.g., "fr").

        Returns:
            tuple: (MarianTokenizer, MarianMTModel)
        """
        model_path = os.path.join(self.model_base_path, f"{source_lang}-{target_lang}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model directory not found: {model_path}")

        print(f"Loading model from {model_path}...")
        tokenizer = MarianTokenizer.from_pretrained(model_path)
        model = MarianMTModel.from_pretrained(model_path)
        return tokenizer, model

    def translate(self, text, source_lang, target_lang):
        """
        Translate text using the locally saved model.

        Args:
            text (str): Text to translate.
            source_lang (str): Source language code.
            target_lang (str): Target language code.

        Returns:
            str: Translated text.
        """
        tokenizer, model = self.load_model(source_lang, target_lang)
        tokens = tokenizer.encode(text, return_tensors="pt", truncation=True)
        translated_tokens = model.generate(tokens)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text

# Example Usage
if __name__ == "__main__":
    translator = OfflineTranslator(model_base_path="./local_models")
    source_lang = "en"
    target_lang = "fr"
    text = "Hello, how are you?"

    try:
        translated_text = translator.translate(text, source_lang, target_lang)
        print(f"Translated text: {translated_text}")
    except FileNotFoundError as e:
        print(e)
