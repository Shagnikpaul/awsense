import pytest
from src.validator import validate_message


def test_valid_message():
    valid, error = validate_message("What is AWS Lambda?")
    assert valid is True
    assert error is None


def test_empty_message():
    valid, error = validate_message("")
    assert valid is False
    assert error is not None


def test_long_message():
    long_msg = "x" * 600
    valid, error = validate_message(long_msg)
    assert valid is False
    assert error is not None
