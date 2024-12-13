from langdetect import detect
from docx import Document
import Helper


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
    return language_map.get(language_code, ["Unknown"])[0]


# Example usage
file_path = "Output_Folder_Translated/Translated_From_French_To_English_French.docx"
language = detect_language(file_path)
print(f"The detected language is: {language}")