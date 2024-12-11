from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import xml.etree.ElementTree as ET

# Register the custom font with the correct path
pdfmetrics.registerFont(TTFont("Helvetica", "fonts/Helvetica.ttf"))

def xml_to_pdf_with_formatting(xml_path, pdf_output_path):
    """Recreate PDF from XML with font formatting and positions."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    c = canvas.Canvas(pdf_output_path)
    
    for page in root.findall("Page"):
        for text in page.findall("Text"):
            content = text.text
            font = text.get("font", "Helvetica")
            size = float(text.get("size", 12))
            bbox = eval(text.get("bbox", "(0, 0, 0, 0)"))
            color = int(text.get("color", 0))  # Convert color to RGB int

            # Register and fallback for missing fonts
            try:
                c.setFont(font, size)
            except KeyError:
                print(f"Font '{font}' not found. Falling back to 'Helvetica'.")
                c.setFont("Helvetica", size)

            # Set text color
            r, g, b = ((color >> 16) & 255) / 255.0, ((color >> 8) & 255) / 255.0, (color & 255) / 255.0
            c.setFillColor(Color(r, g, b))

            # Draw text at the specified position
            x, y, _, _ = bbox
            c.drawString(x, y, content)

        c.showPage()  # End current page and start a new one

    c.save()
    print(f"PDF recreated: {pdf_output_path}")
