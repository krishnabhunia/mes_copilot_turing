from transformers import MarianMTModel, MarianTokenizer  # type: ignore
import os
from itertools import permutations
import logging
import Helper


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def download_model(source_lang, target_lang):
    """
    Download and save MarianMTModel and MarianTokenizer locally.

    Args:
        source_lang (str): Source language code (e.g., "en").
        target_lang (str): Target language code (e.g., "fr").
        model_dir (str): Directory to save models.
    """
    cache_base_dir = "./cache"
    base_name = os.getenv("TRANSFORMER_BASE_MODEL_NAME") or "Helsinki-NLP"
    translation_type = os.getenv("TRANSLATION_TYPE") or "opus-mt"
    model_name = f"{base_name}/{translation_type}-{source_lang}-{target_lang}"
    model_path_name = os.path.join(cache_base_dir, model_name)
    os.makedirs(model_name, exist_ok=True)

    print(f"Downloading model: {model_name}")
    MarianMTModel.from_pretrained(model_name).save_pretrained(model_path_name)
    MarianTokenizer.from_pretrained(model_name).save_pretrained(model_path_name)
    print(f"Model saved to: {model_path_name}")


if __name__ == "__main__":
    # Get all language pairs with English
    comb = list(permutations(Helper.get_language_list(), 2))
    comb = list(permutations(['en','fr'], 2))
    language_pairs = comb
    language_pairs_with_en = [combo for combo in comb if 'en' in combo]
    # for source, target in language_pairs_with_en:
    #     logging.info(f"Downloading model for {source} -> {target}")

    for source, target in language_pairs_with_en:
        logging.info(f"Downloading model for :{source} -> {target}")
        download_model(source, target)