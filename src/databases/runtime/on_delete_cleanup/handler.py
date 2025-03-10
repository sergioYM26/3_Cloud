import os
import json

import boto3
from boto3.dynamodb.conditions import Key

ads_table_name = os.environ["TABLE_NAME_ADS"]
comments_table_name = os.environ["TABLE_NAME_COMMENTS"]
images_bucket = os.environ["IMAGES_BUCKET"]

resource = boto3.resource("dynamodb")
ads_table = resource.Table(ads_table_name)
comments_table = resource.Table(comments_table_name)
s3 = boto3.client("s3")


def handler(event, context):
    """Delete comments and image when a ad entry is deleted.

    Parameters
    ----------
    event: dict
        The event that triggered the lambda function.
    context: dict
        The context of the lambda function.
    """
    print("Received event: " + json.dumps(event))

    for record in event["Records"]:
        if record["eventName"] == "REMOVE":
            ad_id = record["dynamodb"]["Keys"]["ad_id"]["S"]

            # Delete the ad image
            image_key = f"{ad_id}.jpeg"
            s3.delete_object(Bucket=images_bucket, Key=image_key)

            # Delete the ad comments
            comments = comments_table.query(
                KeyConditionExpression=Key("ad_id").eq(ad_id)
            )["Items"]

            for comment in comments:
                comment_id = comment["ad_id"]
                comments_table.delete_item(
                    Key={"ad_id": comment_id, "timestamp": comment["timestamp"]}
                )
