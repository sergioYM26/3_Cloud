import os
import json

import shortuuid
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamo_table = os.environ["TABLE_NAME"]
chats_table = boto3.resource("dynamodb").Table(dynamo_table)


def handler(event, context):
    """
    Send a message to a chat between two users or create a new chat if it doesn't exist.

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

    message_data = json.loads(event["body"])

    author = event["requestContext"]["authorizer"]["claims"]["username"]
    destination = message_data["destination"]
    message = message_data["message"]

    # See if there is already a chat between the two users
    chats = chats_table.scan(FilterExpression=Key("data").begins_with("USR_"))[
        "Items"
    ]

    chat_id = None
    for chat in chats:
        if author in chat["data"] or destination in chat["data"]:
            chat_id = chat["chat_id"]
            break

    if not chat_id:
        chat_id = shortuuid.uuid()
        # Ensure the generated ad_id is unique
        while chats_table.query(
            KeyConditionExpression=Key("chat_id").eq(chat_id)
        ).get("Items"):
            chat_id = shortuuid.uuid()
        chats_table.put_item(
            Item={
                "chat_id": chat_id,
                "data": f"USR_{author}:{destination}",
            }
        )

    chats_table.put_item(
        Item={
            "chat_id": chat_id,
            "author": author,
            "data": f"MSG_{str(datetime.now().timestamp())}",
            "message": message,
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Message sent successfully on chat_id: " + chat_id}
        ),
    }
