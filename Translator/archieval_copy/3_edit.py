import fitz  # type: ignore # PyMuPDF


def edit_pdf_text_with_format(input_pdf, output_pdf, old_text, new_text, font_path="path/to/font.ttf"):
    """Edit a PDF file by replacing text while keeping the formatting intact."""
    doc = fitz.open(input_pdf)

    for page in doc:
        areas = page.search_for(old_text)  # Find text locations
        for area in areas:
            # Redact old text and insert new text with font from a file
            page.add_redact_annot(area, fill=(1, 1, 1))  # White background
            page.apply_redactions()

            # Insert new text with a specified font file
            page.insert_text(
                area.tl,  # Insert at the top-left of the redacted area
                new_text,
                fontsize=12,  # Set an appropriate font size
                fontfile=font_path,  # Use the specified font file
                color=(0, 0, 0),  # Black color
            )

    doc.save(output_pdf)
    print(f"Edited PDF saved as: {output_pdf}")


# Example Usage
input_pdf = "example.pdf"  # Input PDF file path
output_pdf = "edited_example.pdf"  # Output PDF file path
font_path = "path/to/font.ttf"  # Path to your custom TTF font file
edit_pdf_text_with_format(input_pdf, output_pdf, "I am Krishna", "new_text", font_path)
