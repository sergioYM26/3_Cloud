import os
import json

import boto3

dynamo_table = os.environ["TABLE_NAME"]
client = boto3.client("dynamodb")


def handler(event, context):
    table = client.Table(dynamo_table)
    items = table.scan().get("Items", [])
    return {"statusCode": 200, "body": json.dumps(items)}
