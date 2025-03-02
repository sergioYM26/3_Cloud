from constructs import Construct
import aws_cdk.aws_s3 as s3
import aws_cdk as cdk

from config import SYWallaConfig


class Images(Construct):
    """Construct that creates the bucket for the ads images."""

    def __init__(
        self, scope: Construct, id: str, *, config: SYWallaConfig, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.images_bucket = s3.Bucket(
            self,
            f"{config.name}-{config.stage}-ads-images",
            bucket_name=f"{config.name}-{config.stage}-ads-images",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
