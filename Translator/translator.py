import os
import shutil
from dotenv import load_dotenv
from transformers import MarianMTModel, MarianTokenizer  # type: ignore
import zipfile
import json
from PyPDF2 import PdfReader
from xml.etree import ElementTree as ET
import Helper
from tqdm import tqdm
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
    def __init__(self) -> None:
        try:
            logging.info("Initializing ...")
            args = Translator.read_arguement()

            self.input_folder = args.input_folder or os.getenv("INPUT_FOLDER_TO_BE_TRANSLATED") or "Input"
            self.output_folder = args.output_folder or os.getenv("OUTPUT_FOLDER_TRANSLATED") or "Output"
            self.temp_folder = os.getenv("TEMPORARY_TRANSLATION_FOLDER") or "Temporary"
            self.temp_file = os.getenv("TEMPORARY_TRANSLATION_FILE") or "Temporary_File"
            self.translate_text_length = int(os.getenv("TRANSLATION_TEXT_LENGTH")) or 512  # type: ignore
            self.translated_file_prefix = os.getenv("TRANSLATED_FILE_PREFIX") or "Translated"
            self.temp_file_extension = "json"
            self.temp_xml_document = "document.xml"
            self.chunk_size = int(os.getenv("CHUNK_SIZE")) or 512  # type: ignore
            self.source_lang = args.source_lang or os.getenv("DEFAULT_SOURCE_LANG") or "en"
            self.target_lang = args.target_lang or os.getenv("DEFAULT_TARGET_LANG") or "fr"
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

            # Parse arguments
            args = parser.parse_args()
            return args
        except Exception as ex:
            logging.error(ex)

    def initialize_translator(self):
        try:
            logging.info("Initializing Translator ...")
            base_name = os.getenv("TRANSFORMER_BASE_MODEL_NAME") or "Helsinki-NLP"
            translation_type = os.getenv("TRANSLATION_TYPE") or "opus-mt"
            self.tensor_type = Translator.get_tensor(os.getenv("TENSOR_TYPE")) or Translator.get_tensor("pytorch")
            self.model_name = f"{base_name}/{translation_type}-{self.source_lang}-{self.target_lang}"
            logging.info(f"Translator Name : {self.model_name}")
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = MarianMTModel.from_pretrained(self.model_name)
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
        except Exception as ex:
            logging.error(ex)

    def translate(self, text):
        try:
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

            return "\n".join(translated)
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

    def extract_files_for_translating(self):
        try:
            input_file_path = os.path.join(self.input_folder, self.file_name)
            if not os.path.exists(input_file_path):
                raise FileNotFoundError(f"Input file {input_file_path} not found.")
            # output_file_path = os.path.join(self.output_folder, self.file_name)
            # Step 1: Extract the .docx contents
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
                    plain_text_data.append({text_node.text: ""})  # type : ignore  # Add plain text as key with blank value

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
            self.initialize_translator()
            # Read the JSON file
            input_file = f"{self.temp_folder}/{self.temp_file}.{self.temp_file_extension}"
            with open(input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Translate and populate values
            # count = 0
            logging.info("Translating started ...")
            start_time = datetime.now()
            for da in tqdm(data, desc="Translating : ", unit=" Words"):
                for d in da.items():
                    da[d[0]] = self.translate(d[0])
                # count += 1
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

    def generate_translated_file(self):
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
                    original_text = text_node.text
                    if original_text in [list(item.keys())[0] for item in translations]:
                        # Find the corresponding translation value
                        translation_value = [item[original_text] for item in translations if original_text in item][0]
                        text_node.text = translation_value

                # Write back the updated XML
                tree.write(document_xml_path, encoding='utf-8', xml_declaration=True)  # type: ignore

            # Step 5: Recreate the .docx file from extracted content
            temp_zip = shutil.make_archive(os.path.join(self.output_folder, "temp_docx"), "zip", self.temp_folder)
            formatted_date = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            os.rename(temp_zip, os.path.join(self.output_folder, f"{self.translated_file_prefix}_From_{Helper.get_language_name(self.source_lang)}_To_{Helper.get_language_name(self.target_lang)}_{formatted_date}_{self.file_name}"))

            # Clean up temporary files if desired
            shutil.rmtree(self.temp_folder)
            logging.info(f"Recreated .docx file saved as: {output_file_path}")
        except Exception as ex:
            logging.error(ex)

    def process_folder(self):
        try:
            logging.debug("Processing Folder ...")
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
        except Exception as ex:
            logging.error(f"Error processing folder: {ex}")


if __name__ == "__main__":
    try:
        logging.info("Translation Module Invoked...")
        translator = Translator()
        translator.delete_output_folder()
        translator.process_folder()
        logging.info("Translation Module Completed")
    except Exception as ex:
        logging.error(ex)
