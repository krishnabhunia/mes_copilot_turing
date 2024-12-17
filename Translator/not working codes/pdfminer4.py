from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from io import BytesIO

def pdfminer_4():
    # Path to the PDF file
    pdf_path = "sample.pdf"

    # Extract PDF to XML
    output = BytesIO()  # Buffer to store XML content
    with open(pdf_path, "rb") as f:
        # Resource manager and parameters for analysis
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = XMLConverter(rsrcmgr, output, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        # Process each page
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
        
        # Close the device
        device.close()

    # Save the XML output to a file
    xml_output_path = "output.xml"
    with open(xml_output_path, "wb") as xml_file:
        xml_file.write(output.getvalue())
        print("XML File Generated")

    output.close()
