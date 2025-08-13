import os
import re
import tempfile
import fitz
import docx2txt
import textract
import pyparsing as pp
from fastapi import UploadFile


def extract_text_from_uploaded_file(file: UploadFile) -> str:
    suffix = file.filename.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    try:
        if suffix == "pdf":
            with fitz.open(tmp_path) as doc:
                text = "\n".join([page.get_text() for page in doc])
        elif suffix == "docx":
            text = docx2txt.process(tmp_path)
        elif suffix == "doc":
            text = textract.process(tmp_path).decode("utf-8")
        elif suffix == "txt":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file format.")
    finally:
        os.unlink(tmp_path)
    return text


def extract_text_from_pdf(file):
    text = ""
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf_doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def get_text(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    else:
        text = None
    return text