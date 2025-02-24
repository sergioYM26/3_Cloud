#!/usr/bin/env python3

import aws_cdk as cdk

from core.component import SYWallaslsStack
from config import SYWallaConfig

config = SYWallaConfig()

app = cdk.App()
SYWallaslsStack(
    app,
    "SYWallaslsStack",
    config=config,
    env=cdk.Environment(account=config.account_id, region=config.region),
)

app.synth()
