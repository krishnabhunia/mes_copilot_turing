from xml.etree import ElementTree as ET
from docx import Document

# Load XML
xml_file = "output.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Create a Word document
doc = Document()

# Parse and add content
for page in root.findall(".//page"):
    for text in page.findall(".//text"):
        content = text.text
        if content:
            doc.add_paragraph(content)

# Save the DOCX
doc.save("output.docx")
