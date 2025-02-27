import os
import json

import boto3

dynamo_table = os.environ["TABLE_NAME"]
table = boto3.resource("dynamodb").Table(dynamo_table)


def handler(event, context):
    """Get all items from dynamodb database.

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
    items = table.scan().get("Items", [])
    return {"statusCode": 200, "body": json.dumps(items, default=int)}
