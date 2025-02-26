import aws_cdk as cdk

from constructs import Construct
from config import SYWallaConfig

import aws_cdk.aws_dynamodb as dynamodb


class Databases(Construct):
    """."""

    def __init__(self, scope, id, *, config: SYWallaConfig, **kwargs):
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
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.Tags.of(self.advertisements).add(
            "Student-NAME", config.student_name
        )

        # chats dynamodb database
        self.chats = dynamodb.Table(
            self,
            f"{config.name}-{config.stage}-chats",
            table_name=f"{config.name}-{config.stage}-chats",
            partition_key=dynamodb.Attribute(
                name="chat_id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        cdk.Tags.of(self.advertisements).add(
            "Student-NAME", config.student_name
        )
