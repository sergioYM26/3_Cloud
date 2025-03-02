import os
import json

import boto3
from boto3.dynamodb.conditions import Key

dynamo_table = os.environ["TABLE_NAME"]
chats_table = boto3.resource("dynamodb").Table(dynamo_table)


def handler(event, context):
    """
    Get all chats where the user is involved

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

    user = event["requestContext"]["authorizer"]["claims"]["username"]

    # Get all chats where the user is involved
    chats = chats_table.scan(FilterExpression=Key("data").begins_with("USR_"))[
        "Items"
    ]

    chats_user = []
    for chat in chats:
        if user in chat["data"]:
            chats_user.append(
                {"chat_id": chat["chat_id"], "users": chat["data"]}
            )

    return {
        "statusCode": 200,
        "body": json.dumps(chats_user, default=int),
    }
