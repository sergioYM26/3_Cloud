import os
import json
import datetime

import boto3
import shortuuid

from PIL import Image
from io import BytesIO
from base64 import b64decode

dynamo_table = os.environ["TABLE_NAME"]
images_bucket = os.environ["IMAGES_BUCKET"]
days_to_expire = os.environ["DAYS_TO_EXPIRE"]

table = boto3.resource("dynamodb").Table(dynamo_table)
s3 = boto3.client("s3")


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
    print("Received event: " + json.dumps(event))

    new_ad_id = shortuuid.uuid()

    # Ensure the generated ad_id is unique
    while table.get_item(Key={"ad_id": new_ad_id}).get("Item"):
        new_ad_id = shortuuid.uuid()

    ad_data = json.loads(event["body"])

    new_ad = {
        "ad_id": new_ad_id,
        "title": ad_data["title"],
        "description": ad_data["description"],
        "price": ad_data["price"],
        "creationDate": int(datetime.datetime.now().timestamp()),
        "expireAt": int(
            (
                datetime.datetime.now()
                + datetime.timedelta(days=int(days_to_expire))
            ).timestamp()
        ),
    }

    image = ad_data.get("image")
    image_name = ad_data.get("imageName")
    if image and image_name:
        im = Image.open(BytesIO(b64decode(image)))
        im.thumbnail((300, 300))  # Resize image to 300x300
        in_memory_file = BytesIO()
        im.save(in_memory_file, "JPEG")
        in_memory_file.seek(0)

        s3.upload_fileobj(in_memory_file, images_bucket, f"{new_ad_id}.jpeg")

    table.put_item(Item=new_ad)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(
            {"message": f"Ad created successfully with id: {new_ad_id}"}
        ),
    }
