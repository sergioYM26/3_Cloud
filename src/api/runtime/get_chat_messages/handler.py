import os
import json

import boto3
from boto3.dynamodb.conditions import Key

dynamo_table = os.environ["TABLE_NAME"]
chats_table = boto3.resource("dynamodb").Table(dynamo_table)


def handler(event, context):
    """
    Get all messages from a chat

    Parameters
    ----------
    event: dict
        The event that triggered the lambda function.
    context: dict
        The context of the lambda function.
    Returns
    -------
    dict
        The HTTP response of the lambda function.
    """
    print("Received event: " + json.dumps(event))

    chat_id = event.get("pathParameters", {}).get("chat_id")
    if not chat_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "chat_id is required"}),
        }

    # Get all messages from the chat
    messages = chats_table.query(
        KeyConditionExpression=Key("chat_id").eq(chat_id)
    )["Items"]

    messages = [
        message for message in messages if message["data"].startswith("MSG_")
    ]

    return {
        "statusCode": 200,
        "body": json.dumps({"messages": messages}, default=int),
    }
