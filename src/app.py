#!/usr/bin/env python3

import os
import aws_cdk as cdk

from component import SYWallaslsStack
from config import SYWallaConfig

config = SYWallaConfig()

app = cdk.App()
SYWallaslsStack(
    app,
    "SYWallaslsStack",
    config=config,
    env=cdk.Environment(
        account=os.environ["ACCOUNT"], region=os.environ["REGION"]
    ),
)

app.synth()
