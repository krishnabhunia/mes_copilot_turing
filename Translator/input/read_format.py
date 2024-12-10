import zipfile
import os
import json
from xml.etree import ElementTree as ET

# Paths
input_docx = "input/Krishna.docx"  # Input file
temp_folder = "temp_folder"  # Temp folder for extracted content
output_docx = "re_created.docx"  # Final recreated file
json_file = "output.json"  # JSON file to store plain text data

# Step 1: Extract the .docx contents
os.makedirs(temp_folder, exist_ok=True)
with zipfile.ZipFile(input_docx, 'r') as docx_zip:
    docx_zip.extractall(temp_folder)

# Step 2: Extract plain text data from document.xml
plain_text_data = []

document_xml_path = os.path.join(temp_folder, "word", "document.xml")
if os.path.exists(document_xml_path):
    # Parse the document.xml file to extract text
    tree = ET.parse(document_xml_path)
    root = tree.getroot()
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Find all text nodes in the XML
    for text_node in root.findall(".//w:t", namespace):
        plain_text_data.append({text_node.text: ""})  # Add plain text as key with blank value

# Step 3: Write plain text data to JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(plain_text_data, f, indent=4)

print(f"JSON file with plain text data created: {json_file}")
