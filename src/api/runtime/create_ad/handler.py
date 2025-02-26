import os
import json
import datetime

import boto3
import uuid

dynamo_table = os.environ["TABLE_NAME"]
images_bucket = os.environ["IMAGES_BUCKET"]
days_to_expire = os.environ["DAYS_TO_EXPIRE"]

table = boto3.resource("dynamodb").Table(dynamo_table)
bucket = boto3.resource("s3").Bucket(images_bucket)


def handler(event, context):
    """Insert a new advert into the dynamo db table.

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
    print("Received event: " + json.dumps(event, indent=2))

    new_ad_id = str(uuid.uuid4())

    # Ensure the generated ad_id is unique
    while table.get_item(Key={"ad_id": new_ad_id}).get("Item"):
        new_ad_id = str(uuid.uuid4())

    ad_data = event["body"]

    new_ad = {
        "ad_id": new_ad_id,
        "title": ad_data["title"],
        "description": ad_data["description"],
        "price": ad_data["price"],
        "image": ad_data["image"],
        "creationDate": int(datetime.datetime.now().timestamp()),
        "expireAt": int(
            (
                datetime.datetime.now()
                + datetime.timedelta(days=int(days_to_expire))
            ).timestamp()
        ),
    }

    table.put_item(Item=new_ad)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(new_ad),
    }
