import os
import shutil
import sys
from dotenv import load_dotenv
from transformers import MarianMTModel, MarianTokenizer  # type: ignore

load_dotenv()

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Suppress TensorFlow and system-level logs
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress TensorFlow logs (Error only)
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Disable oneDNN optimizations
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable CUDA if not using GPU

# Redirect stderr to suppress logs written to STDERR
# sys.stderr = open(os.devnull, "w")

class Translator:
    def __init__(self) -> None:
        self.output_folder = os.getenv("OUTPUT_FOLDER_TRANSLATED") or ""
        self.model_name = 'Helsinki-NLP/opus-mt-en-fr'
        # self.model_name = 'google-t5/t5-small'
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def delete_output_folder(self):
        if os.path and os.path.exists(self.output_folder):  # type : ignore
            # print('Folder existed, so deleting ...')
            shutil.rmtree(self.output_folder)
            # print('Folder deleted:', self.output_folder)


if __name__ == "__main__":
    translator = Translator()
    translator.delete_output_folder()
