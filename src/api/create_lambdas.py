import os
import aws_cdk.aws_lambda as _lambda
from constructs import Construct
from config import SYWallaConfig

RUNTIME_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/runtime"


class ApiLambdas:
    """."""

    def __init__(
        self,
        scope: Construct,
        *,
        config: SYWallaConfig,
        ads_table: str,
        comments_table: str,
        images_bucket: str,
    ) -> None:
        # Advertisements - Lambdas
        self.create_ad = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-create-ad-lambda",
            function_name=f"{config.name}-{config.stage}-create-ad-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/create_ad"
            ),
            environment={
                "TABLE_NAME": ads_table,
                "IMAGES_BUCKET": images_bucket,
                "DAYS_TO_EXPIRE": config.ad_creation_days_to_expire,
            },
        )

        self.list_ads = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-list-ads-lambda",
            function_name=f"{config.name}-{config.stage}-list-ads-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/list_ads"
            ),
            environment={"TABLE_NAME": ads_table},
        )

        self.get_ad = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-get-ad-lambda",
            function_name=f"{config.name}-{config.stage}-get-ad-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/get_ad"
            ),
            environment={
                "TABLE_NAME_ADS": ads_table,
                "TABLE_NAME_COMMENTS": comments_table,
                "IMAGES_BUCKET": images_bucket,
            },
        )

        # Comments - Lambdas
        self.post_comment = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-post-comment-lambda",
            function_name=f"{config.name}-{config.stage}-post-comment-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/post_comment"
            ),
            environment={"TABLE_NAME": comments_table},
        )

        # Chat - Lambdas
        self.get_chat_messages = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-get-chat-messages-lambda",
            function_name=f"{config.name}-{config.stage}-get-chat-messages-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/get_chat_messages"
            ),
            environment={"TABLE_NAME": ads_table},
        )

        self.post_chat_message = _lambda.DockerImageFunction(
            scope,
            f"{config.name}-{config.stage}-post-chat-message-lambda",
            function_name=f"{config.name}-{config.stage}-post-chat-message-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/post_chat_message"
            ),
            environment={"TABLE_NAME": ads_table},
        )
