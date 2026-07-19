# Certificate OCR System

A web application that automatically extracts structured information (candidate name,
certificate title, organization, issue date, certificate number, grade) from certificate
images or PDFs using Tesseract OCR.

## Features

- Drag-and-drop upload for images (JPG, PNG, TIFF, BMP) and PDFs
- Image preprocessing pipeline (grayscale, adaptive thresholding, denoising, deskewing)
  to improve OCR accuracy
- Automatic field extraction from raw OCR text
- Clean web UI showing results in a table, with copy-to-clipboard JSON
- REST API for programmatic access
- Basic test suite (pytest)

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **OCR:** Tesseract (via pytesseract)
- **Image processing:** OpenCV
- **PDF handling:** pdf2image + Poppler
- **Frontend:** Plain HTML/CSS/JavaScript

## Prerequisites (install these first)

1. **Python 3.11+** — https://www.python.org/downloads/
   - On Windows, check "Add python.exe to PATH" during install.
2. **Tesseract OCR** (separate program, not a Python package)
   - Windows: install from the UB-Mannheim Tesseract build
   - Mac: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`
3. **Poppler** (only needed for PDF support)
   - Windows: download "Poppler for Windows", unzip, add its `bin` folder to PATH
   - Mac: `brew install poppler`
   - Linux: `sudo apt install poppler-utils`
4. **Git** — https://git-scm.com/

## Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd certificate-ocr-system

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Windows note: pointing to Tesseract

If `pytesseract` can't find Tesseract automatically, add this near the top of
`app/core/ocr_engine.py`:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Running the app

```bash
uvicorn main:app --reload
```

Then open http://localhost:8000 in your browser.

## Running tests

```bash
python -m pytest tests/
```

## API Endpoints

| Method | Endpoint             | Description                  |
|--------|-----------------------|-------------------------------|
| GET    | `/`                   | Web interface                |
| GET    | `/health`             | Health check                 |
| POST   | `/extract`            | Upload a file, get extracted fields |
| GET    | `/results/{id}`       | Retrieve a previous result    |
| DELETE | `/documents/{id}`     | Delete a stored result        |

### Example usage

```python
import requests

files = {"file": open("certificate.pdf", "rb")}
response = requests.post("http://localhost:8000/extract", files=files)
data = response.json()
print(data["candidate_name"], data["certificate_title"])
```

## Project Structure

```
certificate-ocr-system/
├── app/
│   ├── api/routes.py         # API endpoints
│   ├── core/
│   │   ├── ocr_engine.py     # Tesseract OCR wrapper
│   │   ├── preprocessor.py   # Image cleanup pipeline
│   │   └── extractor.py      # Field extraction logic
│   └── utils/file_handler.py # Upload validation/saving
├── static/                   # CSS & JS
├── templates/index.html      # Web UI
├── tests/                    # Pytest test suite
├── uploads/                  # Uploaded files (gitignored)
├── main.py                   # App entry point
├── requirements.txt
└── README.md
```

## Known Limitations / Next Steps

- Field extraction uses rule-based pattern matching — accuracy depends on
  certificate layout. Improving this with more patterns or an NER model is
  a natural next step.
- Results are stored in memory; restart the server and they're gone.
  Add SQLite/PostgreSQL for persistence (see Phase 4 in the internship brief).
- No authentication — add this before any real deployment.

## License

Built for the Teerop Pvt. Limited Gen AI & LLM Applications Internship Program.
