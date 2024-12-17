import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas

def pdfminer_5():
    # Paths to input XML and output PDF
    xml_path = "output.xml"
    pdf_path = "recreated.pdf"

    # Parse the XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a PDF using ReportLab
    c = canvas.Canvas(pdf_path)

    # Extract and add content to the PDF
    for page in root.findall("page"):
        for text_box in page.findall("textbox"):
            for text_line in text_box.findall("textline"):
                for text in text_line.findall("text"):
                    # Get the content and position (if available)
                    content = text.text.strip() if text.text else ""
                    x = float(text.get("x", 100))  # Default x position
                    y = float(text.get("y", 800))  # Default y position
                    
                    # Add text to the PDF (y-axis needs adjustment as PDF coordinates are bottom-up)
                    c.drawString(x, 842 - y, content)  # Adjust height for standard A4

        c.showPage()  # Add a new page for each XML page element

    # Save the recreated PDF
    c.save()

    print(f"PDF recreated and saved as {pdf_path}")
