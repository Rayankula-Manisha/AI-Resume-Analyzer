
import pdfplumber


def extract_resume_text(uploaded_file):
    """Extract readable text from an uploaded PDF resume."""

    extracted_pages = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()
