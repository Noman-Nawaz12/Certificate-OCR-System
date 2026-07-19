"""
Utilities for safely saving and validating uploaded files.
"""
import os
import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".pdf"}
MAX_FILE_SIZE_MB = 10

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def is_allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def save_upload(file_bytes: bytes, original_filename: str) -> str:
    """
    Saves uploaded file bytes to disk with a unique name.
    Returns the full path to the saved file.
    """
    ext = os.path.splitext(original_filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name
    with open(save_path, "wb") as f:
        f.write(file_bytes)
    return str(save_path)


def validate_file_size(file_bytes: bytes) -> bool:
    size_mb = len(file_bytes) / (1024 * 1024)
    return size_mb <= MAX_FILE_SIZE_MB
