import os
import json
import boto3

from base64 import b64encode

dynamo_table = os.environ["TABLE_NAME"]
images_bucket = os.environ["IMAGES_BUCKET"]

table = boto3.resource("dynamodb").Table(dynamo_table)
s3 = boto3.client("s3")


def handler(event, context):
    """Get specific advert data from given ID.

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

    ad_id = event["pathParameters"]["ad_id"]

    advertisement = table.get_item(Key={"ad_id": ad_id}).get("Item")

    if not advertisement:
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Ad not found"}),
        }

    try:
        image_obj = s3.get_object(Bucket=images_bucket, Key=f"{ad_id}.jpeg")
        image = image_obj["Body"].read()
        advertisement["image"] = b64encode(image).decode("utf-8")
    except s3.exceptions.NoSuchKey:
        advertisement["image"] = None

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(advertisement, default=int),
    }
