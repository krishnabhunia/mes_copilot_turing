import asyncio
import translator
import logging
import Helper
import argparse
import lang_detector
import os
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


async def file_translate_main(input_file, target_lang, output_folder, custome_file_name_prefix):
    try:
        translate_file = translator.Translator()
        input_path = os.getenv("INPUT_FOLDER_TO_BE_TRANSLATED") or translate_file.input_folder
        input_file_path = os.path.join(input_path, input_file)
        source_lang = lang_detector.detect_language(input_file_path)

        # user_output_file_name = translate_file.custom_execution(input_file_path, source_lang[0], target_lang, output_folder, custome_file_name_prefix)
        user_output_file_name = await asyncio.to_thread(translate_file.custom_execution, input_file_path, source_lang[0], target_lang, output_folder, custome_file_name_prefix)
        
        logging.info(f"Translation Completed For File {input_file_path}")
        # return output_file_path output_filename file_type
        return user_output_file_name
    except Exception as ex:
        logging.error(ex)


if __name__ == "__main__":
    args = read_custom_arguement()
    translate_file = translator.Translator()
    source_lang = lang_detector.detect_language(args.input_file_path)
    translate_file.custom_execution(args.input_file_path, source_lang[0], args.target_lang, args.output_folder)
    logging.info(f"Translation Completed For File {args.input_file_path}")
