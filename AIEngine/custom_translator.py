# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("translation", model="Lalita/marianmt-th-zh_cn")

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Lalita/marianmt-th-zh_cn")
model = AutoModelForSeq2SeqLM.from_pretrained("Lalita/marianmt-th-zh_cn")