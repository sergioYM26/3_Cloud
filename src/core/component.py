from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from config import SYWallaConfig

from databases.infrastructure import Databases
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
        Api(
            self,
            "Api",
            config=config,
            ads_table=databases.advertisements.table_name,
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "SrcQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
