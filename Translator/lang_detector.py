from langdetect import detect
from docx import Document


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
    # Map language code to language name
    language_map = {
        'en': 'English',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'zh': 'Chinese',
        'hi': 'Hindi',
        # Add more mappings as needed
    }
    return language_map.get(language_code, "Unknown")


# Example usage
file_path = "Output_Folder_Translated/Translated_From_French_To_English_French.docx"
file_path = "Input_Folder_To_Be_Translated/Hindi.docx"
language = detect_language(file_path)
print(f"The detected language is: {language}")
