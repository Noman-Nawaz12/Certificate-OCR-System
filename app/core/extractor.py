"""
Extracts structured fields (name, certificate title, date, etc.)
from raw OCR text using pattern matching.

This is intentionally rule-based and simple — a great place for you
to improve accuracy as you learn more about the certificate formats
you're testing against.
"""
import re
from typing import Optional, Dict


DATE_PATTERN = re.compile(
    r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}|"
    r"(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{1,2},?\s+\d{4})\b",
    re.IGNORECASE
)

CERT_ID_PATTERN = re.compile(
    r"\b(?:certificate\s*(?:id|no|number)?\s*[:#]?\s*)([A-Z0-9\-]{4,20})\b",
    re.IGNORECASE
)

GRADE_PATTERN = re.compile(
    r"\b(?:grade|score)\s*[:\-]?\s*([A-Za-z0-9\+\-\.]{1,10})\b",
    re.IGNORECASE
)

NAME_LINE_PATTERN = re.compile(
    r"(?:this\s+is\s+to\s+certify\s+that|certifies\s+that|awarded\s+to|presented\s+to)\s*[:\-]?\s*([A-Z][a-zA-Z\.\s]{2,50})",
    re.IGNORECASE
)

ORG_KEYWORDS = [
    "university", "institute", "college", "academy", "school",
    "corporation", "company", "ltd", "inc", "association", "foundation"
]


def _find_first(pattern: re.Pattern, text: str) -> Optional[str]:
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def extract_candidate_name(text: str) -> Optional[str]:
    name = _find_first(NAME_LINE_PATTERN, text)
    if name:
        # Trim trailing junk / newlines
        name = name.split("\n")[0].strip()
    return name


def extract_organization(text: str) -> Optional[str]:
    for line in text.split("\n"):
        lower = line.lower()
        if any(keyword in lower for keyword in ORG_KEYWORDS):
            return line.strip()
    return None


def extract_certificate_title(text: str) -> Optional[str]:
    """
    Looks for a line following common phrases like 'has completed' or
    'for successfully completing', which usually precedes the course/title.
    """
    match = re.search(
        r"(?:completed|completing|completion of)\s+(?:the\s+)?([A-Za-z0-9 ,\-]{3,80})",
        text, re.IGNORECASE
    )
    if match:
        return match.group(1).split("\n")[0].strip()
    return None


def extract_all_fields(text: str) -> Dict[str, Optional[str]]:
    """
    Runs all extraction functions and returns a structured dictionary
    of fields found in the OCR text.
    """
    return {
        "candidate_name": extract_candidate_name(text),
        "certificate_title": extract_certificate_title(text),
        "organization_name": extract_organization(text),
        "issue_date": _find_first(DATE_PATTERN, text),
        "certificate_number": _find_first(CERT_ID_PATTERN, text),
        "grade_score": _find_first(GRADE_PATTERN, text),
        "raw_text": text,
    }
