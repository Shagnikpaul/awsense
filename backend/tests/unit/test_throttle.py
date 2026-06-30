from unittest.mock import patch, MagicMock

from src.throttle import (
    load_session,
    record_request,
    record_tokens,
    request_window_expired,
    reset_request_window,
    check_request_limit,
    get_session_record,
    save_session,
)


@patch("src.throttle.get_session_record")
def test_load_existing_session(mock_get):
    mock_get.return_value = {
        "sessionId": "abc",
        "requestCount": 5,
        "tokenCount": 100,
        "windowStart": 123,
    }

    session = load_session("abc")

    assert session["sessionId"] == "abc"
    assert session["requestCount"] == 5
    assert session["tokenCount"] == 100
    assert session["windowStart"] == 123


@patch("src.throttle.current_timestamp")
@patch("src.throttle.get_session_record")
def test_load_new_session(mock_get, mock_time):
    mock_get.return_value = {}
    mock_time.return_value = 1000

    session = load_session("abc")

    assert session == {
        "sessionId": "abc",
        "requestCount": 0,
        "tokenCount": 0,
        "windowStart": 1000,
    }


@patch("src.throttle.save_session")
def test_record_request(mock_save):
    session = {
        "sessionId": "abc",
        "requestCount": 2,
        "tokenCount": 0,
        "windowStart": 1000,
    }

    record_request(session)

    assert session["requestCount"] == 3
    mock_save.assert_called_once_with(session)


@patch("src.throttle.save_session")
def test_record_tokens(mock_save):
    session = {
        "sessionId": "abc",
        "requestCount": 0,
        "tokenCount": 100,
        "windowStart": 1000,
    }

    record_tokens(session, 50)

    assert session["tokenCount"] == 150
    mock_save.assert_called_once_with(session)


@patch("src.throttle.current_timestamp")
def test_request_window_not_expired(mock_time):
    mock_time.return_value = 2000

    session = {
        "windowStart": 1000,
    }

    assert request_window_expired(session) is False


@patch("src.throttle.current_timestamp")
def test_request_window_expired(mock_time):
    mock_time.return_value = 5000

    session = {
        "windowStart": 1000,
    }

    assert request_window_expired(session) is True


@patch("src.throttle.current_timestamp")
def test_reset_request_window(mock_time):
    mock_time.return_value = 9999

    session = {
        "requestCount": 10,
        "windowStart": 1000,
    }

    reset_request_window(session)

    assert session["requestCount"] == 0
    assert session["windowStart"] == 9999


@patch("src.throttle.request_window_expired")
def test_check_request_limit_success(mock_expired):
    mock_expired.return_value = False

    session = {
        "sessionId": "abc",
        "requestCount": 5,
        "tokenCount": 100,
        "windowStart": 1000,
    }

    allowed, retry = check_request_limit(session)

    assert allowed is True
    assert retry == 0


@patch("src.throttle.current_timestamp")
@patch("src.throttle.request_window_expired")
def test_check_request_limit_hourly_limit(mock_expired, mock_time):
    mock_expired.return_value = False
    mock_time.return_value = 1500

    session = {
        "sessionId": "abc",
        "requestCount": 20,
        "tokenCount": 100,
        "windowStart": 1000,
    }

    allowed, retry = check_request_limit(session)

    assert allowed is False
    assert retry == 3100


@patch("src.throttle.request_window_expired")
def test_check_request_limit_token_limit(mock_expired):
    mock_expired.return_value = False

    session = {
        "sessionId": "abc",
        "requestCount": 5,
        "tokenCount": 50000,
        "windowStart": 1000,
    }

    allowed, retry = check_request_limit(session)

    assert allowed is False
    assert retry == 86400


@patch("src.throttle.reset_request_window")
@patch("src.throttle.request_window_expired")
def test_check_request_limit_resets_window(
    mock_expired,
    mock_reset,
):
    mock_expired.return_value = True

    session = {
        "sessionId": "abc",
        "requestCount": 5,
        "tokenCount": 100,
        "windowStart": 1000,
    }

    allowed, retry = check_request_limit(session)

    mock_reset.assert_called_once_with(session)
    assert allowed is True
    assert retry == 0


@patch("src.throttle.get_table")
def test_get_session_record(mock_get_table):
    table = MagicMock()
    table.get_item.return_value = {
        "Item": {
            "sessionId": "abc",
        }
    }

    mock_get_table.return_value = table

    result = get_session_record("abc")

    assert result["sessionId"] == "abc"

    table.get_item.assert_called_once_with(
        Key={
            "sessionId": "abc",
        }
    )


@patch("src.throttle.get_table")
def test_save_session(mock_get_table):
    table = MagicMock()

    mock_get_table.return_value = table

    session = {
        "sessionId": "abc",
    }

    save_session(session)

    table.put_item.assert_called_once_with(Item=session)
