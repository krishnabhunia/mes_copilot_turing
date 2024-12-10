import shutil
import os
import json
from xml.etree import ElementTree as ET

# Paths
temp_folder = "temp_folder"  # Temp folder for extracted content
output_docx = "re_created.docx"  # Final recreated file
json_file = "output.json"  # JSON file to store plain text data

# Assume JSON file has been updated with translations
with open(json_file, 'r', encoding='utf-8') as f:
    translations = json.load(f)

document_xml_path = os.path.join(temp_folder, "word", "document.xml")
if os.path.exists(document_xml_path):
    # Parse the document.xml file to extract text
    tree = ET.parse(document_xml_path)
    root = tree.getroot()
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Step 4: Replace original text in document.xml with translations
if os.path.exists(document_xml_path):
    for text_node in root.findall(".//w:t", namespace):  # type: ignore
        original_text = text_node.text
        if original_text in [list(item.keys())[0] for item in translations]:
            # Find the corresponding translation value
            translation_value = [
                item[original_text]
                for item in translations
                if original_text in item
            ][0]
            text_node.text = translation_value

    # Write back the updated XML
    tree.write(document_xml_path, encoding='utf-8', xml_declaration=True)  # type: ignore

# Step 5: Recreate the .docx file from extracted content
temp_zip = shutil.make_archive("temp_docx", "zip", temp_folder)
os.rename(temp_zip, output_docx)

# Clean up temporary files if desired
shutil.rmtree(temp_folder)
print(f"Recreated .docx file saved as: {output_docx}")
