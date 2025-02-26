import os
import json

dynamo_table = os.environ["TABLE_NAME"]


def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
