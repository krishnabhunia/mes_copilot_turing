import fitz  # PyMuPDF
import os

def pdf_to_xml(input_pdf, output_xml):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)
    
    # Prepare XML file
    with open(output_xml, "w", encoding="utf-8") as xml_file:
        xml_file.write("<document>\n")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text_xml = page.get_text("xml")
            xml_file.write(f"<page number='{page_num + 1}'>\n{text_xml}\n</page>\n")
        
        xml_file.write("</document>")
    
    print(f"XML file '{output_xml}' created successfully.")

def xml_to_pdf(input_xml, output_pdf):
    # Create a new PDF document
    pdf_document = fitz.open()
    
    # Read the XML content
    with open(input_xml, "r", encoding="utf-8") as file:
        xml_content = file.read()
    
    # Parse XML and recreate PDF pages
    pdf_document.insert_page(-1, text=xml_content)
    
    # Save the regenerated PDF
    pdf_document.save(output_pdf)
    print(f"PDF file '{output_pdf}' regenerated successfully.")

# Example Usage
input_pdf_path = "input.pdf"
output_xml_path = "output.xml"
regenerated_pdf_path = "regenerated.pdf"

# Convert PDF to XML
pdf_to_xml(input_pdf_path, output_xml_path)

# Regenerate PDF from XML
xml_to_pdf(output_xml_path, regenerated_pdf_path)
