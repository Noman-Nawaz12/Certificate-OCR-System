"""
API route definitions for the Certificate OCR system.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.core.ocr_engine import extract_text
from app.core.extractor import extract_all_fields
from app.utils.file_handler import is_allowed_file, save_upload, validate_file_size

router = APIRouter()

# In-memory store of results (swap for a real database in Phase 4)
RESULTS_STORE = {}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/extract")
async def extract_certificate(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    file_bytes = await file.read()

    if not validate_file_size(file_bytes):
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")

    saved_path = save_upload(file_bytes, file.filename)

    try:
        raw_text = extract_text(saved_path)
        fields = extract_all_fields(raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")

    result_id = str(uuid.uuid4())
    RESULTS_STORE[result_id] = fields

    return JSONResponse(content={"id": result_id, **fields})


@router.get("/results/{result_id}")
def get_result(result_id: str):
    result = RESULTS_STORE.get(result_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found.")
    return result


@router.delete("/documents/{result_id}")
def delete_result(result_id: str):
    if result_id not in RESULTS_STORE:
        raise HTTPException(status_code=404, detail="Result not found.")
    del RESULTS_STORE[result_id]
    return {"status": "deleted"}
