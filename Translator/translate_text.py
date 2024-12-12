import translator
import sys

try:
    trans = translator.Translator()
    trans.initialize_translator()
    print(trans.translate(sys.argv[1]))
except Exception as ex:
    print(ex)
