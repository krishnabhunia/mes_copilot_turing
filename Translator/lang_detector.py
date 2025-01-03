from langdetect import detect  # type: ignore
from docx import Document  # type: ignore
import Helper
import sys
import logging
from pathlib import Path
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def detect_language(file_path):
    # Check if the file is a .docx
    if file_path.endswith('.docx'):
        # Extract text from .docx
        document = Document(file_path)
        content = "\n".join([p.text for p in document.paragraphs])
    else:
        # Read text-based files
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

    # Detect the natural language
    language_code = detect(content)

    # Map language code to language names
    language_map = Helper.language_mapper()

    # Get the primary language name
    logging.info(f"Detected language code: {language_code}")
    language = language_map.get(language_code, ["Unknown"])[0]
    logging.info(f"The detected language is: {language}")
    return language_code, language


def detect_file_language():
    if sys.argv[1]:
        file_path = sys.argv[1]
    else:
        file_path = str(Path("inp fr/French.docx"))
    language_tuple = detect_language(file_path)
    logging.info(f"The detected language is: {language_tuple}")
    return language_tuple


if __name__ == "__main__":
    detect_file_language()

