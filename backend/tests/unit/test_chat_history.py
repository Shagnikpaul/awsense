from decimal import Decimal
from unittest.mock import MagicMock, patch

from src.chat_history import (
    convert_decimals,
    create_conversation,
    save_message,
    get_conversation,
    list_conversations,
    conversation_exists,
    get_conversation_metadata,
)

# ------------------------------------------------------------------
# convert_decimals
# ------------------------------------------------------------------


def test_convert_decimals_nested():
    data = {
        "a": Decimal("1"),
        "b": [
            Decimal("2"),
            {"c": Decimal("3")},
        ],
    }

    converted = convert_decimals(data)

    assert converted == {
        "a": 1,
        "b": [
            2,
            {"c": 3},
        ],
    }


# ------------------------------------------------------------------
# create_conversation
# ------------------------------------------------------------------


@patch("src.chat_history.get_conversations_table")
def test_create_conversation(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    create_conversation(
        client_id="client-1",
        conversation_id="conv-1",
        title="What is S3?",
    )

    table.put_item.assert_called_once()

    item = table.put_item.call_args.kwargs["Item"]

    assert item["clientId"] == "client-1"
    assert item["conversationId"] == "conv-1"
    assert item["title"] == "What is S3?"
    assert "createdAt" in item
    assert "updatedAt" in item
    assert "ttl" in item


# ------------------------------------------------------------------
# save_message
# ------------------------------------------------------------------


@patch("src.chat_history.get_messages_table")
@patch("src.chat_history.get_conversations_table")
def test_save_message(mock_conv_table, mock_msg_table):
    msg_table = MagicMock()
    conv_table = MagicMock()

    mock_msg_table.return_value = msg_table
    mock_conv_table.return_value = conv_table

    save_message(
        conversation_id="conv-1",
        role="assistant",
        content="Hello",
        sources=["url"],
        token_usage={
            "inputTokens": 10,
            "outputTokens": 5,
        },
    )

    msg_table.put_item.assert_called_once()
    conv_table.update_item.assert_called_once()


# ------------------------------------------------------------------
# get_conversation
# ------------------------------------------------------------------


@patch("src.chat_history.get_messages_table")
def test_get_conversation(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.query.return_value = {
        "Items": [
            {
                "conversationId": "conv",
                "timestamp": "123",
                "content": "hello",
                "role": "user",
                "ttl": Decimal("100"),
                "tokenUsage": {
                    "inputTokens": Decimal("4"),
                    "outputTokens": Decimal("2"),
                },
            }
        ]
    }

    messages = get_conversation("conv")

    assert len(messages) == 1

    assert messages[0]["content"] == "hello"

    assert "ttl" not in messages[0]

    assert messages[0]["tokenUsage"]["inputTokens"] == 4

    assert messages[0]["tokenUsage"]["outputTokens"] == 2


# ------------------------------------------------------------------
# list_conversations
# ------------------------------------------------------------------


@patch("src.chat_history.get_conversations_table")
def test_list_conversations(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.query.return_value = {
        "Items": [
            {
                "conversationId": "conv-1",
                "title": "S3",
                "ttl": Decimal("123"),
            }
        ]
    }

    conversations = list_conversations("client-1")

    assert len(conversations) == 1

    assert conversations[0]["conversationId"] == "conv-1"

    assert "ttl" not in conversations[0]


# ------------------------------------------------------------------
# conversation_exists
# ------------------------------------------------------------------


@patch("src.chat_history.get_conversations_table")
def test_conversation_exists_true(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.get_item.return_value = {"Item": {"conversationId": "conv"}}

    assert conversation_exists("conv") is True


@patch("src.chat_history.get_conversations_table")
def test_conversation_exists_false(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.get_item.return_value = {}

    assert conversation_exists("conv") is False


# ------------------------------------------------------------------
# get_conversation_metadata
# ------------------------------------------------------------------


@patch("src.chat_history.get_conversations_table")
def test_get_conversation_metadata(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.get_item.return_value = {
        "Item": {
            "conversationId": "conv-1",
            "clientId": "client-1",
            "ttl": Decimal("123"),
        }
    }

    metadata = get_conversation_metadata("conv-1")

    assert metadata["conversationId"] == "conv-1"

    assert metadata["clientId"] == "client-1"

    assert "ttl" not in metadata


@patch("src.chat_history.get_conversations_table")
def test_get_conversation_metadata_none(mock_table):
    table = MagicMock()
    mock_table.return_value = table

    table.get_item.return_value = {}

    assert get_conversation_metadata("conv-1") is None
