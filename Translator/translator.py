import os
import shutil
from dotenv import load_dotenv  # type: ignore
from transformers import MarianMTModel, MarianTokenizer, T5Tokenizer, T5ForConditionalGeneration  # type: ignore
import zipfile
import json
from PyPDF2 import PdfReader  # type: ignore
from xml.etree import ElementTree as ET
import Helper
from tqdm import tqdm  # type: ignore
from datetime import datetime
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Suppress TensorFlow logs and CUDA initialization
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Only errors
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN optimizations
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU usage completely


load_dotenv()


class Translator:
    def __init__(self, args=None) -> None:
        try:
            logging.debug("Initializing ...")
            self.input_folder = getattr(args, "input_folder", None) or os.getenv("INPUT_FOLDER_TO_BE_TRANSLATED") or "Input"
            self.output_folder = getattr(args, "output_folder", None) or os.getenv("OUTPUT_FOLDER_TRANSLATED") or "Output"
            self.temp_folder = os.getenv("TEMPORARY_TRANSLATION_FOLDER") or "Temporary"
            self.temp_file = os.getenv("TEMPORARY_TRANSLATION_FILE") or "Temporary_File"
            self.translate_text_length = int(os.getenv("TRANSLATION_TEXT_LENGTH")) or 512  # type: ignore
            self.translated_file_prefix = os.getenv("TRANSLATED_FILE_PREFIX") or "Translated"
            self.temp_file_extension = "json"
            self.temp_xml_document = "document.xml"
            self.chunk_size = int(os.getenv("CHUNK_SIZE")) or 512  # type: ignore
            self.source_lang = getattr(args, "source_lang", None) or os.getenv("DEFAULT_SOURCE_LANG") or "en"
            self.target_lang = getattr(args, "target_lang", None) or os.getenv("DEFAULT_TARGET_LANG") or "fr"
            self.delete_folder = getattr(args, "delete_folder", None)
            self.cache_base_dir = "./cache"
            self.google_translator_model = os.getenv("GOOGLE_TRANSLATOR") or "t5-large"
            self.google_translator_status = os.getenv("GOOGLE_TRANSLATOR_STATUS") or 'False'
        except ValueError as vex:
            logging.error(vex)
        except Exception as ex:
            logging.error(ex)

    @staticmethod
    def read_arguement():
        try:
            logging.info("Initializing Arguments ...")
            # Create the argument parser
            parser = argparse.ArgumentParser(description="Translator Script")

            # Define required positional arguments
            parser.add_argument('source_lang', help='Compulsory source language (e.g., fr)')
            parser.add_argument('target_lang', help='Compulsory target language (e.g., en)')

            # Define optional arguments
            parser.add_argument('--input_folder', default=None, help='Optional input folder (default: None)')
            parser.add_argument('--output_folder', default=None, help='Optional output folder (default: None)')
            parser.add_argument('--delete_folder', action='store_true', help='Flag to delete folders (default: False)')

            # Parse arguments
            args = parser.parse_args()
            logging.info(f"Arguments parsed : '{args.source_lang}' and name :{Helper.get_language_name(args.source_lang)}")
            logging.info(f"Arguments parsed : '{args.target_lang}' and name :{Helper.get_language_name(args.target_lang)}")
            logging.info(f"Arguments parsed : '{args.input_folder}'")
            logging.info(f"Arguments parsed : '{args.output_folder}'")
            logging.info(f"Delete arguement parsed : '{args.delete_folder}'")
            return args
        except Exception as ex:
            logging.error(ex)

    @staticmethod
    def read_custom_arguement():
        try:
            logging.info("Initializing Arguments ...")
            # Create the argument parser
            parser = argparse.ArgumentParser(description="Translator Script")

            # Define required positional arguments
            parser.add_argument('source_lang', help='Compulsory source language (e.g., fr)')
            parser.add_argument('target_lang', help='Compulsory target language (e.g., en)')

            # Define optional arguments
            parser.add_argument('input_file', help='Compulsory input file (default: None)')
            parser.add_argument('--output_folder', default=None, help='Optional output folder (default: None)')

            # Parse arguments
            args = parser.parse_args()
            logging.info(f"Arguments parsed : '{args.source_lang}' and name :{Helper.get_language_name(args.source_lang)}")
            logging.info(f"Arguments parsed : '{args.target_lang}' and name :{Helper.get_language_name(args.target_lang)}")
            logging.info(f"Arguments parsed : '{args.input_file}'")
            logging.info(f"Arguments parsed : '{args.output_folder}'")
            return args
        except Exception as ex:
            logging.error(ex)

    def initialize_translator(self):
        try:
            logging.debug("Initializing Translator ...")

            if os.getenv("USE_MULTILINGUAL_MODEL", "false").lower() == "true":
                if self.source_lang == "en":
                    translation_type = f"{os.getenv('TRANSLATION_TYPE')}-en-mul"
                    self.prepend_code = f">>{Helper.get_language_prepend_code(self.target_lang)}<<"
                else:
                    translation_type = f"{os.getenv('TRANSLATION_TYPE')}-mul-en"
                    self.prepend_code = f">>{Helper.get_language_prepend_code(self.source_lang)}<<"
            else:
                translation_type = f"{os.getenv('TRANSLATION_TYPE')}/opus-mt-{self.source_lang}-{self.target_lang}" or f"opus-mt-{self.source_lang}-{self.target_lang}"

            base_name = os.getenv("TRANSFORMER_BASE_MODEL_NAME") or "Helsinki-NLP"
            self.tensor_type = Translator.get_tensor(os.getenv("TENSOR_TYPE")) or Translator.get_tensor("pytorch")
            self.model_name = f"{base_name}/{translation_type}"
            self.model_path = os.path.join(self.cache_base_dir, self.model_name)
            logging.info(f"Translator Name : {self.model_name}")

            if not os.path.exists(os.path.join(self.cache_base_dir, self.model_name)):
                self.download_and_save_model()

            self.tokenizer = MarianTokenizer.from_pretrained(self.model_path)  # type: ignore
            self.model = MarianMTModel.from_pretrained(self.model_path)  # type: ignore
        except Exception as ex:
            logging.error(ex)

    def initialize_translator_for_google(self):
        try:
            logging.info("Initializing Translator ...")
            base_name = os.getenv("GOOGLE_TRANSLATOR") or self.google_translator_model or "t5-large"
            self.tensor_type = Translator.get_tensor(os.getenv("TENSOR_TYPE")) or Translator.get_tensor("pytorch")
            self.model_name = f"{base_name}"
            self.model_path = os.path.join(self.cache_base_dir, self.model_name)
            logging.info(f"Translator Name : {self.model_name}")

            if not os.path.exists(os.path.join(self.cache_base_dir, self.model_name)):
                self.download_and_save_model_for_google()

            self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)  # type: ignore
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)  # type: ignore
        except Exception as ex:
            logging.error(ex)

    def download_and_save_model(self):
        """
        Download translation model and tokenizer for offline use.
        """
        try:
            os.makedirs(self.model_path, exist_ok=True)

            logging.info(f"Downloading model for {self.model_name}")

            MarianMTModel.from_pretrained(self.model_name).save_pretrained(self.model_path)
            MarianTokenizer.from_pretrained(self.model_name).save_pretrained(self.model_path)

            logging.info(f"Model saved to {self.model_path}")
        except Exception as ex:
            logging.error(ex)

    def download_and_save_model_for_google(self):
        """
        Download translation model and tokenizer for offline use.
        """
        try:
            os.makedirs(self.model_path, exist_ok=True)

            logging.info(f"Downloading model for {self.model_name}")
            T5Tokenizer.from_pretrained(self.model_name).save_pretrained(self.model_path)  # type: ignore
            T5ForConditionalGeneration.from_pretrained(self.model_name).save_pretrained(self.model_path)  # type: ignore
            logging.info(f"Model saved to {self.model_path}")
        except Exception as ex:
            logging.error(ex)

    @staticmethod
    def get_tensor(req_tensor):
        try:
            tensor_map = {
                "pytorch": "pt",
                "tensorflow": "tf",
                "numpy": "np",
                "jax": "jax",
                "mlx": "mlx"
            }
            return tensor_map.get(req_tensor.lower(), None)
        except AttributeError:
            raise ValueError("Invalid tensor type provided.")
        except Exception as ex:
            logging.error(ex)

    def delete_output_folder(self):
        try:
            if self.delete_folder:
                logging.info(f"Deleting Output Folder : {self.output_folder} ... ")
                if os.path.exists(self.output_folder):  # type : ignore
                    logging.debug("Path exists , deleting folder ...")
                    shutil.rmtree(self.output_folder)
                    logging.debug(f"Folder deleted {self.output_folder}")
                else:
                    logging.debug(f"Folder doesn't exists : {self.output_folder}")
                logging.info(f"Deleting Temporary Folder : {self.temp_folder} ... ")
                if os.path.exists(self.temp_folder):
                    logging.debug("Removing temporary folders : {self.temp_folder} ... ")
                    shutil.rmtree(self.temp_folder)
                    logging.debug(f"Temporary folder removed : {self.temp_folder}")
            else:
                logging.info("No delete folder requested")
        except Exception as ex:
            logging.error(ex)

    def translate(self, text):
        try:
            if os.getenv("USE_MULTILINGUAL_MODEL", "false").lower() == "true":
                text = f"{self.prepend_code} {text}"

            sentences = text.split("\n")
            translated = []
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                if current_length + len(sentence) <= self.chunk_size:
                    current_chunk.append(sentence)
                    current_length += len(sentence)
                else:
                    tokens = self.tokenizer.encode(" ".join(current_chunk), return_tensors=self.tensor_type, max_length=self.translate_text_length, truncation=True)
                    translated_tokens = self.model.generate(tokens, max_length=self.translate_text_length, num_beams=5, early_stopping=True)
                    translated.append(self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True))
                    current_chunk = [sentence]
                    current_length = len(sentence)

            if current_chunk:
                tokens = self.tokenizer.encode(" ".join(current_chunk), return_tensors=self.tensor_type, max_length=self.translate_text_length, truncation=True)
                translated_tokens = self.model.generate(tokens, max_length=self.translate_text_length, num_beams=5, early_stopping=True)
                translated.append(self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True))

            translating_str = "\n".join(translated)
            return translating_str

        except Exception as ex:
            logging.error(ex)

    def translate_test(self, text):
        try:
            tokens = self.tokenizer.encode(text, return_tensors=self.tensor_type, max_length=self.translate_text_length, truncation=True)
            translated_tokens = self.model.generate(tokens, max_length=self.translate_text_length, num_beams=5, early_stopping=True)
            translating_str = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
            return translating_str
        except Exception as ex:
            logging.error(ex)

    def translate_with_google(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors=self.tensor_type, max_length=512, truncation=True)
            # Generate translation
            outputs = self.model.generate(inputs.input_ids, max_length=512, num_beams=5, early_stopping=True)
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            return translated_text

        except Exception as ex:
            logging.error(ex)

    def get_document_type(self, file_name):
        try:
            endswith = os.path.splitext(file_name)[1]
            if endswith in [".docs", ".doc", ".docx"]:
                return "word"
            elif endswith in [".pdf"]:
                return "pdf"
            elif endswith in [".txt", ".text"]:
                return "txt"
        except Exception as ex:
            logging.error(ex)

    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as ex:
            logging.error(ex)

    @staticmethod
    def is_blank(text):
        if text == "N/A" or text.strip() == "":
            return False
        else:
            return True

    def extract_files_for_translating(self, custom_file_name_prefix=None):
        try:
            input_file_path = os.path.join(self.input_folder, self.file_name)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(f"Input file {input_file_path} not found.")
            # output_file_path = os.path.join(self.output_folder, self.file_name)
            # Step 1: Extract the .docx contents
            if custom_file_name_prefix:
                current_time = datetime.now().strftime("%H_%M_%S")
                self.temp_folder = f"{self.temp_folder}_{custom_file_name_prefix}_{current_time}"

            os.makedirs(self.temp_folder, exist_ok=True)
            with zipfile.ZipFile(input_file_path, 'r') as docx_zip:
                docx_zip.extractall(self.temp_folder)

            # Step 2: Extract plain text data from document.xml
            plain_text_data = []

            document_xml_path = os.path.join(self.temp_folder, self.get_document_type(self.file_name), "document.xml")  # type:ignore
            if os.path.exists(document_xml_path):
                # Parse the document.xml file to extract text
                tree = ET.parse(document_xml_path)
                root = tree.getroot()
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                # Find all text nodes in the XML
                for text_node in root.findall(".//w:t", namespace):
                    if Translator.is_blank(text_node.text):
                        plain_text_data.append({text_node.text.strip(): ""})  # type : ignore  # Add plain text as key with blank value

            # Step 3: Write plain text data to JSON
            json_file = f"{self.temp_folder}/{self.temp_file}.{self.temp_file_extension}"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(plain_text_data, f, indent=4)
            logging.info(f"JSON file with plain text data created: {json_file}")
        except FileNotFoundError as ex:
            logging.error(f"File not found: {ex}")
        except zipfile.BadZipFile as ex:
            logging.error(f"Error extracting ZIP file: {ex}")
        except Exception as ex:
            logging.error(ex)

    def translate_extracted_file(self):
        try:
            if self.google_translator_status == 'True':
                self.initialize_translator_for_google()
            else:
                self.initialize_translator()
            # Read the JSON file
            input_file = f"{self.temp_folder}/{self.temp_file}.{self.temp_file_extension}"
            with open(input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Translate and populate values
            # count = 0
            logging.info("Translating started ...")
            start_time = datetime.now()

            if self.google_translator_status == 'True':
                query = f"Translate {Helper.get_language_name(self.source_lang)} to {Helper.get_language_name(self.target_lang)}: "
                for da in tqdm(data, desc="Translating : ", unit=" Words"):
                    for d in da.items():
                        query_to_pass = f"{query}{d[0]}"
                        da[d[0]] = self.translate_with_google(query_to_pass)
            else:
                for da in tqdm(data, desc="Translating : ", unit=" Words"):
                    for d in da.items():
                        da[d[0]] = self.translate(d[0])
                        # da[d[0]] = self.translate_test(d[0])

            time_difference = datetime.now() - start_time
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            logging.info(f"Time taken: {hours} hours, {minutes} minutes, {seconds} seconds")

            # Write back to the JSON file
            with open(input_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            logging.info("Translation completed offline and updated in the JSON file.")
        except Exception as ex:
            logging.error(ex)

    def generate_translated_file(self, custom_file_name_prefix=None):
        try:
            # Assume JSON file has been updated with translations
            # self.file_name = "test.docx"
            output_file_path = os.path.join(self.output_folder, self.file_name)
            json_file = f"{self.temp_folder}/{self.temp_file}.{self.temp_file_extension}"
            with open(json_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)

            document_xml_path = os.path.join(self.temp_folder, "word", "document.xml")
            if os.path.exists(document_xml_path):
                # Parse the document.xml file to extract text
                tree = ET.parse(document_xml_path)
                root = tree.getroot()
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Step 4: Replace original text in document.xml with translations
            if os.path.exists(document_xml_path):
                for text_node in root.findall(".//w:t", namespace):  # type: ignore
                    original_text = text_node.text.strip()
                    if original_text in [list(item.keys())[0] for item in translations]:
                        # Find the corresponding translation value
                        translation_value = [item[original_text] for item in translations if original_text in item][0]
                        text_node.text = translation_value

                # Write back the updated XML
                tree.write(document_xml_path, encoding='utf-8', xml_declaration=True)  # type: ignore

            # Step 5: Recreate the .docx file from extracted content
            temp_zip = shutil.make_archive(os.path.join(self.output_folder, "temp_docx"), "zip", self.temp_folder)
            formatted_date = datetime.now().strftime("%d_%b_%Y_%H_%M_%S")

            self.output_file_name = f"{self.translated_file_prefix}_From_{Helper.get_language_name(self.source_lang)}_To_{Helper.get_language_name(self.target_lang)}_{formatted_date}_{self.file_name}"

            if custom_file_name_prefix:
                self.output_file_name = f"{custom_file_name_prefix}{self.output_file_name}"

            self.output_file_name_path = os.path.join(self.output_folder, self.output_file_name)
            os.rename(temp_zip, self.output_file_name_path)

            # Clean up temporary files if desired
            shutil.rmtree(self.temp_folder)
            logging.info(f"Recreated .docx file saved as: {output_file_path}")
            return self.output_file_name_path
        except Exception as ex:
            logging.error(ex)

    def process_folder(self):
        try:
            logging.info(f"Processing Folder : {self.input_folder} ...")
            logging.info(f"Full Processing Folder : {os.path.abspath(self.input_folder)} ...")
            if not os.path.exists(self.input_folder):
                raise FileNotFoundError(f"Input folder {self.input_folder} does not exist.")
            if not os.listdir(self.input_folder):
                logging.warning(f"No files found in input folder: {self.input_folder}")
                return
            for self.file_name in os.listdir(self.input_folder):
                logging.debug(f"Processing File {self.file_name}")
                self.extract_files_for_translating()
                self.translate_extracted_file()
                self.generate_translated_file()
            logging.debug("Process folder ends")
            logging.info(f"Chunk Size : {self.chunk_size} and Translation Text Length : {self.translate_text_length}")
        except Exception as ex:
            logging.error(f"Error processing folder: {ex}")

    def custom_execution(self, input_file_name_path, source_lang, target_lang, output_folder=None, custom_file_name_prefix=None):
        try:
            logging.info("Translation Module Invoked...")
            # args = Translator.read_custom_arguement()
            # Translator(args)
            self.input_folder = os.path.dirname(input_file_name_path)
            self.file_name = os.path.basename(input_file_name_path)
            self.source_lang = source_lang
            self.target_lang = target_lang
            self.output_folder = output_folder or self.output_folder

            if not os.path.exists(input_file_name_path):
                raise Exception("File Not Found")

            self.extract_files_for_translating(custom_file_name_prefix)
            self.translate_extracted_file()
            user_output_file_name = self.generate_translated_file(custom_file_name_prefix)

            logging.info("Translation Module Completed")
            return user_output_file_name
        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    try:
        logging.info("Translation Module Invoked...")
        args = Translator.read_arguement()
        translator = Translator(args)
        translator.delete_output_folder()
        translator.process_folder()
        logging.info("Translation Module Completed")
    except Exception as ex:
        logging.error(ex)
