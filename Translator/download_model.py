from transformers import MarianMTModel, MarianTokenizer  # type: ignore
import os


def download_model(source_lang, target_lang, model_dir="offline_models"):
    """
    Download and save MarianMTModel and MarianTokenizer locally.
    
    Args:
        source_lang (str): Source language code (e.g., "en").
        target_lang (str): Target language code (e.g., "fr").
        model_dir (str): Directory to save models.
    """
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    save_path = os.path.join(model_dir, f"{source_lang}-{target_lang}")
    os.makedirs(save_path, exist_ok=True)

    print(f"Downloading model: {model_name}")
    MarianMTModel.from_pretrained(model_name).save_pretrained(save_path)
    MarianTokenizer.from_pretrained(model_name).save_pretrained(save_path)
    print(f"Model saved to: {save_path}")


# Pre-download models for desired language pairs
language_pairs = [("en", "fr"), ("fr", "en"), ("en", "es"), ("es", "en")]
for source, target in language_pairs:
    download_model(source, target)
