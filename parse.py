import PyPDF2
from io import BytesIO
from pdfminer.high_level import extract_text

async def parse_pdf(file):
    # Read the file into a BytesIO object
    pdf_file = await file.read()
    pdf_file_io = BytesIO(pdf_file)

    try:
        # Try using PyPDF2 first
        pdf = PyPDF2.PdfReader(pdf_file_io)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    except Exception as e:
        # If PyPDF2 fails, fall back to pdfminer.six
        print(f"PyPDF2 failed with exception: {e}. Trying pdfminer.six.")
        pdf_file_io.seek(0)  # Reset the BytesIO object to the beginning
        text = extract_text(pdf_file_io)

    return text
