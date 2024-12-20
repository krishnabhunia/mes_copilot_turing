import subprocess
import logging
import os
import lang_detector
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_normal():
    input_folder = "inp eng"
    output_folder = "out eng"
    lang_list = ['zh', 'es', 'fr', 'de', 'nl', 'it', 'hu', 'pt', 'fi', 'sv']
    for lang in lang_list:
        logging.info(f"Execution started for : 'en' '{lang}'")
        run_test('en', lang, input_folder, output_folder)
        logging.info("Loop complete")

    for file_name in os.listdir(output_folder):
        out_lang = lang_detector.detect_language(file_name)
        run_test(out_lang, 'en',  input_folder, output_folder)
        logging.info("Loop complete")


def run_test(exist_lang, new_lang, input_folder, output_folder):
    # Define the script and arguments
    script_name = "translator.py"

    # Execute the script with arguments
    try:
        result = subprocess.run(
            ["python", script_name, exist_lang, new_lang, "--input_folder", input_folder, "--output_folder", output_folder],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("Output:", result.stdout)
        logging.error("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    run_normal()
