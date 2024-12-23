import translator
import logging
import Helper
import argparse
import lang_detector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def read_custom_arguement():
    try:
        logging.info("Initializing Arguments ...")
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Translator Script")

        # Define required positional arguments
        parser.add_argument('target_lang', help='Compulsory target language (e.g., en)')

        # Define optional arguments
        parser.add_argument('input_file_path', help='Compulsory input file (default: None)')
        parser.add_argument('--output_folder', default=None, help='Optional output folder (default: None)')

        # Parse arguments
        args = parser.parse_args()
        # logging.info(f"Arguments parsed : '{args.source_lang}' and name :{Helper.get_language_name(args.source_lang)}")
        logging.info(f"Arguments parsed : '{args.target_lang}' and name :{Helper.get_language_name(args.target_lang)}")
        logging.info(f"Arguments parsed : '{args.input_file_path}'")
        logging.info(f"Arguments parsed : '{args.output_folder}'")
        return args
    except Exception as ex:
        logging.error(ex)


if __name__ == "__main__":
    args = read_custom_arguement()
    translate_file = translator.Translator()
    source_lang = lang_detector.detect_language(args.input_file_path)
    translate_file.custom_execution(args.input_file_path, source_lang[0], args.target_lang, args.output_folder)
    logging.info(f"Translation Completed For File {args.input_file_path}")
