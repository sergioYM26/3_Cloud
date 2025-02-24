from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from config import SYWallaConfig


class SYWallaslsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: SYWallaConfig,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "SrcQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
