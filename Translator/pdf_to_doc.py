from pdf2docx import Converter


try:
    # Convert PDF to DOCX
    pdf_file = "input_pdf/English_PDF.pdf"
    docx_file = "output.docx"

    converter = Converter(pdf_file)
    converter.convert(docx_file)
    converter.close()
except Exception as ex:
    print(ex)
