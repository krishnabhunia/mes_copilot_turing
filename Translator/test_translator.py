import subprocess
import logging
import os
import lang_detector
import translator
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_normal():
    input_folder = "inp eng"
    output_folder = "out eng"
    lang_list = ['zh', 'es', 'fr', 'de', 'nl', 'it', 'hu', 'pt', 'fi', 'sv']
    # lang_list = ['es', 'fr']
    for lang in lang_list:
        logging.info(f"Execution started for : 'en' '{lang}'")
        run_test('en', lang, input_folder, output_folder)
        logging.info("Loop complete")

    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)  # Construct full file path
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            try:
                logging.info(f"Execution started for: 'en' '{file_name}'")
                # Detect the language of the file
                out_lang = lang_detector.detect_language(file_path)
                print(f"Launguage detected : {out_lang}")
                translate_file = translator.Translator()
                input_file_path = os.path.join(output_folder, file_name)
                translate_file.custom_execution(input_file_path, out_lang[0], 'en')

                # run_test(out_lang[0], 'en', output_folder, "output_folder_to_eng")
                logging.info(f"Execution completed for: 'en' '{file_name}'")
            except Exception as e:
                logging.error(f"Error processing file '{file_name}': {e}")
        else:
            logging.warning(f"Skipping non-file entry: {file_name}")


def run_test(exist_lang, new_lang, input_folder, output_folder):
    """
    Run the translator script with the provided arguments.

    Args:
        exist_lang (str): Source language.
        new_lang (str): Target language.
        input_folder (str): Path to the input folder.
        output_folder (str): Path to the output folder.
    """
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
    except subprocess.CalledProcessError as e:
        logging.error("Errors:", e.stderr)
        logging.error(f"Error occurred: {e}")
    except Exception as ex:
        logging.error(f"Exception occurred: {ex}")


if __name__ == "__main__":
    run_normal()
