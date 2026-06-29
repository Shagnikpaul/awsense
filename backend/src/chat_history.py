import os
import time
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key


def convert_decimals(value):
    if isinstance(value, Decimal):
        return int(value)

    if isinstance(value, list):
        return [convert_decimals(v) for v in value]

    if isinstance(value, dict):
        return {k: convert_decimals(v) for k, v in value.items()}

    return value


def get_conversations_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ["CONVERSATIONS_TABLE"])


def get_messages_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ["CHAT_MESSAGES_TABLE"])


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def ttl_timestamp():
    return int(time.time()) + (30 * 24 * 60 * 60)


def create_conversation(client_id: str, conversation_id: str, title: str):
    """
    Creates a new conversation.
    Called only once—the first time a message is sent in a new chat.
    """
    timestamp = now_iso()

    get_conversations_table().put_item(
        Item={
            "conversationId": conversation_id,
            "clientId": client_id,
            "title": title,
            "createdAt": timestamp,
            "updatedAt": timestamp,
            "ttl": ttl_timestamp(),
        },
        ConditionExpression="attribute_not_exists(conversationId)",
    )


def save_message(
    conversation_id: str, role: str, content: str, sources=None, token_usage=None
):
    """
    Saves a single chat message.
    """
    timestamp = now_iso()

    get_messages_table().put_item(
        Item={
            "conversationId": conversation_id,
            "timestamp": timestamp,
            "role": role,
            "content": content,
            "sources": sources or [],
            "tokenUsage": token_usage or {},
            "ttl": ttl_timestamp(),
        }
    )

    # Keep the conversation at the top of the sidebar.
    get_conversations_table().update_item(
        Key={
            "conversationId": conversation_id,
        },
        UpdateExpression="""
            SET
                updatedAt = :updatedAt,
                #ttl = :ttl
        """,
        ConditionExpression="attribute_exists(conversationId)",
        ExpressionAttributeNames={
            "#ttl": "ttl",
        },
        ExpressionAttributeValues={
            ":updatedAt": timestamp,
            ":ttl": ttl_timestamp(),
        },
    )


def get_conversation(conversation_id: str):
    """
    Returns every message in chronological order.
    """
    response = get_messages_table().query(
        KeyConditionExpression=Key("conversationId").eq(conversation_id),
        ScanIndexForward=True,  # oldest → newest
    )

    items = response.get("Items", [])

    for item in items:
        item.pop("ttl", None)

    return convert_decimals(items)


def list_conversations(client_id: str, limit: int = 20):
    """
    Returns all conversations belonging to one browser,
    ordered by updatedAt descending.
    """
    response = get_conversations_table().query(
        IndexName="clientId-updatedAt-index",
        KeyConditionExpression=Key("clientId").eq(client_id),
        ScanIndexForward=False,  # newest first
        Limit=limit,
    )
    items = response.get("Items", [])

    for item in items:
        item.pop("ttl", None)

    return items


def conversation_exists(conversation_id):
    response = get_conversations_table().get_item(
        Key={
            "conversationId": conversation_id,
        }
    )

    return "Item" in response


def get_conversation_metadata(conversation_id: str):
    response = get_conversations_table().get_item(
        Key={
            "conversationId": conversation_id,
        }
    )

    item = response.get("Item")

    if item:
        item.pop("ttl", None)

    return item
