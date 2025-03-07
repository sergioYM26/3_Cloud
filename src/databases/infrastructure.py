import os
import aws_cdk as cdk

from constructs import Construct
from config import SYWallaConfig

import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_lambda_event_sources as lambda_events

RUNTIME_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/runtime"


class Databases(Construct):
    """Construct that creates all databases and needed resources."""

    def __init__(
        self, scope, id, *, config: SYWallaConfig, images_bucket: str, **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # advertisements dynamodb database
        self.advertisements = dynamodb.Table(
            self,
            f"{config.name}-{config.stage}-advertisements",
            table_name=f"{config.name}-{config.stage}-advertisements",
            partition_key=dynamodb.Attribute(
                name="ad_id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl-ad",
            stream=dynamodb.StreamViewType.KEYS_ONLY,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.Tags.of(self.advertisements).add(
            "Student-NAME", config.student_name
        )

        # Comments dynamo database
        self.comments = dynamodb.Table(
            self,
            f"{config.name}-{config.stage}-comments",
            table_name=f"{config.name}-{config.stage}-comments",
            partition_key=dynamodb.Attribute(
                name="ad_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.Tags.of(self.advertisements).add(
            "Student-NAME", config.student_name
        )

        # Clean up lambda dynamodb database
        self.cleanup_lambda = _lambda.DockerImageFunction(
            self,
            f"{config.name}-{config.stage}-on-delete-cleanup-lambda",
            function_name=f"{config.name}-{config.stage}-on-delete-cleanup-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/on_delete_cleanup"
            ),
            environment={
                "TABLE_NAME_ADS": self.advertisements.table_name,
                "TABLE_NAME_COMMENTS": self.comments.table_name,
                "IMAGES_BUCKET": images_bucket,
            },
        )

        self.cleanup_lambda.add_event_source(
            source=lambda_events.DynamoEventSource(
                self.advertisements,
                starting_position=_lambda.StartingPosition.LATEST,
            )
        )

        # chats dynamodb database
        self.chats = dynamodb.Table(
            self,
            f"{config.name}-{config.stage}-chats-data",
            table_name=f"{config.name}-{config.stage}-chats-data",
            partition_key=dynamodb.Attribute(
                name="chat_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="data", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.Tags.of(self.advertisements).add(
            "Student-NAME", config.student_name
        )
