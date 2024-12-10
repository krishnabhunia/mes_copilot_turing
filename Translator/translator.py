import os
import shutil
from dotenv import load_dotenv
from transformers import MarianMTModel, MarianTokenizer  # type: ignore
import zipfile
import json
from xml.etree import ElementTree as ET

# Suppress TensorFlow logs and CUDA initialization
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Only errors
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN optimizations
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU usage completely


load_dotenv()


class Translator:
    def __init__(self) -> None:
        self.input_folder = os.getenv("INPUT_FOLDER_TO_BE_TRANSLATED") or "Input"
        self.output_folder = os.getenv("OUTPUT_FOLDER_TRANSLATED") or "Output"
        self.temp_folder = os.getenv("TEMPORARY_TRANSLATION_FOLDER") or "Temporary"
        self.temp_file = os.getenv("TEMPORARY_TRANSLATION_FILE") or "Temporary_File"
        self.translate_text_length = os.getenv("TRANSLATION_TEXT_LENGTH")
        self.model_name = 'Helsinki-NLP/opus-mt-en-fr'
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def delete_output_folder(self):
        if os.path.exists(self.output_folder):  # type : ignore
            print("Path exists , deleting folder ...")
            shutil.rmtree(self.output_folder)
            print(f"Folder deleted {self.output_folder}")
        else:
            print(f"Folder deoesn't exists : {self.output_folder}")

    def translate_text(self, text, chunk_size=512, translate_lang='pt'):
        sentences = text.split("\n")
        translated = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) <= chunk_size:
                current_chunk.append(sentence)
                current_length += len(sentence)
            else:
                tokens = self.tokenizer.encode(" ".join(current_chunk), return_tensors=translate_lang, max_length=self.translate_text_length, truncation=True)
                translated_tokens = self.model.generate(tokens, max_length=self.translate_text_length, num_beams=5, early_stopping=True)
                translated.append(self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True))
                current_chunk = [sentence]
                current_length = len(sentence)

        if current_chunk:
            tokens = self.tokenizer.encode(" ".join(current_chunk), return_tensors=translate_lang, max_length=self.translate_text_length, truncation=True)
            translated_tokens = self.model.generate(tokens, max_length=self.translate_text_length, num_beams=5, early_stopping=True)
            translated.append(self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True))

        return "\n".join(translated)

    def get_document_type(self, file_name):
        endswith = os.path.splitext(file_name)[1]
        if endswith in ["docs", "doc", "docx"]:
            return "word"
        elif endswith in ["pdf"]:
            return "pdf"

    def process_folder(self):
        for file_name in os.listdir(self.input_folder):
            input_file_path = os.path.join(self.input_folder, file_name)
            output_file_path = os.path.join(self.output_folder, file_name)

            # Step 1: Extract the .docx contents
            os.makedirs(self.temp_folder, exist_ok=True)
            with zipfile.ZipFile(input_file_path, 'r') as docx_zip:
                docx_zip.extractall(self.temp_folder)

            # Step 2: Extract plain text data from document.xml
            plain_text_data = []

            document_xml_path = os.path.join(self.temp_folder, self.get_document_type(file_name), "document.xml")  # type:ignore
            if os.path.exists(document_xml_path):
                # Parse the document.xml file to extract text
                tree = ET.parse(document_xml_path)
                root = tree.getroot()
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                # Find all text nodes in the XML
                for text_node in root.findall(".//w:t", namespace):
                    plain_text_data.append({text_node.text: ""})  # Add plain text as key with blank value

            # Step 3: Write plain text data to JSON
            json_file = f"{self.temp_folder}/{self.temp_file}"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(plain_text_data, f, indent=4)

            print(f"JSON file with plain text data created: {json_file}")


if __name__ == "__main__":
    translator = Translator()
    translator.delete_output_folder()
    translator.process_folder()
