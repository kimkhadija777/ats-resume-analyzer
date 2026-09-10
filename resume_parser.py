from io import BytesIO

import docx
import pdfplumber


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""

    text_parts = []

    with pdfplumber.open(
        BytesIO(file_bytes)
    ) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def extract_docx_text(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""

    document = docx.Document(
        BytesIO(file_bytes)
    )

    text_parts = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            text_parts.append(text)

    return "\n".join(text_parts).strip()


def extract_resume_text(uploaded_file) -> str:
    """
    Extract resume text based on file extension.
    """

    file_name = uploaded_file.name.lower()

    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".pdf"):

        return extract_pdf_text(file_bytes)

    if file_name.endswith(".docx"):

        return extract_docx_text(file_bytes)

    raise ValueError(
        "Unsupported file type. "
        "Please upload a PDF or DOCX file."
    )
