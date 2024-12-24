from transformers import MarianMTModel, MarianTokenizer  # type: ignore
import os
from itertools import permutations
import logging
import Helper


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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


if __name__ == "__main__":
    # Get all language pairs with English
    comb = list(permutations(Helper.get_language_list(), 2))
    language_pairs = comb
    # language_pairs_with_en = [combo for combo in comb if 'en' in combo]
    # for source, target in language_pairs_with_en:
    #     logging.info(f"Downloading model for {source} -> {target}")

    for source, target in language_pairs:
        logging.info(f"Downloading model for {source} -> {target}")
        download_model(source, target)
