import fitz  # PyMuPDF
import xml.etree.ElementTree as ET


def pdf_to_xml_with_formatting(pdf_path, xml_output_path):
    """Convert PDF to XML with font formatting and positions."""
    doc = fitz.open(pdf_path)
    root = ET.Element("PDFDocument")

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_element = ET.SubElement(root, "Page", attrib={"number": str(page_num + 1)})
        for text in page.get_text("dict")["blocks"]:   # type: ignore
            for line in text["lines"]:
                for span in line["spans"]:
                    # Extract text, font, and size
                    text_element = ET.SubElement(page_element, "Text", attrib={
                        "font": span["font"],
                        "size": str(span["size"]),
                        "bbox": str(span["bbox"]),
                        "color": str(span["color"])
                    })
                    text_element.text = span["text"]

    # Write the XML to a file
    tree = ET.ElementTree(root)
    tree.write(xml_output_path, encoding="utf-8", xml_declaration=True)
    print(f"XML file created: {xml_output_path}")


# Example Usage
pdf_path = "input/Krishna_PDF.pdf"  # Path to your PDF file
xml_output_path = "output.xml"  # Path to save the XML file
pdf_to_xml_with_formatting(pdf_path, xml_output_path)
