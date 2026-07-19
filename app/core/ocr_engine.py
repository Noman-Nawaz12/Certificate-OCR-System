"""
Wrapper around Tesseract OCR (via pytesseract) for extracting text
from images and PDFs.
"""
import os
import tempfile
from typing import List

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from app.core.preprocessor import preprocess_image


def extract_text_from_image(image_path: str, use_preprocessing: bool = True) -> str:
    """Run OCR on a single image file and return the raw extracted text."""
    if use_preprocessing:
        processed = preprocess_image(image_path)
        pil_image = Image.fromarray(processed)
    else:
        pil_image = Image.open(image_path)

    text = pytesseract.image_to_string(pil_image)
    print(text)
    return text.strip()


def extract_text_from_pdf(pdf_path: str, use_preprocessing: bool = True) -> str:
    """
    Convert each page of a PDF to an image, run OCR on each page,
    and combine the results.
    """
    pages = convert_from_path(pdf_path)
    all_text: List[str] = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        for i, page in enumerate(pages):
            page_path = os.path.join(tmp_dir, f"page_{i}.png")
            page.save(page_path, "PNG")
            page_text = extract_text_from_image(page_path, use_preprocessing)
            all_text.append(page_text)

    return "\n\n".join(all_text).strip()


def extract_text(file_path: str, use_preprocessing: bool = True) -> str:
    """
    Auto-detect file type (image vs PDF) and extract text accordingly.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path, use_preprocessing)
    elif ext in (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"):
        return extract_text_from_image(file_path, use_preprocessing)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
