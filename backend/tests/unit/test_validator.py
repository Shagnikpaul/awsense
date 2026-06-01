from src.validator import validate_message


def test_valid_message():
    valid, _ = validate_message("What is S3?")
    assert valid is True


def test_empty_message():
    valid, _ = validate_message("")
    assert valid is False


def test_too_long_message():
    valid, _ = validate_message("a" * 501)
    assert valid is False
