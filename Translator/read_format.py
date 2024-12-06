import zipfile
import os
import shutil
import json

# Paths
input_docx = "input/Krishna.docx"  # Input file
temp_folder = "temp_folder"  # Temp folder for extracted content
output_folder = 'translated_document/'
output_docx = "re_created.docx"  # Final recreated file
json_file = "output.json"  # JSON file to store data

# Step 1: Extract the .docx contents
os.makedirs(temp_folder, exist_ok=True)
with zipfile.ZipFile(input_docx, 'r') as docx_zip:
    docx_zip.extractall(temp_folder)

# Step 2: Create a JSON file with keys as data and blank values
docx_data = []

for root, dirs, files in os.walk(temp_folder):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read file content and add as key
            content = f.read().strip()
            docx_data.append({content: ""})  # Store content as key with blank value

# Write to a JSON file
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(docx_data, f, indent=4)

print(f"JSON file with extracted data created: {json_file}")

# Step 3: Recreate the .docx file from extracted content
temp_zip = shutil.make_archive("temp_docx", "zip", temp_folder)
os.rename(temp_zip, output_docx)

# Clean up temporary files if desired
shutil.rmtree(temp_folder)
print(f"Recreated .docx file saved as: {output_docx}")
