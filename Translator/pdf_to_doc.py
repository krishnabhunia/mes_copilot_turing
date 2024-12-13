from pdf2docx import Converter

# Convert PDF to DOCX
pdf_file = "example.pdf"
docx_file = "output.docx"

converter = Converter(pdf_file)
converter.convert(docx_file)
converter.close()
