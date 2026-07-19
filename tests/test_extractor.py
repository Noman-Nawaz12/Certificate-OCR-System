from app.core.extractor import extract_all_fields


def test_extract_date():
    text = "This certifies that John Doe has completed the course. Date: 12/05/2024"
    fields = extract_all_fields(text)
    assert fields["issue_date"] == "12/05/2024"


def test_extract_candidate_name():
    text = "This is to certify that Jane Smith has successfully completed the Python Bootcamp"
    fields = extract_all_fields(text)
    assert fields["candidate_name"] is not None
    assert "Jane Smith" in fields["candidate_name"]


def test_extract_certificate_number():
    text = "Certificate Number: ABC-12345"
    fields = extract_all_fields(text)
    assert fields["certificate_number"] == "ABC-12345"


def test_no_fields_found_returns_none():
    text = "some random unrelated text with nothing useful"
    fields = extract_all_fields(text)
    assert fields["issue_date"] is None
