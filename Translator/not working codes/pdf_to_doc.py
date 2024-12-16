from PyPDF2 import PdfReader
from docx import Document

pdf_file = "input_pdf/English_PDF.pdf"
docx_file = "output.docx"

reader = PdfReader(pdf_file)
doc = Document()

for page in reader.pages:
    doc.add_paragraph(page.extract_text())

doc.save(docx_file)
