from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from config import SYWallaConfig

from databases.infrastructure import Databases
from images.infrastructure import Images
from api.infrastructure import Api


class SYWallaslsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: SYWallaConfig,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        databases = Databases(self, "Databases", config=config)
        images = Images(self, "Images", config=config)
        api = Api(
            self,
            "Api",
            config=config,
            ads_table=databases.advertisements.table_name,
            images_bucket=images.images_bucket.bucket_name,
        )

        databases.advertisements.grant_write_data(api.lambdas.create_ad)
        databases.advertisements.grant_read_data(api.lambdas.list_ads)
        databases.advertisements.grant_read_data(api.lambdas.get_ad)
        databases.advertisements.grant_write_data(api.lambdas.post_comment)

        databases.chats.grant_write_data(api.lambdas.post_chat_message)
        databases.chats.grant_read_data(api.lambdas.get_chat_messages)

        images.images_bucket.grant_write(api.lambdas.create_ad)
        images.images_bucket.grant_read(api.lambdas.get_ad)
