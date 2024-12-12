import chardet
from pygments.lexers import guess_lexer
from docx import Document


def detect_language(file_path):
    # Check if the file is a .docx
    if file_path.endswith('.docx'):
        # Extract text from .docx
        document = Document(file_path)
        content = "\n".join([p.text for p in document.paragraphs])
    else:
        # Detect encoding for text-based files
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']

        # Read file content
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()

    # Guess language
    lexer = guess_lexer(content)
    return lexer.name


# Example usage
file_path = "/home/kb/github/original/mes_copilot_mvp/Translator/Output_Folder_Translated/Translated_To_fr_Krishna.docx"
language = detect_language(file_path)
print(f"The detected language is: {language}")
