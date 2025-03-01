import os
import json
import boto3

from boto3.dynamodb.conditions import Key
from base64 import b64encode

dynamo_table_ads = os.environ["TABLE_NAME_ADS"]
dynamo_table_comments = os.environ["TABLE_NAME_COMMENTS"]
images_bucket = os.environ["IMAGES_BUCKET"]

resource = boto3.resource("dynamodb")
ads_table = resource.Table(dynamo_table_ads)
comments_table = resource.Table(dynamo_table_comments)
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
    print("Received event: " + json.dumps(event))

    ad_id = event["pathParameters"]["ad_id"]

    advertisement = ads_table.get_item(Key={"ad_id": ad_id}).get("Item")

    if not advertisement:
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Ad not found"}),
        }

    # Get comments
    comments = comments_table.query(
        KeyConditionExpression=Key("ad_id").eq(ad_id)
    )["Items"]

    advertisement["comments"] = comments

    # Get image
    try:
        image_obj = s3.get_object(Bucket=images_bucket, Key=f"{ad_id}.jpeg")
        image = image_obj["Body"].read()
        advertisement["image"] = b64encode(image).decode("utf-8")
    except s3.exceptions.NoSuchKey:
        advertisement["image"] = None  # Having image is optional

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(advertisement, default=int),
    }
