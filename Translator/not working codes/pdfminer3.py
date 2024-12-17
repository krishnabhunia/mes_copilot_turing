from PyPDF2 import PdfReader
from docx import Document

reader = PdfReader("sample.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

print(text)

# Create a Word document
doc = Document()

# Add the extracted text to the document
doc.add_paragraph(text)

# Save the document as a .docx file
doc.save("output.docx")
