from pdfminer.high_level import extract_text
from docx import Document

# Path to your PDF file
pdf_path = "sample.pdf"

# Extract text from PDF
text = extract_text(pdf_path)

# Create a Word document
doc = Document()

# Add the extracted text to the document
doc.add_paragraph(text)

# Save the document as a .docx file
doc.save("output.docx")
