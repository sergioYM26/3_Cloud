import os
import json

import boto3
from datetime import datetime

dynamo_table = os.environ["TABLE_NAME"]
comments_table = boto3.resource("dynamodb").Table(dynamo_table)


def handler(event, context):
    print("Received event: " + json.dumps(event))

    author = event["requestContext"]["authorizer"]["claims"]["username"]

    ad_id = event.get("pathParameters", {}).get("ad_id")
    if not ad_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "ad_id is required"}),
        }

    comment_data = json.loads(event["body"])
    comment_data["ad_id"] = ad_id
    comment_data["timestamp"] = str(datetime.now().timestamp())
    comment_data["author"] = author

    comments_table.put_item(Item=comment_data)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Comment created successfully on ad_id: " + ad_id}
        ),
    }
