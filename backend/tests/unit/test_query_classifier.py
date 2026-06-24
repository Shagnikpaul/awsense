from src.query_classifier import is_greeting


def test_hi_is_greeting():
    assert is_greeting("hi")


def test_hello_is_greeting():
    assert is_greeting("hello")


def test_s3_question_is_not_greeting():
    assert not is_greeting("What is Amazon S3?")


def test_ec2_question_is_not_greeting():
    assert not is_greeting("How does EC2 work?")
