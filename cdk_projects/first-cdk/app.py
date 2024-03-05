#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_stacks.crud_cdk import CrudCdkStack


app = cdk.App()
CrudCdkStack(app, "FirstCdkStack", env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
