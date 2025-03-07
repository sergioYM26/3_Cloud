from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from config import SYWallaConfig

from databases.infrastructure import Databases
from images.infrastructure import Images
from users.infrastructure import Users
from api.infrastructure import Api


class SYWallaslsStack(Stack):
    """Stack definition, instantiates all the constructs."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: SYWallaConfig,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        images = Images(self, "Images", config=config)
        databases = Databases(
            self,
            "Databases",
            config=config,
            images_bucket=images.images_bucket.bucket_name,
        )
        users = Users(self, "Users", config=config)
        api = Api(
            self,
            "Api",
            config=config,
            user_pool=users.user_pool,
            ads_table=databases.advertisements.table_name,
            comments_table=databases.comments.table_name,
            chats_table=databases.chats.table_name,
            images_bucket=images.images_bucket.bucket_name,
        )

        databases.advertisements.grant_read_write_data(api.lambdas.create_ad)
        databases.advertisements.grant_read_write_data(api.lambdas.list_ads)
        databases.advertisements.grant_read_write_data(api.lambdas.get_ad)
        databases.advertisements.grant_read_write_data(api.lambdas.post_comment)
        databases.advertisements.grant_read_write_data(databases.cleanup_lambda)

        databases.comments.grant_read_write_data(api.lambdas.post_comment)
        databases.comments.grant_read_write_data(api.lambdas.get_ad)
        databases.comments.grant_read_write_data(databases.cleanup_lambda)

        databases.chats.grant_read_write_data(api.lambdas.get_chats)
        databases.chats.grant_read_write_data(api.lambdas.post_chat_message)
        databases.chats.grant_read_write_data(api.lambdas.get_chat_messages)

        images.images_bucket.grant_read_write(api.lambdas.create_ad)
        images.images_bucket.grant_read_write(api.lambdas.get_ad)
        images.images_bucket.grant_read_write(databases.cleanup_lambda)
