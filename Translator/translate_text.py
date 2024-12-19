import translator
import argparse
import logging
import Helper
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@staticmethod  # type:ignore
def read_arguement():
    parser = argparse.ArgumentParser(description="Translator Script")

    # Define required positional arguments
    parser.add_argument('target_lang', help='Compulsory target language (e.g., fr)')
    parser.add_argument('text', help='Compulsory text to be translated (e.g., "Hi Capgemini")')

    # Optional argument
    parser.add_argument('--source_lang', default='en', help='Optional source language (default: en)')

    args = parser.parse_args()

    logging.info(f"Arguments parsed: '{args.source_lang}' and name: {Helper.get_language_name(args.source_lang)}")
    logging.info(f"Arguments parsed: '{args.target_lang}' and name: {Helper.get_language_name(args.target_lang)}")
    logging.info(f"Arguments parsed: '{args.text}'")

    return args


if __name__ == "__main__":
    try:
        args = read_arguement()
        trans = translator.Translator(args)
        trans.initialize_translator()
        res = trans.translate(args.text)
        logging.info(f"Translated Text : {res}")
    except Exception as ex:
        print(ex)
