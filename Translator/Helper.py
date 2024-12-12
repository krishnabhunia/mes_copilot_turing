import os


@staticmethod  # type: ignore[misc]
def language_mapper():
    language_map = {
        'zh': ['chinese'],
        'en': ['english', 'eng'],
        'es': ['spanish'],
        'fr': ['french'],
        'de': ['german'],
        'nl': ['hollander', 'dutch'],
        'it': ['italian'],
        'hu': ['magyar', 'hungarian'],
        'pt': ['portuguese'],
        'fi': ['suomi', 'finnish'],
        'sv': ['svenska', 'swedish']
    }
    return language_map


@staticmethod  # type: ignore[misc]
def get_language_name(inp_lang):
    language_map = language_mapper()
    inp_lang_lower = inp_lang.lower()
    for code, names in language_map.items():
        if inp_lang_lower in code:
            return names[0].title()
    else:
        raise ValueError(f"Unsupported language: {inp_lang}")


@staticmethod  # type: ignore[misc]
def get_language_code(inp_lang):
    language_map = language_mapper()
    inp_lang_lower = inp_lang.lower()
    for code, names in language_map.items():
        if inp_lang_lower in names:
            return code
    else:
        raise ValueError(f"Unsupported language: {inp_lang}")

# @staticmethod
# def get_document_type(self, file_name):
#     endswith = os.path.splitext(file_name)[1]
#     if endswith in [".docs", ".doc", ".docx"]:
#         return "word"
#     elif endswith in [".pdf"]:
#         return "pdf"
#     elif endswith in [".txt", ".text"]:
#         return "txt"


@staticmethod  # type: ignore[misc]
def file_mapper():
    file_type_map = {
        "word": [".docs", ".doc", ".docx"],
        "pdf": [".pdf"],
        "txt": [".txt", ".text"]
    }
    return file_type_map


@staticmethod  # type: ignore[misc]
def get_document_type(file_name):
    file_type_map = file_mapper()
    endswith = os.path.splitext(file_name)[1].lower()
    for doc_type, extensions in file_type_map.items():
        if endswith in extensions:
            return doc_type
    else:
        raise ValueError(f"Unsupported file type: {endswith}")