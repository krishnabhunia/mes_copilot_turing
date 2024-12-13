import translator
import argparse
import logging
import Helper
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@staticmethod  # type:ignore
def read_arguement():
    parser = argparse.ArgumentParser(description="Translator Script")
    # Define required positional arguments
    parser.add_argument('source_lang', help='Compulsory source language (e.g., fr)')
    parser.add_argument('target_lang', help='Compulsory target language (e.g., en)')
    parser.add_argument('text', help='Compulsory text to be translated "(e.g., Hi Capgemini)"')
    args = parser.parse_args()
    logging.info(f"Arguments parsed : '{args.source_lang}' and name :{Helper.get_language_name(args.source_lang)}")
    logging.info(f"Arguments parsed : '{args.target_lang}' and name :{Helper.get_language_name(args.target_lang)}")
    logging.info(f"Arguments parsed : '{args.text}'")
    return args


if __name__ == "__main__":
    try:
        trans = translator.Translator()
        trans.initialize_translator()
        args = read_arguement()
        print(trans.translate(args.source_lang))
    except Exception as ex:
        print(ex)
